import numpy as np
import cv2


class LaneImageFactory:

    def __init__(self, image_width, image_height):
        self.image_width = image_width
        self.image_height = image_height
        self.plot_y_left = np.linspace(0, image_height - 1, image_height)
        self.plot_y_right = np.flip(self.plot_y_left, 0)

        self.deg, self.polynomial = self._get_polynomial()

    @staticmethod
    def _get_polynomial():
        deg = 2
        return deg, lambda p, x: p[0] * x ** 2 + p[1] * x + p[2]

    def _calculate_plot_x(self, line_points, plot_y):
        y_coordinates, x_coordinates = line_points
        polynomial_coefficients = np.polyfit(y_coordinates, x_coordinates, self.deg)

        plot_x = self.polynomial(polynomial_coefficients, plot_y)
        return plot_x.astype(int)

    def create(self, left_line_points, right_line_points):
        plot_x_left = self._calculate_plot_x(left_line_points, self.plot_y_left)
        plot_x_right = self._calculate_plot_x(right_line_points, self.plot_y_right)

        left = np.stack([plot_x_left, self.plot_y_left]).T
        right = np.stack([plot_x_right, self.plot_y_right]).T

        total = np.concatenate([left, right]).astype(np.int32)

        image = np.zeros((self.image_height, self.image_width, 3), dtype=np.uint8)
        cv2.fillPoly(image, [total], (0, 255, 0))

        return image
