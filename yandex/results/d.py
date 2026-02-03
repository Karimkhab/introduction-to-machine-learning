import sys
import math

tokens = sys.stdin.buffer.read().split()
it = iter(tokens)

n1 = int(next(it))
points1 = [(float(next(it)), float(next(it))) for _ in range(n1)]

n2 = int(next(it))
points2 = [(float(next(it)), float(next(it))) for _ in range(n2)]

px = float(next(it))
py = float(next(it))

pi = math.pi
tau = math.tau

cls1 = []
cls2 = []
min_r = float("inf")

for x, y in points1:
    dx, dy = x - px, y - py
    r = math.hypot(dx, dy)
    if r == 0.0:
        print(-1)
        sys.exit(0)
    ang = math.atan2(dy, dx)
    if ang < 0:
        ang += tau
    cls1.append((r, ang))
    if r < min_r:
        min_r = r

for x, y in points2:
    dx, dy = x - px, y - py
    r = math.hypot(dx, dy)
    if r == 0.0:
        print(-1)
        sys.exit(0)
    ang = math.atan2(dy, dx)
    if ang < 0:ang += tau
    cls2.append((r, ang))
    if r < min_r:min_r = r


def possible(d, signA, strict=False):
    shift1 = 0.0 if signA == 1 else pi
    shift2 = pi  if signA == 1 else 0.0

    intervals = [(0.0, tau)]

    def intersect_with(center, r):
        nonlocal intervals

        if d > r:
            return False

        t = d / r
        t = min(t,1.0)
        alpha = math.acos(t)

        left = center - alpha
        right = center + alpha

        if left < 0.0:parts = [(left + tau, tau), (0.0, right)]
        elif right >= tau:parts = [(left, tau), (0.0, right - tau)]
        else:parts = [(left, right)]

        new_intervals = []
        for L, R in intervals:
            for a, b in parts:
                x = max(L, a)
                y = min(R, b)
                if x <= y:new_intervals.append((x, y))

        if not new_intervals:return False

        new_intervals.sort()
        merged = [new_intervals[0]]
        for a, b in new_intervals[1:]:
            L, R = merged[-1]
            if a <= R:merged[-1] = (L, max(R, b))
            else:merged.append((a, b))

        intervals = merged
        return True

    for r, ang in cls1:
        center = ang + shift1
        if center >= tau:
            center -= tau
        if not intersect_with(center, r):return False

    for r, ang in cls2:
        center = ang + shift2
        if center >= tau:
            center -= tau
        if not intersect_with(center, r):return False

    eps = 1e-15
    if strict:return any((R - L) > eps for L, R in intervals)
    return True


if not (possible(0.0, 1, strict=True) or possible(0.0, -1, strict=True)):
    print(-1)
    sys.exit(0)

lo, hi = 0.0, min_r
for _ in range(70):
    mid = (lo + hi) / 2.0
    if possible(mid, 1) or possible(mid, -1):lo = mid
    else:hi = mid

print(round(lo, 10))
