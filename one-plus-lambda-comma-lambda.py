from random import sample, random, randint
from numpy.random import binomial as bin
from matplotlib import pyplot as plt
from sys import argv


class OnePlusLambdaCommaLambda:
    def __init__(self, lam_mut, lam_cross, f, n, x_0=None):
        self.f = f
        self.lam_mut = lam_mut
        self.lam_cross = lam_cross
        self.n = n
        if x_0 is not None:
            self.x = x_0
        else:
            self.x = [randint(0, 1) for _ in range(n)]
        self.cur_f = self.f(self.x)

    def mut(self, x, ell):
        # creating one mutant after the mutation strength ell is chosen
        y = x.copy()
        for i in sample(range(len(x)), ell):
            y[i] = 1 - x[i]
        return y

    def cross(self, x, x_dash):
        # creating one crossover offspring
        y = x.copy()
        for i in range(len(x)):
            if randint(1, self.lam_cross) == 1:
                y[i] = x_dash[i]
        return y

    def mutation_phase(self):
        # creating lambda_1 mutants and choosing the best of them as x'
        ell = bin(self.n, self.lam_mut/self.n)
        x_dash = self.mut(self.x, ell)
        f_dash = self.f(x_dash)
        for _ in range(self.lam_mut - 1):
            x_ddash = self.mut(self.x, ell)
            f_ddash = self.f(x_ddash)
            if f_ddash > f_dash:
                f_dash = f_ddash
                x_dash = x_ddash
        return x_dash

    def crossover_phase(self, x_dash):
        y = self.cross(self.x, x_dash)
        f_y = self.f(y)
        for i in range(self.lam_cross - 1):
            y_dash = self.cross(self.x, x_dash)
            f_y_dash = self.f(y_dash)
            if f_y_dash > f_y:
                f_y = f_y_dash
                y = y_dash
        return y, f_y

    def run(self):
        counters = {'iters': 0}  # for the case we need other information to track
        while self.f(self.x) < self.n:
            # mutation
            x_dash = self.mutation_phase()
            # print(x_dash)
            # crossover
            y, f_y = self.crossover_phase(x_dash)
            # print(y)
            # selection
            if self.cur_f <= f_y:
                self.cur_f = f_y
                self.x = y
            # if counters['iters'] % self.n == 0:
            #     print(counters['iters'], ':', self.cur_f)
            #     print(self.x)
            #     print(x_dash)
            #     print(y)
            counters['iters'] = counters['iters'] + 1
        # print(counters['iters'])
        return counters


def leading_ones(x):
    for i in range(len(x)):
        if x[i] == 0:
            return i
    return len(x)


# we decided to make experiments for n=512. We are interested in lambda=1, 2, 4, ... ,256 (powers of two).
# also try the same for the mutation lambda that is half of the crossover lambda (so lambda_mut = 1, 2, ..., 128).

n = 512
runs = 128
if len(argv) < 2:
    thread_number = 0
else:
    thread_number = argv[1]


with open('one-plus-lambda-lambda-{}.out'.format(thread_number), 'w') as f:
    for lam in [2 ** k for k in range(9)]:
        f.write('lambda={}\n'.format(lam))
        for _ in range(runs):
            f.write('{} '.format(OnePlusLambdaCommaLambda(lam, lam, leading_ones, n).run()['iters']))
            f.flush()
        f.write('\n')

    for lam in [2 ** k for k in range(8)]:
        f.write('lambda_mut={} lambda_cross={}\n'.format(lam, 2 * lam))
        for _ in range(runs):
            f.write('{} '.format(OnePlusLambdaCommaLambda(lam, lam * 2, leading_ones, n).run()['iters']))
            f.flush()
        f.write('\n')




