import numpy as np
from lane.drawing import Drawing


class LaneLine:

    def __init__(self, start_x, curved_line_factory):
        self.current_x = start_x
        self.curved_line_factory = curved_line_factory

        self.line = None
        self.detection_area_mask = None

    @property
    def x(self):
        return self.current_x

    @property
    def coordinates(self):
        return self.line.coordinates

    @property
    def is_valid(self):
        return self.line.is_valid

    def update(self, bw_image):
        image = self._apply_line_detection_area_mask(bw_image)
        self.line = self.curved_line_factory.create(image, self.current_x)

        if self.line.is_valid:
            self.current_x = int(self.line.coordinates[700][0])
            self.detection_area_mask = self._create_line_detection_area_mask(self.line.coordinates, image.shape)

    def _apply_line_detection_area_mask(self, bw_image):
        image = np.copy(bw_image)
        if self.detection_area_mask is not None:
            image[self.detection_area_mask == 0] = 0

        return image

    @staticmethod
    def _create_line_detection_area_mask(line, image_shape):
        line_points_count = len(line)
        delta = [[100, 0]] * line_points_count
        left_b = line - delta
        right_b = line + delta

        return Drawing.create_mask_image(image_shape, left_b, right_b, 1)
