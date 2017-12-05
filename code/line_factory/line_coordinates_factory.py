import numpy as np


class CurvedLineCoordinatesFactory:

    def __init__(self, image_width, image_height):
        self.image_width = image_width
        self.image_height = image_height
        self.plot_y = np.linspace(0, image_height - 1, image_height)

        self.deg, self.polynomial = self._get_polynomial()

    @staticmethod
    def _get_polynomial():
        deg = 2
        return deg, lambda p, x: p[0] * x ** 2 + p[1] * x + p[2]

    def create(self, line_points):
        y_coordinates, x_coordinates = line_points
        polynomial_coefficients = np.polyfit(y_coordinates, x_coordinates, self.deg)

        plot_x = self.polynomial(polynomial_coefficients, self.plot_y)
        return np.stack([plot_x, self.plot_y]).T, (plot_x, self.plot_y)
