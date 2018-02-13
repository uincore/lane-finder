from line_factory.polynomial import Polynomial


class CurvedLine:

    def __init__(self, line_is_valid, coordinates, polynomial_coefficients):
        self.line_is_valid = line_is_valid
        self.line_coordinates = coordinates
        self.polynomial_coefficients = polynomial_coefficients

    @property
    def is_valid(self):
        return self.line_is_valid

    @property
    def coordinates(self):
        return self.line_coordinates

    @property
    def radius(self):
        if self.is_valid:
            y = len(self.line_coordinates)
            return Polynomial.radius(self.polynomial_coefficients, y)

        return 0
