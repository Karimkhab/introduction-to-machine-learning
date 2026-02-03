import sys
from collections import defaultdict, deque

input = sys.stdin.readline

n, k = map(int, input().split())
cats = list(map(int, input().split()))

if k == 0:
    print(0)
    sys.exit()

blocks = deque()
freq = defaultdict(int)

cur_len = 0
best = 0

last = None
run = 0

for x in cats:
    if x == last:
        run += 1
    else:
        if last is not None:
            blocks.append((last, run))
            cur_len += run
            freq[last] += 1

            while len(freq) > k:
                lb, lc = blocks.popleft()
                cur_len -= lc
                freq[lb] -= 1
                if freq[lb] == 0:
                    del freq[lb]

            if cur_len > best:
                best = cur_len

        last = x
        run = 1

if last is not None:
    blocks.append((last, run))
    cur_len += run
    freq[last] += 1

    while len(freq) > k:
        lb, lc = blocks.popleft()
        cur_len -= lc
        freq[lb] -= 1
        if freq[lb] == 0:
            del freq[lb]

    if cur_len > best:
        best = cur_len

print(best)