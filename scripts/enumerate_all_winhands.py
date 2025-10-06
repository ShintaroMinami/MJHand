#! /usr/bin/env python

import pickle
import itertools
import numpy as np
from tqdm import tqdm
from scipy.sparse import csr_matrix
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from pathlib import Path
BASE_DIR = str(Path(__file__).resolve().parent.parent)

parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('--pkl_dir', type=str, default=BASE_DIR+'/mjhand/pkl/', help='pkl directory to load patterns from')
parser.add_argument('--out_pkl', type=str, default='all_winhand_patterns.pkl', help='output .pkl file to save patterns')
args = parser.parse_args()


def is_chiitoitsu(hd):
    return np.all((hd == 0) | (hd == 2))

def load_pkl_file(pklfile):
    data = {}
    for d in pickle.load(open(pklfile, 'rb')):
        num = d['num']
        if num == 0: continue
        if num not in data:
            data[num] = []
        data[num].append((d['tiles'], d['count']))
    return data

patterns_mps_mn = load_pkl_file(f'{args.pkl_dir}/org/patterns_mps_mentsu.pkl')
patterns_mps_jt = load_pkl_file(f'{args.pkl_dir}/org/patterns_mps_mentsu_jantou.pkl')
patterns_z_mn = load_pkl_file(f'{args.pkl_dir}/org/patterns_z_mentsu.pkl')
patterns_z_jt = load_pkl_file(f'{args.pkl_dir}/org/patterns_z_mentsu_jantou.pkl')

#patterns_mps_mn = pickle.load(open(f'{args.pkl_dir}/org/patterns_mps_mentsu.pkl', 'rb'))
#patterns_mps_jt = pickle.load(open(f'{args.pkl_dir}/org/patterns_mps_mentsu_jantou.pkl', 'rb'))
#patterns_z_mn = pickle.load(open(f'{args.pkl_dir}/org/patterns_z_mentsu.pkl', 'rb'))
#patterns_z_jt = pickle.load(open(f'{args.pkl_dir}/org/patterns_z_mentsu_jantou.pkl', 'rb'))

patterns_mps = {**patterns_mps_mn, **patterns_mps_jt}
patterns_z = {**patterns_z_mn, **patterns_z_jt}


pattern_total, count_total, tiles_list, weights_list = 0, 0, [], []

# Kokushi Musou
kokushi_tiles = [0,8,9,17,18,26] + list(range(27,34))
for ids in kokushi_tiles:
    hd = np.zeros(34, dtype=np.int8)
    hd[np.array(kokushi_tiles)] = 1
    hd[np.array(ids)] = 2
    tiles_list.append(hd)
    weights_list.append((4**12)*6)

print("Kokushi Musou patterns:", len(tiles_list))
print("Kokushi Musou weights:", sum(weights_list))

# Chiitoitsu
num_check, weight_check = 0, 0
for ids in itertools.combinations(range(34), 7):
    hd = np.zeros(34, dtype=np.int8)
    hd[np.array(ids)] = 2
    tiles_list.append(hd)
    weights_list.append(6**7)
    num_check += 1
    weight_check += 6**7

print("Chiitoitsu patterns:", num_check)
print("Chiitoitsu weights:", weight_check)

# 4 Mentsu + 1 Jantou
num_check, num_remove, weight_check, weight_remove = 0, 0, 0, 0
for mt_num in tqdm(list(itertools.combinations_with_replacement(range(4), 4))):
    mt_count = np.zeros(4, dtype=int)
    for idx in mt_num: mt_count[idx] += 1
    for jt_num in range(4):
        jt_count = np.zeros(4, dtype=int)
        jt_count[jt_num] = 1
        tiles_count = 3*mt_count + 2*jt_count
        stack_pattern, stack_num_pattern, stack_num_count = [], [], []
        for n_tiles in tiles_count[:3]:
            n_count = 1 if n_tiles == 0 else sum([d[1] for d in patterns_mps[int(n_tiles)]])
            pattern = [([0]*9, 1)] if n_tiles == 0 else patterns_mps[int(n_tiles)]
            n_pattern = len(pattern)
            stack_pattern.append(pattern)
            #stack_num_pattern.append(n_pattern)
            #stack_num_count.append(n_count)
        for n_tiles in tiles_count[3:]:
            n_count = 1 if n_tiles == 0 else sum([d[1] for d in patterns_z[int(n_tiles)]])
            pattern = [([0]*7, 1)] if n_tiles == 0 else patterns_z[int(n_tiles)]
            n_pattern = len(pattern)
            stack_pattern.append(pattern)
            #stack_num_pattern.append(n_pattern)
            #stack_num_count.append(n_count)
        #count_total += np.prod(stack_num_count)
        #pattern_total += np.prod(stack_num_pattern)
        for a in itertools.product(*stack_pattern):
            tiles, count = zip(*a)
            tiles = np.concat(tiles, dtype=np.int8)
            prod_weight = np.prod(count)
            num_check += 1
            weight_check += prod_weight
            if is_chiitoitsu(tiles):
                num_remove += 1
                weight_remove += prod_weight
                continue
            tiles_list.append(tiles)
            weights_list.append(prod_weight)


print("Removed patterns:", num_remove)
print("Removed weights:", weight_remove)

print("4 Mentsu + 1 Jantou patterns:", num_check)
print("4 Mentsu + 1 Jantou weights:", weight_check)

print("Total winhand patterns:", len(tiles_list))
print("Total winhand weights:", sum(weights_list))

print("Win Hand Probability:", sum(weights_list) /4250305029168216000 )

tiles_np = np.stack(tiles_list)
tiles_csr = csr_matrix(tiles_np)

weights_np = np.array(weights_list, dtype=np.int64)

pickle.dump((tiles_csr, weights_np), open(args.out_pkl, 'wb'))
