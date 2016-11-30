import math


class ComputeFunction(object):
    c = 16.0
    K = 0.01
    R = 2.0
    beta = 0.1
    # eps: accuracy: $\abs{u-u^*}, u^* = \sum_{0}^{N} \{\dots\}$
    eps = 1e-7
    # time
    limit = 10

    def __init__(self, c=2.0, K=0.01, R=2.0, beta=0.1, eps=1e-7, t=1e-3, limit=10):
        self.c = c
        self.K = K
        self.R = R
        self.beta = beta
        self.eps = eps
        self.t = t
        self.limit = limit

    def function_u(self, theta, t):
        temp = self.beta * self.R * self.R / self.K
        temp_1 = 0
        for k in range(1, self.limit):
            temp_1 += (4 * k + 1) * self.calculate_P_x(2 * k - 2, 0) / (16 * k * k * (2 * k + 1) * (k + 1)) \
                      * (1 - math.exp(-2 * k * (1 + 2 * k) * self.K * t / (self.c * self.R * self.R))) \
                      * self.calculate_P_x(2 * k, math.cos(theta))
        temp *= temp_1
        temp += +self.beta * t / (4 * self.c) + \
                self.beta * self.R * self.R / (4 * self.K) \
                * (1 - math.exp(-2 * self.K * t / (self.c * self.R * self.R))) * math.cos(theta)
        return temp

    def calculate_P_x(self, n, x):
        if (n == 0):
            return 1
        if (n == 1):
            return x
        return ((2 * n - 1) * x * self.calculate_P_x(n - 1, x) - (n - 1) * self.calculate_P_x(n - 2, x)) / n
