import numpy as np
import cv2


class PerspectiveTransformationOperation:

    def __init__(self, image_width, image_height, perspective_distance, min_distance, max_distance):
        self.image_size = (image_width, image_height)
        self.min_distance = min_distance
        self.max_distance = max_distance

        self.perspective_distance = None
        self.transformation_parameters = None
        self.M_forward = None
        self.M_back = None

        self.update_perspective_distance(perspective_distance)

    def _get_transform_parameters(self, image_size, perspective_distance):

        src = self._get_source_points(image_size, perspective_distance, self.min_distance, self.max_distance)
        dst = self._get_destination_points(image_size)

        M_forward = cv2.getPerspectiveTransform(src, dst)
        M_back = cv2.getPerspectiveTransform(dst, src)

        return M_forward, M_back

    @staticmethod
    def _get_source_points(image_size, perspective_distance, min_distance, max_distance):
        image_width, image_height = image_size

        perspective_difference = ((image_width / 2) / perspective_distance) * max_distance

        src_points = [[0, image_height - min_distance],
                      [perspective_difference, image_height - max_distance],
                      [image_width - perspective_difference, image_height - max_distance],
                      [image_width, image_height - min_distance]]

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

    def update_perspective_distance(self, perspective_distance):
        # TODO: set threshold
        self.perspective_distance = perspective_distance
        self.M_forward, self.M_back = self._get_transform_parameters(self.image_size, perspective_distance)
