# import numpy as np
# from lane.drawing import Drawing


class LaneLine:

    def __init__(self, start_x, curved_line_factory):
        self.start_x = start_x
        self.end_x = None
        self.curved_line_factory = curved_line_factory

        self.line = None

    @property
    def x_bottom(self):
        return self.start_x

    @property
    def x_top(self):
        return self.end_x

    @property
    def coordinates(self):
        return self.line.coordinates

    @property
    def is_valid(self):
        return self.line.is_valid

    def update(self, bw_image):
        self.line = self.curved_line_factory.create(bw_image, self.start_x)

        if self.line.is_valid:
            self.start_x = int(self.line.coordinates[-20][0])
            self.end_x = int(self.line.coordinates[0][0])

    # @staticmethod
    # def _create_line_detection_area_mask(line, image_shape):
    #     line_points_count = len(line)
    #     delta = [[100, 0]] * line_points_count
    #     left_b = line - delta
    #     right_b = line + delta
    #
    #     return Drawing.create_mask_image(image_shape, left_b, right_b, 1)
