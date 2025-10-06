#! /usr/bin/env python
'''
This script was implemented based on the following web page.
https://qiita.com/tomohxx/items/96a4efaacfbb6761cc59
'''

from math import comb, pow

S = 3  # 数牌の種類数
H = 7  # 字牌の種類数
T = 9 * S + H  # 全ての牌の種類数
M = 14  # 手牌の枚数

num = [[0] * 3 for _ in range(M + 1)]
den = [[0] * 3 for _ in range(M + 1)]

ntot = nlh = ntsis = nsp = nto = 0
dtot = dlh = dtsis = dsp = dto = 0


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
                num[sum_[9]][1] += 1
                den[sum_[9]][1] += d

                if sum_[9] % 2 == 0 and issp(hd):
                    num[sum_[9]][2] += 1
                    den[sum_[9]][2] += d
            elif sum_[9] % 3 == 2 and iswh2(hd):
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


def dealsum(n, m, l):
    c = [[1, 1, 1], [1, 0, 0], [1, 1, 1], [1, 1, 0], [1, 0, 0]]
    d = [[1, 1, 1], [4, 0, 0], [6, 6, 6], [4, 4, 0], [1, 0, 0]]
    res = [[0] * 3 for _ in range(S + H + 2)]
    p = [1] * (S + H + 2)
    q = [1] * (S + H + 2)
    r = [1] * (S + H + 2)
    s = [1] * (S + H + 2)
    t = [1] * (S + H + 2)
    u = [1] * (S + H + 2)

    def recurse(n, m, l):
        global ntot, dtot, nlh, dlh, ntsis, dtsis
        if n == S + H:
            ntot += p[S + H]
            dtot += s[S + H]

            if res[S + H][1] == 0 and res[S + H][2] == 1:
                nlh += q[S + H]
                dlh += t[S + H]
                ntsis += r[S + H]
                dtsis += u[S + H]
        elif n < H:
            for i in range(max(0, m - l + 4), min(4, m) + 1):
                res[n + 1] = res[n][:]
                res[n + 1][i % 3] += 1
                p[n + 1] = p[n] * c[i][0]
                q[n + 1] = q[n] * c[i][1]
                r[n + 1] = r[n] * c[i][2]
                s[n + 1] = s[n] * d[i][0]
                t[n + 1] = t[n] * d[i][1]
                u[n + 1] = u[n] * d[i][2]
                recurse(n + 1, m - i, l - 4)
        else:
            for i in range(max(0, m - l + 36), min(M, m) + 1):
                res[n + 1] = res[n][:]
                res[n + 1][i % 3] += 1
                p[n + 1] = p[n] * num[i][0]
                q[n + 1] = q[n] * num[i][1]
                r[n + 1] = r[n] * num[i][2]
                s[n + 1] = s[n] * den[i][0]
                t[n + 1] = t[n] * den[i][1]
                u[n + 1] = u[n] * den[i][2]
                recurse(n + 1, m - i, l - 36)

    recurse(n, m, l)


def main():
    global nsp, dsp, nto, dto
    dealtile(0, M, 4 * (T - 1), 1)
    dealsum(0, M, 4 * T)

    nsp = comb(T, M // 2)
    dsp = comb(T, M // 2) * pow(6, M // 2)
    nto = 13
    dto = 13 * 6 * pow(4, 12)

    print(f"Number of Tiles: {M}")
    print(f"Total: {ntot} {dtot}")
    print(f"Legal Hand: {nlh} {dlh} {100.0 * dlh / dtot:.2f}%")
    print(f"Internal Seven Pairs: {ntsis} {dtsis} {100.0 * dtsis / dtot:.2f}%")
    print(f"Seven Pairs: {nsp} {dsp} {100.0 * dsp / dtot:.2f}%")
    print(f"Thirteen Orphans: {nto} {dto} {100.0 * dto / dtot:.2f}%")
    print(f"Probability: {(dlh + dsp - dtsis + dto) / dtot:.15e}")

if __name__ == "__main__":
    main()
