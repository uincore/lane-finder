import numpy as np
from lane.lane_line import LaneLine
from lane.drawing import Drawing


class Lane:

    def __init__(self, curved_line_factory):
        self.left_line = None
        self.right_line = None

        self.curved_line_factory = curved_line_factory
        self.lane_mask_color = (0, 255, 0)

        self.lane_is_lost = False
        self.lane_width = 0

    @property
    def line_left(self):
        return self.left_line

    @property
    def line_right(self):
        return self.right_line

    @property
    def is_lost(self):
        return self.lane_is_lost

    def _initialize(self, bw_image):
        left_line_x, right_line_x = self._get_lane_lines_start_points(bw_image)
        self.lane_width = right_line_x - left_line_x

        self.left_line = LaneLine(left_line_x, self.curved_line_factory)
        self.right_line = LaneLine(right_line_x, self.curved_line_factory)

    def create_mask_image(self, bw_image):
        if self.left_line is None and self.right_line is None:
            self._initialize(bw_image)

        self.left_line.update(bw_image)
        self.right_line.update(bw_image)

        output_shape = (bw_image.shape[0], bw_image.shape[1], 3)

        self.lane_is_lost = not self._validate(self.left_line, self.right_line, self.lane_width)
        if self.lane_is_lost:
            self.left_line = None
            self.right_line = None
            return np.zeros(output_shape, dtype=np.uint8)

        if(self.left_line.is_valid == self.right_line.is_valid):
            self.lane_width = self.right_line.x - self.left_line.x

        left_line = self._get_line_coordinates(self.left_line)
        right_line = self._get_line_coordinates(self.right_line)
        return Drawing.create_mask_image(output_shape, left_line, right_line, self.lane_mask_color)

    @staticmethod
    def _get_lane_lines_start_points(bw_image):
        image_height, image_width = bw_image.shape
        image_center = image_width // 2

        image_bottom_half = bw_image[image_height // 2:, :]
        histogram = np.sum(image_bottom_half, axis=0)

        left_line_x = np.argmax(histogram[:image_center])
        right_line_x = np.argmax(histogram[image_center:]) + image_center

        return left_line_x, right_line_x

    def _validate(self, line1, line2, lane_width):
        lines_are_valid = line1.is_valid == line2.is_valid is True
        one_of_lines_can_be_predicted = line1.is_valid != line2.is_valid and lane_width > 700
        lines_are_parallel_fn = lambda x, y: np.std((x.line_coordinates - y.line_coordinates)[:, 0]) < 100

        return (lines_are_valid and lines_are_parallel_fn(line1, line2)) or one_of_lines_can_be_predicted

    def _get_line_coordinates(self, line):
        if line.is_valid:
            return line.line_coordinates

        return self._get_opposite_line_coordinates(line)

    def _get_opposite_line_coordinates(self, line):
        shift = [[self.lane_width, 0]] * 720
        if line is self.right_line:
            return self.left_line.line_coordinates + shift
        if line is self.left_line:
            return self.right_line.line_coordinates - shift

        raise Exception("Invalid line object")