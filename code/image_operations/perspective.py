import numpy as np


class Perspective():

    def __init__(self, image_width, image_height, vp_distance, max_distance, ground_line_meters_per_pixel):

        assert max_distance < vp_distance, "max distance can't greater than lane vanishing point distance"

        self.source_im_size = (image_width, image_height)
        self.x_min_max = (0, image_width)
        self.y_min_max = (image_height - max_distance, image_height)

        self.vanishing_point_distance = vp_distance
        self.max_dist = max_distance

        self.meters_per_pixel = ground_line_meters_per_pixel

        self.image_perspective_width = self._calculate_perspective_width(image_width, vp_distance, max_distance)
        self.destination_im_size = self._calculate_destination_image_size(image_width, vp_distance, max_distance)

    @property
    def source_image_size(self):
        return self.source_im_size

    @property
    def source_image_points(self):
        x_min, x_max = self.x_min_max
        y_min, y_max = self.y_min_max

        src_points = [[x_min, y_max],
                      [self.image_perspective_width, y_min],
                      [x_max - self.image_perspective_width, y_min],
                      [x_max, y_max]]

        return np.float32(src_points)

    @property
    def destination_image_size(self):
        return self.destination_im_size

    @property
    def destination_image_points(self):
        image_width, image_height = self.destination_im_size

        dst_points = [[0, image_height],
                      [0, 0],
                      [image_width, 0],
                      [image_width, image_height]]

        return np.float32(dst_points)

    @property
    def destination_image_meters_pre_pixel_coefficient(self):
        return self.meters_per_pixel

    def update_vanishing_point_distance(self, value):
        self.vanishing_point_distance = value

    @staticmethod
    def _calculate_perspective_width(image_width, vp_distance, max_distance):
        return (image_width / vp_distance) * (vp_distance - max_distance)

    @staticmethod
    def _calculate_destination_image_size(image_width, vp_distance, max_distance):
        x_width = image_width
        y_distance = (vp_distance * (2 * vp_distance - max_distance) / (vp_distance - max_distance)) - 2 * vp_distance

        return x_width, y_distance
