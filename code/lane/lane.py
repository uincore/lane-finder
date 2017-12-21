import numpy as np
from lane.lane_line import LaneLine


class Lane:

    def __init__(self, curved_line_factory):
        self.left_line = None
        self.right_line = None
        self.lane_width = 0

        self.curved_line_factory = curved_line_factory

    @property
    def line_left(self):
        return self.left_line

    @property
    def line_right(self):
        return self.right_line

    @property
    def width(self):
        return self.lane_width

    def update(self, bw_image):
        if self.left_line is None and self.right_line is None:
            self._initialize(bw_image)

        self.left_line.update(bw_image)
        self.right_line.update(bw_image)

        self.lane_width = self._get_lane_width(self.left_line, self.right_line)

    def reset(self):
        self.left_line = None
        self.right_line = None
        self.lane_width = 0

    def _initialize(self, bw_image):
        left_line_x, right_line_x = self._get_lane_lines_start_points(bw_image)
        self.lane_width = right_line_x - left_line_x

        self.left_line = LaneLine(left_line_x, self.curved_line_factory)
        self.right_line = LaneLine(right_line_x, self.curved_line_factory)

    @staticmethod
    def _get_lane_lines_start_points(bw_image):
        image_height, image_width = bw_image.shape
        image_center = image_width // 2

        image_bottom_half = bw_image[image_height // 2:, :]
        histogram = np.sum(image_bottom_half, axis=0)

        left_line_x = np.argmax(histogram[:image_center])
        right_line_x = np.argmax(histogram[image_center:]) + image_center

        return left_line_x, right_line_x

    def _get_lane_width(self, left_line, right_line):
        if left_line.is_valid == right_line.is_valid is True:
            return right_line.x - left_line.x
        if left_line.is_valid != right_line.is_valid:
            return self.lane_width

        return 0
