import numpy as np


class CurvedLineCoordinatesFactory:

    def __init__(self, image_width, image_height):
        self.image_width = image_width
        self.image_height = image_height
        self.plot_y = np.linspace(0, image_height - 1, image_height)

        self.deg, self.polynomial_fn, self.curvature_fn = self._get_polynomial()

    @staticmethod
    def _get_polynomial():
        deg = 2
        return deg, \
               lambda p, x: p[0] * x ** 2 + p[1] * x + p[2], \
               lambda p, y: ((1 + (2 * p[0] * y + p[1]) ** 2) ** (3 / 2)) / abs(2 * p[0])

    def create(self, line_points):
        y_coordinates, x_coordinates = line_points
        polynomial_coefficients = np.polyfit(y_coordinates, x_coordinates, self.deg)

        plot_x = self.polynomial_fn(polynomial_coefficients, self.plot_y)

        return np.stack([plot_x, self.plot_y]).T

    def get_radius(self, y_coordinates, x_coordinates, y_coefficient, x_coefficient):
        polynomial_coefficients = np.polyfit(y_coordinates * y_coefficient, x_coordinates * x_coefficient, self.deg)
        radius = self.curvature_fn(polynomial_coefficients, self.image_height)
        return radius
