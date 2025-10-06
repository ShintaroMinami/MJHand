#! /usr/bin/env python
'''
This script was implemented based on the following web page.
https://qiita.com/tomohxx/items/96a4efaacfbb6761cc59
'''

import os
import numpy as np
from itertools import combinations
from pathlib import Path
BASE_DIR = str(Path(__file__).resolve().parent.parent)
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('--pkl_dir', type=str, default=BASE_DIR+'/mjhand/pkl/org/', help='pkl directory to save patterns')
args = parser.parse_args()

S = 3  # 数牌の種類数
H = 7  # 字牌の種類数
T = 9 * S + H  # 全ての牌の種類数
M = 14  # 手牌の枚数

num = [[0] * 3 for _ in range(M + 1)]
den = [[0] * 3 for _ in range(M + 1)]

ntot = nlh = ntsis = nsp = nto = 0
dtot = dlh = dtsis = dsp = dto = 0

mentsu_n = []
mentsu_n_jt = []
toitsu = []


def iswh0(t):
    a, b = t[0], t[1]
    for i in range(7):
        r = a % 3
        if b >= r and t[i + 2] >= r:
            a, b = b - r, t[i + 2] - r
        else:
            return False
    return a % 3 == 0 and b % 3 == 0


def iswh2(t):
    p = sum(i * t[i] for i in range(9))
    for i in range(p * 2 % 3, 9, 3):
        if t[i] >= 2:
            t[i] -= 2
            if iswh0(t):
                t[i] += 2
                return True
            t[i] += 2
    return False


def issp(t):
    return all(x == 0 or x == 2 for x in t)


def dealtile(n, m, l, d):
    hd = [0] * 34
    c = [1, 4, 6, 4, 1]
    sum_ = [0] * 10
    def recurse(n, m, l, d):
        if n == 9:
            num[sum_[9]][0] += 1
            den[sum_[9]][0] += d

            if sum_[9] % 3 == 0 and iswh0(hd):
                mentsu_n.append({"num": sum(hd), "tiles": hd[:9].copy(), "count": d})
                num[sum_[9]][1] += 1
                den[sum_[9]][1] += d

                if sum_[9] % 2 == 0 and issp(hd):
                    num[sum_[9]][2] += 1
                    den[sum_[9]][2] += d

            elif sum_[9] % 3 == 2 and iswh2(hd):
                mentsu_n_jt.append({"num": sum(hd), "tiles": hd[:9].copy(), "count": d})
                num[sum_[9]][1] += 1
                den[sum_[9]][1] += d

                if sum_[9] % 2 == 0 and issp(hd):
                    num[sum_[9]][2] += 1
                    den[sum_[9]][2] += d

        else:
            for i in range(min(4, m) + 1):
                hd[n] = i
                sum_[n + 1] = sum_[n] + i
                recurse(n + 1, m - i, l - 4, d * c[i])

    recurse(n, m, l, d)


dealtile(0, M, 4 * (T - 1), 1)

mentsu_z = []
for n_ko in range(5):
    for a in combinations(range(7), n_ko):
        hd = np.array([0] * 7)
        if n_ko > 0:
            hd[np.array(a)] = 3
        mentsu_z.append({
            "num": int(sum(hd)),
            "tiles": hd.tolist().copy(),
            "count": 4 ** (len(a))
        })

mentsu_z_jt = []
for men in mentsu_z:
    count0 = men['count']
    hd = men['tiles']
    for i in np.where(np.array(hd) == 0)[0]:
        hd = men['tiles'].copy()
        hd[i] = 2
        count = count0 * 6
        mentsu_z_jt.append({
            "num": int(sum(hd)),
            "tiles": hd.copy(),
            "count": count
        })



os.makedirs(args.pkl_dir, exist_ok=True)

import pickle
pickle.dump(mentsu_n, open(f"{args.pkl_dir}/patterns_mps_mentsu.pkl", "wb"))
pickle.dump(mentsu_n_jt, open(f"{args.pkl_dir}/patterns_mps_mentsu_jantou.pkl", "wb"))
pickle.dump(mentsu_z, open(f"{args.pkl_dir}/patterns_z_mentsu.pkl", "wb"))
pickle.dump(mentsu_z_jt, open(f"{args.pkl_dir}/patterns_z_mentsu_jantou.pkl", "wb"))
