import sys
import math


def cross(o, a, b):
    # (a - o) x (b - o)
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def convex_hull(points):
    # Monotonic chain, returns hull in CCW without repeating first point
    points = sorted(set(points))
    if len(points) <= 1:
        return points

    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    return lower[:-1] + upper[:-1]


def dist_point_to_segment(ax, ay, bx, by):
    # distance from origin to segment AB
    dx = bx - ax
    dy = by - ay
    denom = dx * dx + dy * dy
    if denom == 0.0:
        return math.hypot(ax, ay)

    # minimize |A + t(B-A)|^2, t in [0,1]
    t = -(ax * dx + ay * dy) / denom
    if t < 0.0:
        t = 0.0
    elif t > 1.0:
        t = 1.0

    px = ax + t * dx
    py = ay + t * dy
    return math.hypot(px, py)


def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)

    n1 = int(next(it))
    c1 = [(float(next(it)), float(next(it))) for _ in range(n1)]
    n2 = int(next(it))
    c2 = [(float(next(it)), float(next(it))) for _ in range(n2)]
    p0x = float(next(it))
    p0y = float(next(it))

    # Build U = {x - p0 for class1} U {p0 - y for class2}
    U = []
    for x, y in c1:
        U.append((x - p0x, y - p0y))
    for x, y in c2:
        U.append((p0x - x, p0y - y))

    # If any u == (0,0), strict separation impossible (point lies on any line through p0)
    # In that case distance is 0 anyway, but we can early return.
    for ux, uy in U:
        if ux == 0.0 and uy == 0.0:
            print(-1)
            return

    hull = convex_hull(U)
    m = len(hull)
    if m == 0:
        print(-1)
        return
    if m == 1:
        d = math.hypot(hull[0][0], hull[0][1])
    elif m == 2:
        (ax, ay), (bx, by) = hull
        d = dist_point_to_segment(ax, ay, bx, by)
    else:
        d = float('inf')
        for i in range(m):
            ax, ay = hull[i]
            bx, by = hull[(i + 1) % m]
            d = min(d, dist_point_to_segment(ax, ay, bx, by))

    # If distance is ~0, no strictly separating line exists
    eps = 1e-12
    if d <= eps:
        print(-1)
    else:
        # Enough precision for 1e-6 absolute/relative
        print("{:.10f}".format(d))


if __name__ == "__main__":
    solve()
