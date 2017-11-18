import numpy as np
from image_operations.drawing.lane_line import LaneLine
from image_operations.drawing.lane_image_factory import LaneImageFactory


class DrawLaneOperation:

    def __init__(self, image_width, image_height):
        self.image_height, self.image_width = image_height, image_width
        self.image_center = self.image_width // 2

        self.left_lane = None
        self.right_lane = None
        self.lane_image_factory = LaneImageFactory(image_width, image_height)

    def execute(self, bw_image):
        self._validate_image(bw_image)

        if self.left_lane is None or self.right_lane is None:
            self._initialize_lanes(bw_image)

        nonzero_y, nonzero_x = bw_image.nonzero()
        nonzero_indexes_x, nonzero_indexes_y = np.array(nonzero_x), np.array(nonzero_y)

        left_y, left_x = self.left_lane.detect(nonzero_indexes_x, nonzero_indexes_y)
        right_y, right_x = self.right_lane.detect(nonzero_indexes_x, nonzero_indexes_y)

        return self.lane_image_factory.create((left_y, left_x), (right_y, right_x))

    def _validate_image(self, bw_image):
        expected_shape = (self.image_height, self.image_width)
        assert expected_shape == bw_image.shape, \
            "Input image expected to have {} shape, but was {}".format(expected_shape, bw_image.shape)

    def _initialize_lanes(self, bw_image):
        left_lane_start_x, right_lane_start_x = self._find_lane_lines_start_points(bw_image)

        self.left_lane = LaneLine(left_lane_start_x, self.image_height)
        self.right_lane = LaneLine(right_lane_start_x, self.image_height)

    def _find_lane_lines_start_points(self, bw_image):
        image_bottom_half = bw_image[self.image_height // 2:, :]
        histogram = np.sum(image_bottom_half, axis=0)

        left_lane_x = np.argmax(histogram[:self.image_center])
        right_lane_x = np.argmax(histogram[self.image_center:]) + self.image_center

        return left_lane_x, right_lane_x
