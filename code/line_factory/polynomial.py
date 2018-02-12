from math import log


class Polynomial:

    @staticmethod
    def deg():
        return 2

    @staticmethod
    def compute(p, y):
        return p[0] * y ** 2 + p[1] * y + p[2]

    @staticmethod
    def radius(p, y0):
        return ((1 + (2 * p[0] * y0 + p[1]) ** 2) ** (3 / 2)) / abs(2 * p[0])

    @staticmethod
    def get_tangent_fn(p, x0, y0):
        m = 2 * p[0] * y0 + p[1]
        return lambda y: m * (y - y0) + x0

    @staticmethod
    def get_normal_fn(p, x0, y0):
        m = -1 / (2 * p[0] * y0 + p[1])
        return lambda y: m * (y - y0) + x0

    @staticmethod
    def center(p, x0, y0, radius):
        m = - 1 / (2 * p[0] * y0 + p[1])
        y = y0 - radius * (1 / (1 + m ** 2) ** 0.5)
        x = m * (y - y0) + x0
        return x, y

    @staticmethod
    def distance(p, y_min, y_max):
        def eval_fn(y):
            u = 2 * p[0] * y + p[1]
            s = (u ** 2 + 1) ** 0.5
            return u * s + log(abs(u + s))

        return (1 / (4 * p[0])) * (eval_fn(y_max) - eval_fn(y_min))
