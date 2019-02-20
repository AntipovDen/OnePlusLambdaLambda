from scipy.special import comb
from matplotlib import pyplot as plt


def beta(n, lam, l, j):
    return sum([(1 - comb(n - j, l) / comb(n, l)) ** k * (1 - comb(n - j - 1, l) / comb(n, l)) ** (lam - k - 1) for k in range(lam)])


def upper_beta(n, lam, l, j):
    return lam * (1 - comb(n - j - 1, l) / comb(n, l)) ** (lam - 1)


def lower_beta(n, lam, l, j):
    return lam * (1 - comb(n - j, l) / comb(n, l)) ** (lam - 1)


def inner_sum(n, lam, j):
    return sum([comb(n - j - 2, l) * (lam / n) ** l * (1 - lam / n) ** (n - j - l - 2) * beta(n, lam, l + 2, j) for l in range(n - j - 1)])


def no_better_part(n, lam, i):
    print('i = {}'.format(i))
    return (lam/n) ** 2 * sum([(1 - lam/n) ** j * inner_sum(n, lam, j) for j in range(i + 1)])


def no_better_part_array(n, lam):
    arr = [(lam/n) ** 2 * inner_sum(n, lam, 0)]
    for j in range(1, n):
        arr.append(arr[-1] + (lam/n) ** 2 * (1 - lam/n) ** j * inner_sum(n, lam, j))
    return arr


def better_part(n, lam, i):
    return sum(comb(n, l) * (lam/n) ** l * (1 - lam/n) ** (n - l) * (1 - (1 - comb(n - i - 1, l -1) / comb(n, l)) ** lam) for l in range(1, n - i + 1))


def better_part_array(n, lam):
    return [better_part(n, lam, i) for i in range(n)]

n = 100

for lam in 2, 10, 20, 50, 90:
    assumed_threshold = n / lam * 2
    b = better_part_array(n, lam)
    nb = no_better_part_array(n, lam)
    plt.plot(range(n), nb, 'bo-', label='no better individual')
    plt.plot(range(n), b, 'ro-', label='with better individual')
    plt.plot(range(n), [nb[i] + b[i] for i in range(n)], 'go-', label='total probability')
    plt.plot([assumed_threshold] * 2, [0, b[0] + nb[0]], 'r-')
    plt.title('$\lambda = {}$'.format(lam))
    plt.legend(loc=1)
    plt.xlabel('current fitness')
    plt.show()
