class FunctionP:
    def __init__(self):
        self.cache = {}

    def calculate(self, n, x):
        if Value(n, x) in self.cache:
            return self.cache[Value(n, x)]
        if n == 0:
            return 1
        if n == 1:
            return x
        self.cache[Value(n, x)] = ((2 * n - 1) * x * self.calculate(n - 1, x) - (n - 1) * self.calculate(n - 2, x)) / n
        return self.cache[Value(n, x)]


class Value(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return other.x == self.x and other.y == self.y

    def __str__(self):
        return "(%i,%i)" % (self.x, self.y)

    def __hash__(self):
        return hash("%i %i" % (self.x, self.y))
