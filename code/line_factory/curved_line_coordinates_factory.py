import numpy as np


class CurvedLineCoordinatesFactory:

    def __init__(self):
        self.deg = 2

    @staticmethod
    def polynomial(p, x):
        return p[0] * x ** 2 + p[1] * x + p[2]

    @staticmethod
    def curvature(p, y):
        return ((1 + (2 * p[0] * y + p[1]) ** 2) ** (3 / 2)) / abs(2 * p[0])

    def create(self, line_points, image_height):
        y_coordinates, x_coordinates = line_points
        polynomial_coefficients = np.polyfit(y_coordinates, x_coordinates, self.deg)

        plot_y = np.linspace(0, image_height - 1, image_height)
        plot_x = self.polynomial(polynomial_coefficients, plot_y)

        return np.stack([plot_x, plot_y]).T

    def get_radius(self, image_height, y_coordinates, x_coordinates, y_coefficient, x_coefficient):
        polynomial_coefficients = np.polyfit(y_coordinates * y_coefficient, x_coordinates * x_coefficient, self.deg)
        radius = self.curvature(polynomial_coefficients, image_height)
        return radius
