import numpy as np


class DetectionArea:

    def __init__(self, start_x, line_points, pixels_threshold=50):
        self.start_x = start_x
        self.y, self.x = line_points
        self.x_count = len(self.x)
        self.pixels_threshold = pixels_threshold
        self.new_x = self._get_new_x()

    def _get_new_x(self):
        if self.x_count > self.pixels_threshold:
           return np.int(np.mean(self.x))
        return self.start_x

    @property
    def points_count(self):
        return self.x_count

    @property
    def line_points_x(self):
        return self.x

    @property
    def line_points_y(self):
        return self.y

    @property
    def previous_x(self):
        return self.start_x

    def current_x(self):
        return self.new_x
