import numpy as np
import cv2
from lane.lane_line import LaneLine

class Lane:

    def __init__(self, line_factory):
        self.left_line = None
        self.right_line = None

        self.lane_width = 0
        self.curvature = 0
        self.lane_center_distance = 0

        self.line_factory = line_factory

    def _initialize(self, bw_image):
        left_line_x, right_line_x = self._get_lane_lines_start_points(bw_image)
        self.left_line = LaneLine(left_line_x, self.line_factory)
        self.right_line = LaneLine(right_line_x, self.line_factory)

    def draw(self, bw_image):
        if self.left_line is None and self.right_line is None:
            self._initialize(bw_image)

        left_line = self.left_line.detect(bw_image)
        right_line = self.right_line.detect(bw_image)

        return self._draw_lane(bw_image.shape, left_line, right_line)

    def _draw_lane(self, image_shape, left_line, right_line):
        r = np.flip(right_line, 0)
        total = np.concatenate([left_line, r]).astype(np.int32)

        image = np.zeros((image_shape[0], image_shape[1], 3), dtype=np.uint8)
        cv2.fillPoly(image, [total], (0, 255, 0))

        return image

    @staticmethod
    def _get_lane_lines_start_points(bw_image):
        image_height, image_width = bw_image.shape
        image_center = image_width // 2

        image_bottom_half = bw_image[image_height // 2:, :]
        histogram = np.sum(image_bottom_half, axis=0)

        left_line_x = np.argmax(histogram[:image_center])
        right_line_x = np.argmax(histogram[image_center:]) + image_center

        return left_line_x, right_line_x
