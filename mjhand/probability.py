import numpy as np

TOTAL_TILES = 136
MAX_TSUMO = 20

index = np.arange(0, TOTAL_TILES+1, dtype=int)
index[0] = 1
LOG_INDEX = np.log(index)

def log_nPm(n,m):
    return LOG_INDEX[n:n-m:-1].sum()

LOG_nPm_MAT = np.zeros((TOTAL_TILES+1,MAX_TSUMO+1), dtype=float)
for i in range(1, TOTAL_TILES+1):
    for j in range(1, MAX_TSUMO):
        LOG_nPm_MAT[i,j] = log_nPm(i,j)

LOG_N_FACTORIAL = np.insert(np.log(np.arange(1, MAX_TSUMO+1)).cumsum(), 0, 0)

def get_win_probability(hand, win_hands, n_tsumo=None, tiles_open=None):
    win_hands = win_hands[None,:] if win_hands.ndim == 1 else win_hands
    tiles_open = tiles_open if tiles_open is not None else hand
    tiles_remain = 4 * np.ones_like(34, dtype=np.int8) - tiles_open
    nr_k = np.clip(win_hands - hand[None,:], 0, None)
    N = nr_k.sum(-1).max() if n_tsumo is None else n_tsumo
    mask = (nr_k > 0)
    Nr_k = (tiles_remain[None, :]*mask)
    N0_k = (tiles_remain[None, :]*(~mask))
    nr = nr_k.sum(-1)
    n0 = N - nr
    Nr = Nr_k.sum(-1)
    N0 = N0_k.sum(-1)
    log_N0_P_n0 = LOG_nPm_MAT[N0, n0]
    sum_log_Nrk_P_nrk = LOG_nPm_MAT[Nr_k, nr_k].sum(-1)
    log_N0_Nr_P_n0_nr = LOG_nPm_MAT[N0+Nr, n0+nr]
    log_n0_nr_1_P_nr_1 = LOG_nPm_MAT[n0+nr-1, nr-1]
    log_nr = np.log(nr)
    sum_log_n_factorial = LOG_N_FACTORIAL[nr_k].sum(-1)
    log_prob = log_N0_P_n0 + sum_log_Nrk_P_nrk - log_N0_Nr_P_n0_nr + log_n0_nr_1_P_nr_1 + log_nr - sum_log_n_factorial
    return np.exp(log_prob)

