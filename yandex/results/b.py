import sys
import math

input = sys.stdin.readline

def entropy(ones, total):
    if ones == 0 or ones == total:
        return 0.0
    p = ones / total
    return -p * math.log(p) - (1 - p) * math.log(1 - p)

n, k = map(int, input().split())
labels = [0] + list(map(int, input().split()))

N = 2 * n - 1
left_child = [0] * (N + 1)
right_child = [0] * (N + 1)

for v in range(n + 1, N + 1):
    l, r = map(int, input().split())
    left_child[v] = l
    right_child[v] = r

sub_size = [0] * (N + 1)
sub_ones = [0] * (N + 1)

for v in range(1, n + 1):
    sub_size[v] = 1
    sub_ones[v] = labels[v]

for v in range(n + 1, N + 1):
    l = left_child[v]
    r = right_child[v]
    sub_size[v] = sub_size[l] + sub_size[r]
    sub_ones[v] = sub_ones[l] + sub_ones[r]

infinite = 10**10
dp = [None] * (N + 1)

for v in range(1, n + 1):
    dp[v] = [infinite, 0.0]

for v in range(n + 1, N + 1):
    l = left_child[v]
    r = right_child[v]

    dp_l = dp[l]
    dp_r = dp[r]

    max_t = min(k, sub_size[v])
    cur = [infinite] * (max_t + 1)

    cur[1] = entropy(sub_ones[v], sub_size[v])

    max_l = min(len(dp_l) - 1, k)
    max_r = min(len(dp_r) - 1, k)

    for a in range(1, max_l + 1):
        if dp_l[a] >= infinite:
            continue
        bmax = min(max_r, max_t - a)
        for b in range(1, bmax + 1):
            val = dp_l[a] + dp_r[b]
            t = a + b
            if val < cur[t]:
                cur[t] = val

    dp[v] = cur

root = N
print(dp[root][k])