import sys
import math

data = sys.stdin.buffer.read().split()
it = iter(data)

n1 = int(next(it))
A = [(float(next(it)), float(next(it))) for _ in range(n1)]

n2 = int(next(it))
B = [(float(next(it)), float(next(it))) for _ in range(n2)]

Px = float(next(it))
Py = float(next(it))

PI = math.pi
TWO_PI = 2.0 * math.pi

# Предварительно считаем для каждой точки:
# r  — расстояние до P
# ang — угол вектора (точка - P) в [0, 2π)
A_r, A_ang = [], []
B_r, B_ang = [], []
min_r = float("inf")

for x, y in A:
    dx, dy = x - Px, y - Py
    r = math.hypot(dx, dy)
    if r == 0.0:
        print(-1)
        sys.exit(0)
    ang = math.atan2(dy, dx)
    if ang < 0.0:
        ang += TWO_PI
    A_r.append(r)
    A_ang.append(ang)
    if r < min_r:
        min_r = r

for x, y in B:
    dx, dy = x - Px, y - Py
    r = math.hypot(dx, dy)
    if r == 0.0:
        print(-1)
        sys.exit(0)
    ang = math.atan2(dy, dx)
    if ang < 0.0:
        ang += TWO_PI
    B_r.append(r)
    B_ang.append(ang)
    if r < min_r:
        min_r = r


def can_with_margin(d, signA, strict0=False):
    """
    signA = +1: класс A должен быть "сверху" (n·(A-P) >= d), класс B "снизу" (n·(B-P) <= -d)
    signA = -1: наоборот.

    strict0=True используется только для d=0:
    возвращаем True, только если есть ненулевой по длине диапазон углов
    (то есть можно сделать строгое разделение, без точек на прямой).
    """
    # Для класса A берём вектор (A-P) если signA=+1, иначе (P-A) = -(A-P) (угол + π)
    shiftA = 0.0 if signA == 1 else PI

    # Для класса B вектор должен быть противоположного знака, т.к. хотим n·(P-B) >= d при signA=+1
    # signB = -signA, значит сдвиг либо 0, либо π
    shiftB = 0.0 if signA == -1 else PI

    # Пересечение на круге храним как 1 или 2 НЕ-оборачивающихся отрезка в [0, 2π]
    candidates = None
    first = True

    total = len(A_r) + len(B_r)
    for i in range(total):
        if i < len(A_r):
            r = A_r[i]
            ang = A_ang[i] + shiftA
        else:
            j = i - len(A_r)
            r = B_r[j]
            ang = B_ang[j] + shiftB

        if ang >= TWO_PI:
            ang -= TWO_PI  # достаточно одного вычитания, сдвиг максимум π

        ratio = d / r
        if ratio > 1.0:
            return False  # невозможно для этой точки

        # Допустимые направления нормали n: |угол(n) - ang| <= arccos(d/r)
        alpha = math.acos(ratio)

        l = ang - alpha
        rr = ang + alpha

        # Приводим концы в [0, 2π), отмечаем wrap (оборачивается через 0)
        if l < 0.0:
            l += TWO_PI
        if rr >= TWO_PI:
            rr -= TWO_PI
        wrap = l > rr

        if first:
            if not wrap:
                candidates = [(l, rr)]
            else:
                candidates = [(l, TWO_PI), (0.0, rr)]
            first = False
            continue

        new_candidates = []
        for L, R in candidates:
            if not wrap:
                NL = max(L, l)
                NR = min(R, rr)
                if NL <= NR:
                    new_candidates.append((NL, NR))
            else:
                # Интервал = [l, 2π) ∪ [0, rr]
                # Кандидат [L, R] не оборачивается, значит он может пересечь только одну из частей.
                if R < l and L > rr:
                    continue  # кандидат целиком в "дыре" (rr, l)
                if L <= rr:
                    NL = L
                    NR = min(R, rr)
                    if NL <= NR:
                        new_candidates.append((NL, NR))
                else:
                    NL = max(L, l)
                    NR = R
                    if NL <= NR:
                        new_candidates.append((NL, NR))

        candidates = new_candidates
        if not candidates:
            return False

    if strict0:
        # Нужно, чтобы остался хоть один отрезок положительной длины
        eps = 1e-15
        for L, R in candidates:
            if R - L > eps:
                return True
        return False

    return True


# Сначала проверим, существует ли вообще строго разделяющая прямая (d=0, но строго)
if not (can_with_margin(0.0, 1, strict0=True) or can_with_margin(0.0, -1, strict0=True)):
    print(-1)
    sys.exit(0)

# Бинарный поиск максимального d
lo, hi = 0.0, min_r
for _ in range(70):  # достаточно для точности 1e-6 с запасом
    mid = (lo + hi) / 2.0
    if can_with_margin(mid, 1) or can_with_margin(mid, -1):
        lo = mid
    else:
        hi = mid

print(f"{lo:.10f}")
