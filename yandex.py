import sys


def main():
    """
    Пример ввода и вывода числа n, где -10^9 < n < 10^9:
    n = int(input())
    print(n)
    """
    n, costs = int(input()), list(map(int,input().split()))
    X = int(input())
    combo_products = list(map(int,input().split()))
    k, desired_products = int(input()), list(map(int, input().split()))

    not_combo_products = list(set(desired_products) - set(combo_products))

    doubles_no_comb = [desired_products.count(ncp) for ncp in not_combo_products]
    doubles_comb = [desired_products.count(cp) for cp in combo_products]

    max_iterations, opt_comb = max(doubles_comb),  10**10

    opt = sum(costs[not_combo_products[i] - 1] * doubles_no_comb[i] for i in range(len(not_combo_products)))
    for i in range(max_iterations+1):
        opt_comb = min(opt_comb,X*i + sum(costs[combo_products[i]-1]*doubles_comb[i] for i in range(len(doubles_comb))))
        doubles_comb = list(map(lambda x: x-1 if x!=0 else 0, doubles_comb))
    print(opt+opt_comb)

if __name__ == '__main__':
    main()
