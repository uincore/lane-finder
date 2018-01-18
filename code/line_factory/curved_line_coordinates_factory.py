import numpy as np
from line_factory.polynomial import Polynomial


class CurvedLineCoordinatesFactory:
    @staticmethod
    def create(line_points, image_height):
        y_coordinates, x_coordinates = line_points
        polynomial_coefficients = np.polyfit(y_coordinates, x_coordinates, Polynomial.deg())

        plot_y = np.linspace(0, image_height - 1, image_height)
        plot_x = Polynomial.compute(polynomial_coefficients, plot_y)

        return np.stack([plot_x, plot_y]).T, polynomial_coefficients
