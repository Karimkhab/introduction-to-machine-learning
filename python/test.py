import sys


def main():
    """
    Пример ввода и вывода числа n, где -10^9 < n < 10^9:
    n = int(input())
    print(n)
    """
    n = int(input())
    ans = float('inf')

    for r in range(1, int(n**0.5) + 1):
        x = n % r
        if abs(r - 2 * x) <= 1:
            mx = (n + r - 1) // r
            ans = min(ans, abs(r - mx))

    print(ans)

if __name__ == '__main__':
    main()
