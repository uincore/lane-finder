import numpy as np


class TransformationParameters:
    """

    """

    def __init__(self, im_width, im_height, vp_distance, ground_line_meters_per_pixel, max_distance_coefficient):
        """
        :param im_width: original image width
        :param im_height: original image height
        :param vp_distance: lane vanishing point distance from the bottom of the image
        :param ground_line_meters_per_pixel: meters/pixel on x = 0 line
        :param max_distance_coefficient: lane max detection distance coefficient. Max distance in points will be
                                        calculated as max_distance = vp_distance * max_distance_coefficient.
                                        Should be greater than 0 and less then 0.9
        """
        assert 0 < max_distance_coefficient < 0.9, "max_distance_coefficient should be greater than 0 and less then 0.9"

        self.source_image_width = im_width
        self.source_image_height = im_height
        self.source_im_size = (im_width, im_height)

        self.destination_image_width = im_width

        self.meters_per_pixel = ground_line_meters_per_pixel
        self.max_distance_coefficient = max_distance_coefficient

        self.max_distance = 0
        self.vanishing_point_distance = None
        self.perspective_difference = None
        self.destination_im_size = None
        self.update_vanishing_point_distance(vp_distance)

    @property
    def lane_vanishing_point_distance(self):
        return self.vanishing_point_distance

    @property
    def source_image_size(self):
        return self.source_im_size

    @property
    def source_image_points(self):
        x_min, x_max = 0, self.source_image_width
        y_min, y_max = self.source_image_height - self.max_distance, self.source_image_height

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
        self.max_distance = vp_distance * self.max_distance_coefficient

        self.vanishing_point_distance = vp_distance
        self.perspective_difference = (self.source_image_width * self.max_distance) / (2 * vp_distance)

        destination_image_height = self._calculate_destination_image_height(vp_distance, self.max_distance)
        self.destination_im_size = (self.destination_image_width, destination_image_height)

    def to_meters(self, pixels):
        return self.meters_per_pixel * pixels

    @staticmethod
    def _calculate_destination_image_height(vp_distance, max_distance):
        height = (vp_distance * (2 * vp_distance - max_distance) / (vp_distance - max_distance)) - 2 * vp_distance
        return int(height)
