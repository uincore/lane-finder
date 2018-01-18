import numpy as np
from lane.lane_line import LaneLine


class Lane:

    def __init__(self, curved_line_factory, ground_line_meters_per_pixel):
        """
        :param curved_line_factory:
        :param ground_line_meters_per_pixel: meters/pixel on x = 0 line
        """
        self.left_line = None
        self.right_line = None
        self.bottom_lane_width = 0
        self.top_lane_width = 0
        self.lane_radius = 0
        self.curved_line_factory = curved_line_factory
        self.meters_per_pixel = ground_line_meters_per_pixel

        self.lane_image = None

    @property
    def line_left(self):
        return self.left_line

    @property
    def line_right(self):
        return self.right_line

    @property
    def width(self):
        return self.bottom_lane_width

    @property
    def top_width(self):
        return self.top_lane_width

    @property
    def source_image(self):
        return self.lane_image

    @property
    def radius_m(self):
        return self.lane_radius * self.meters_per_pixel

    def update(self, bw_image):
        self.lane_image = bw_image

        if self.left_line is None and self.right_line is None:
            self._initialize(bw_image)

        self.left_line.update(bw_image)
        self.right_line.update(bw_image)

        self.bottom_lane_width, self.top_lane_width = self._get_lane_width(self.left_line, self.right_line)
        self.lane_radius = self._get_lane_radius(self.left_line, self.right_line)

    def reset(self):
        self.left_line = None
        self.right_line = None
        self.bottom_lane_width = 0
        self.lane_image = None

    def _initialize(self, bw_image):
        left_line_x, right_line_x = self._get_lane_lines_start_points(bw_image)
        self.bottom_lane_width = right_line_x - left_line_x

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

    @staticmethod
    def _get_lane_radius(left_line, right_line):
        if left_line.is_valid == right_line.is_valid is True:
            return left_line.radius

            # return (left_line.radius + right_line.radius) / 2

        if left_line.is_valid:
            return left_line.radius
        if right_line.is_valid:
            return right_line.radius

        return 0

    def _get_lane_width(self, left_line, right_line):
        if left_line.is_valid == right_line.is_valid is True:
            return right_line.x_bottom - left_line.x_bottom, right_line.x_top - left_line.x_top

        if left_line.is_valid != right_line.is_valid:
            return self.bottom_lane_width, self.bottom_lane_width

        return 0, 0
