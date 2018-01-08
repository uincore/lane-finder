import numpy as np
import cv2


class PerspectiveTransformationOperation:

    def __init__(self, image_width, image_height, vanishing_point_distance, max_distance):

        self.image_size = (image_width, image_height)
        self.x_min_max = (0, image_width)
        self.y_min_max = (image_height - max_distance, image_height)

        self.lane_vanishing_point_distance = vanishing_point_distance
        self.max_dist = max_distance

        self.transformation_parameters = None

        self.M_forward, self.M_back = self._get_transform_parameters(self.lane_vanishing_point_distance)

    @property
    def vanishing_point_distance(self):
        return self.lane_vanishing_point_distance

    def _get_transform_parameters(self, vp_distance):

        src = self._get_source_points(vp_distance, self.max_dist, self.x_min_max, self.y_min_max)
        dst = self._get_destination_points(self.image_size)

        M_forward = cv2.getPerspectiveTransform(src, dst)
        M_back = cv2.getPerspectiveTransform(dst, src)

        return M_forward, M_back

    @staticmethod
    def _get_source_points(vp_distance, max_distance, x_min_max, y_min_max):

        x_min, x_max = x_min_max
        y_min, y_max = y_min_max

        perspective_difference = (x_max * max_distance) / (2 * vp_distance)

        src_points = [[x_min, y_max],
                      [perspective_difference, y_min],
                      [x_max - perspective_difference, y_min],
                      [x_max, y_max]]

        return np.float32(src_points)

    @staticmethod
    def _get_destination_points(image_size):
        image_width, image_height = image_size

        dst_points = [[0, image_height],
                      [0, 0],
                      [image_width, 0],
                      [image_width, image_height]]

        return np.float32(dst_points)

    def execute(self, image, to_bird_view=True):
        M = self.M_forward if to_bird_view else self.M_back

        return cv2.warpPerspective(image, M, self.image_size, flags=cv2.INTER_LINEAR)

    def adjust_vanishing_point_distance(self, update_direction=0):
        adjust_step = 2
        if update_direction > 0:
            self.lane_vanishing_point_distance += adjust_step
        if update_direction < 0:
            self.lane_vanishing_point_distance -= adjust_step

        if update_direction != 0:
            self.M_forward, self.M_back = self._get_transform_parameters(self.lane_vanishing_point_distance)
