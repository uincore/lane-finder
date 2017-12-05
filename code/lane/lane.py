import numpy as np
import cv2
from lane.lane_line import LaneLine
from lane.drawing import Drawing


class Lane:

    def __init__(self, line_factory):
        self.left_line = None
        self.right_line = None

        self.lane_width = 0
        self.curvature = 0
        self.lane_center_distance = 0

        self.line_factory = line_factory
        self.lane_mask_color = (0, 255, 0)

    def _initialize(self, bw_image):
        left_line_x, right_line_x = self._get_lane_lines_start_points(bw_image)
        self.left_line = LaneLine(left_line_x, self.line_factory)
        self.right_line = LaneLine(right_line_x, self.line_factory)

    def draw(self, bw_image):
        if self.left_line is None and self.right_line is None:
            self._initialize(bw_image)

        left_line = self.left_line.detect(bw_image)
        right_line = self.right_line.detect(bw_image)

        output_shape = (bw_image.shape[0], bw_image.shape[1], 3)

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
