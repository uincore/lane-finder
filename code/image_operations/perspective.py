import numpy as np


class Perspective():

    def __init__(self, image_width, image_height, max_distance, vp_distance, ground_line_meters_per_pixel):

        self.source_im_size = (image_width, image_height)
        self.x_min_max = (0, image_width)
        self.y_min_max = (image_height - max_distance, image_height)

        self.max_dist = max_distance

        self.vanishing_point_distance = None
        self.perspective_difference = None
        self.destination_im_size = None

        self.update_vanishing_point_distance(vp_distance)

        self.meters_per_pixel = ground_line_meters_per_pixel

    @property
    def source_image_size(self):
        return self.source_im_size

    @property
    def source_image_points(self):
        x_min, x_max = self.x_min_max
        y_min, y_max = self.y_min_max

        src_points = [[x_min, y_max],
                      [self.perspective_difference, y_min],
                      [x_max - self.perspective_difference, y_min],
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

    def update_vanishing_point_distance(self, vp_distance):
        assert self.max_dist < vp_distance, "max distance can't greater than lane vanishing point distance"

        image_width = self.source_im_size[0]

        self.vanishing_point_distance = vp_distance
        self.perspective_difference = (image_width * self.max_dist) / (2 * vp_distance)

        destination_image_h = self._calculate_destination_image_height(vp_distance, self.max_dist)
        self.destination_im_size = (image_width, destination_image_h)

    def to_meters(self, pixels):
        return self.meters_per_pixel * pixels

    @staticmethod
    def _calculate_destination_image_height(vp_distance, max_distance):
        return (vp_distance * (2 * vp_distance - max_distance) / (vp_distance - max_distance)) - 2 * vp_distance
