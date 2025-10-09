
from pathlib import Path
DEFAULT_PKL_DIR = str(Path(__file__).resolve().parent / "pkl")
import pickle
import numpy as np
import faiss
from numpy.random import default_rng

def distance_manhattan(x_db, x_q):
    return np.abs(x_db - x_q[None,:]).sum(-1)


class MJHand():
    def __init__(
        self,
        pkl_dir=DEFAULT_PKL_DIR,
        seed=None,
        ):
        pkl_file = Path(pkl_dir) / "all_winhand_patterns.pkl"
        self.tiles_csr, self.weights = pickle.load(open(pkl_file, 'rb'))
        self.tiles_csr = self.tiles_csr.toarray().astype(np.int8)
        self.num_patterns = self.tiles_csr.shape[0]
        self.num_tiles = self.tiles_csr.shape[1]
        self.rng = default_rng(seed)
        self.indices = np.arange(self.num_patterns)
        self.index = faiss.IndexFlat(self.num_tiles, faiss.METRIC_L1)
        self.index.add(self.tiles_csr)

    def sample_win_hand(self, num_samples=1):
        ids = self.rng.choice(self.indices, size=num_samples, replace=True, p=self.weights/np.sum(self.weights))
        tiles = self.tiles_csr[ids].copy()
        win_tile = np.array([self.rng.choice(range(self.num_tiles), size=1, p=t/np.sum(t))[0] for t in tiles])
        win_tile_onehot = np.eye(self.num_tiles, dtype=int)[win_tile]
        return {"hands": tiles, "win_tiles": win_tile, "win_tiles_onehot": win_tile_onehot}

    def sample_random_hand(self, num_samples=1, num_tiles=14):
        stack = []
        for _ in range(num_samples):
            index_136 = self.rng.choice(range(136), size=num_tiles)
            index_34 = index_136 // 4
            stack.append(convert_34_index_to_34_array(index_34))
        return np.array(stack, dtype=np.int8)

    def search_knn_win_hand(self, query_hand, k=1000):
        query_hand, squeeze = (query_hand[None, :], True) if query_hand.ndim == 1 else (query_hand, False)
        knn_dists, args_k = self.index.search(query_hand, k=k)
        knn_dists = knn_dists.astype(int)
        knn_hands = self.tiles_csr[args_k]
        if squeeze:
            knn_dists, knn_hands = knn_dists.squeeze(), knn_hands.squeeze()
        return {"hands": knn_hands, "manhattan": knn_dists}

    def search_knn_win_hand_slow(self, query_hand, k=1000):
        dists = distance_manhattan(self.tiles_csr, query_hand.astype(np.int8))
        args_k = np.argpartition(dists, k)[:k]
        knn_hands = self.tiles_csr[args_k]
        knn_dists = dists[args_k]
        idx = np.argsort(knn_dists)
        knn_dists = knn_dists[idx]
        knn_hands = knn_hands[idx]
        return {"hands": knn_hands, "manhattan": knn_dists}



def convert_34_index_to_34_array(index_34):
    array_34 = np.zeros(34, dtype=np.int8)
    for i in index_34:
        array_34[i] += 1
    return array_34


def convert_34_array_to_string_dict(array_34):
    m = ''.join([str(i+1)*array_34[i+ 0] for i in range(9) if array_34[i] > 0])
    p = ''.join([str(i+1)*array_34[i+ 9] for i in range(9) if array_34[i+9] > 0])
    s = ''.join([str(i+1)*array_34[i+18] for i in range(9) if array_34[i+18] > 0])
    z = ''.join([str(i+1)*array_34[i+27] for i in range(7) if array_34[i+27] > 0])
    return {"man": m, "pin": p, "sou": s, "honors": z}
