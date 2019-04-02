from random import sample, random, randint
from numpy.random import binomial as bin
from numpy import array, where
from multiprocessing import Pool
from matplotlib import pyplot as plt
from sys import argv
from time import time


class OnePlusLambdaCommaLambda:
    def __init__(self, lam_mut, lam_cross, f, n, x_0=None):
        self.f = f
        self.lam_mut = lam_mut
        self.lam_cross = lam_cross
        self.n = n
        if x_0 is not None:
            self.x = x_0
        else:
            self.x = array([randint(0, 1) for _ in range(n)])
        self.cur_f = self.f(self.x)
        self.offspring = None
        self.x_dash = None
        self.y = None

    def mut(self, ell):
        # write a mutant of self.x into self.offspring
        self.offspring = self.x.copy()
        for i in sample(range(self.n), ell):
            self.offspring[i] = 1 - self.offspring[i]

    def cross(self):
        # creating one crossover offspring
        self.offspring = self.x.copy()
        for i in range(self.n):
            if randint(1, self.lam_cross) == 1:
                self.offspring[i] = self.x_dash[i]

    def mutation_phase(self):
        # creating lambda_1 mutants and choosing the best of them as x'
        ell = bin(self.n, self.lam_mut/self.n)
        self.mut(ell)
        f_dash = self.f(self.offspring)
        self.x_dash = self.offspring
        for _ in range(self.lam_mut - 1):
            self.mut(ell)
            f = self.f(self.offspring)
            if f > f_dash:
                f_dash = f
                self.x_dash = self.offspring

    def crossover_phase(self):
        self.cross()
        self.y = self.offspring
        f_y = self.f(self.offspring)
        for i in range(self.lam_cross - 1):
            self.cross()
            f = self.f(self.offspring)
            if f > f_y:
                f_y = f
                self.y = self.offspring
        return f_y

    def run(self):
        # counters = {'iters': 0}  # for the case we need other information to track
        iters = 0
        while self.f(self.x) < self.n:
            # mutation
            self.mutation_phase()
            # crossover
            f_y = self.crossover_phase()
            # print(y)
            # selection
            if self.cur_f <= f_y:
                self.cur_f = f_y
                self.x = self.y
            # if iters % 10 == 0:
            #     print(iters, ':', self.cur_f)
            #     print(self.x)
            #     print(x_dash)
            #     print(y)
            # counters['iters'] = counters['iters'] + 1
            iters += 1
        # print(counters['iters'])
        return iters

# Bad implementation
# def leading_ones(x):
#     for i in range(len(x)):
#         if x[i] == 0:
#             return i
#     return len(x)


# def leading_ones(x):
#     try:
#         return x.index(0)
#     except ValueError:
#         return len(x)

def leading_ones(x):
    try:
        return where(x == 0)[0][0]
    except IndexError:
        return len(x)


# we decided to make experiments for n=512. We are interested in lambda=1, 2, 4, ... ,256 (powers of two).
# also try the same for the mutation lambda that is half of the crossover lambda (so lambda_mut = 1, 2, ..., 128).

def run_thread(thread_number):
    n = 512
    runs = 8

    with open('one-plus-lambda-lambda-{}.out'.format(thread_number), 'w') as f:
        # for lam in [2 ** k for k in range(9)]:
        #     f.write('lambda={}\n'.format(lam))
        #     for _ in range(runs):
        #         f.write('{} '.format(OnePlusLambdaCommaLambda(lam, lam, leading_ones, n).run()['iters']))
        #         f.flush()
        #     f.write('\n')

        # for lam in [2 ** k for k in range(8)]:
        for lam in [2 ** k for k in range(8, 9)]:
            f.write('lambda_mut={} lambda_cross={}\n'.format(lam, 2 * lam))
            f.flush()
            for _ in range(runs):
                f.write('{} '.format(OnePlusLambdaCommaLambda(lam, lam * 2, leading_ones, n).run()))
                f.flush()
            f.write('\n')


with Pool(4) as pool:
    pool.map(run_thread, list(range(5, 9)))

# test of the usual array copy

# a = [1] * 256 + [0] * 256
# n = 2 ** 15
#
# t_1 = time()
# for i in range(n):
#     leading_ones(a)
# t_2 = time() - t_1
# print("Built-in index:\t{} sec".format(t_2))
#
# a = array(a)
# t_1 = time()
# for i in range(n):
#     leading_ones_np(a)
# t_2 = time() - t_1
# print("NumPy index:\t{} sec".format(t_2))