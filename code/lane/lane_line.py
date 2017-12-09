import numpy as np
from lane.drawing import Drawing


class LaneLine:

    def __init__(self, start_x, line_factory):
        self.start_x = start_x
        self.line_factory = line_factory
        self.detection_area_mask = None
        self.line_points = None

    @property
    def line(self):
        return self.line_points

    def update(self, bw_image):
        image = self._apply_line_detection_area_mask(bw_image)
        line = self.line_factory.get_line(image, self.start_x)
        self.detection_area_mask = self._create_line_detection_area_mask(line, image.shape)

        self.start_x = int(line[700][0])
        self.line_points = line;

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
