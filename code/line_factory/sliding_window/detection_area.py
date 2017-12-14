import numpy as np


class DetectionArea:

    def __init__(self, start_x, line_points, pixels_threshold_min=50, pixels_threshold_max=3000):
        self.start_x = start_x
        self.y, self.x = line_points
        self.x_count = len(self.x)
        self.pixels_threshold_min = pixels_threshold_min
        self.pixels_threshold_max = pixels_threshold_max
        self.new_x = self._get_new_x()
        self.area_is_valid = self.x_count > 10

    def _get_new_x(self):
        if self.pixels_threshold_min < self.x_count < self.pixels_threshold_max:
            return np.int(np.mean(self.x))

        return self.start_x

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
