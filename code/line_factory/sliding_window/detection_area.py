import numpy as np


class DetectionArea:

    def __init__(self, start_x, line_points, window_shape):
        percents_threshold_max = 0.2
        pixels_threshold_min = 50

        self.y, self.x = line_points

        x_count = len(self.x)
        pixels_threshold_max = window_shape[0] * window_shape[1] * percents_threshold_max

        self.area_is_valid = pixels_threshold_min < x_count < pixels_threshold_max
        self.new_x = np.int(np.mean(self.x)) if self.area_is_valid else start_x

    @property
    def line_points_x(self):
        return self.x

    @property
    def line_points_y(self):
        return self.y

    @property
    def center_x(self):
        return self.new_x

    @property
    def is_valid(self):
        # TODO: set to false for invalid points distribution
        return self.area_is_valid
