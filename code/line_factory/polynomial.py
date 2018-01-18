class Polynomial:

    @staticmethod
    def deg():
        return 2

    @staticmethod
    def compute(p, x):
        return p[0] * x ** 2 + p[1] * x + p[2]

    @staticmethod
    def radius(p, y):
        return ((1 + (2 * p[0] * y + p[1]) ** 2) ** (3 / 2)) / abs(2 * p[0])