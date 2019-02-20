from random import sample, random, randint
from numpy.random import binomial as bin
from matplotlib import pyplot as plt


class one_plus_lambda_comma_lambda:
    def __init__(self, lam, f, n, x_0=None):
        self.f = f
        self.lam = lam
        self.n = n
        if x_0 is not None:
            self.x = x_0
        else:
            self.x = [randint(0, 1) for _ in range(n)]
        self.cur_f = self.f(self.x)

    def mut(self, x, ell):
        y = x.copy()
        for i in sample(range(len(x)), ell):
            y[i] = 1 - x[i]
        return y

    def cross(self, x, x_dash):
        y = x.copy()
        for i in range(len(x)):
            if randint(1, self.lam) > 1:
                y[i] = x_dash[i]
        return y

    def mutation_phase(self):
        ell = bin(self.n, self.lam/self.n)
        x_dash = self.mut(self.x, ell)
        f_dash = self.f(x_dash)
        for i in range(self.lam - 1):
            x_ddash = self.mut(self.x, ell)
            f_ddash = self.f(x_ddash)
            if f_ddash > f_dash:
                f_dash = f_ddash
                x_dash = x_ddash
        return x_dash

    def run(self):
        counters = {'iters' : 0}
        while self.f(self.x) < self.n:
            x_dash = self.mutation_phase()
            # crossover
            y = self.cross(self.x, x_dash)
            f_y = self.f(y)
            for i in range(self.lam - 1):
                y_dash = self.cross(self.x, x_dash)
                f_y_dash = self.f(y_dash)
                if f_y_dash > f_y:
                    f_y = f_y_dash
                    y = y_dash
            # selection
            if self.cur_f <= f_y:
                self.cur_f = f_y
                self.x = y
            counters['iters'] = counters['iters'] + 1
            if counters['iters'] % 10 == 0:
                print(counters['iters'] % 10, ':', self.cur_f)
        return counters

def leading_ones(x):
    for i in range(len(x)):
        if x[i] == 0:
            return i
    return i + 1


n = 100
runs = 100
res = dict()

for lam in 1, 10, 20, 50, 90, 100:
    res[lam] = [0] * n
    for i in range(n):
        algo = one_plus_lambda_comma_lambda(lam, leading_ones, n, [1] * i + [0] * (n - i))
        res[lam][i] = sum(algo.mutation_phase()[i] == 1 for _ in range(runs))

    plt.plot(range(n), res[lam], 'bo')
    plt.show()



