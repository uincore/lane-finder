import numpy as np
import cv2
import matplotlib.pyplot as plt


class PerspectiveTransformationOperation:

    def __init__(self, image_width, image_height, perspective_distance):
        transformation_parameters = self._get_transformation_parameters(image_width, image_height, perspective_distance)
        self.image_size = (image_width, image_height)
        self.M_forward, self.M_back = transformation_parameters

    def _get_transformation_parameters(self, image_width, image_height, perspective_distance):
        max_distance = 250

        src = self._get_source_points(image_width, image_height, perspective_distance, max_distance)
        dst = self._get_destination_points(image_width, image_height)

        M_forward = cv2.getPerspectiveTransform(src, dst)
        M_back = cv2.getPerspectiveTransform(dst, src)

        return M_forward, M_back

    @staticmethod
    def _get_source_points(image_width, image_height, perspective_distance, max_distance):

        perspective_difference = ((image_width / 2) / perspective_distance) * max_distance

        src_points = [[0, image_height],
                      [perspective_difference, image_height - max_distance],
                      [image_width - perspective_difference, image_height - max_distance],
                      [image_width, image_height]]

        return np.float32(src_points)

    @staticmethod
    def _get_destination_points(image_width, image_height):
        dst_points = [[0, image_height],
                      [0, 0],
                      [image_width, 0],
                      [image_width, image_height]]

        return np.float32(dst_points)

    def apply(self, image, to_bird_view=True):
        M = self.M_forward if to_bird_view else self.M_back

        return cv2.warpPerspective(image, M, self.image_size, flags=cv2.INTER_LINEAR)
