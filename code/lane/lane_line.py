import numpy as np
# import matplotlib.pyplot as plt
from lane.drawing import Drawing


class LaneLine:

    def __init__(self, start_x, line_factory):
        self.start_x = start_x
        self.line_factory = line_factory
        self.detection_area_mask = None

    def detect(self, bw_image):

        image = np.copy(bw_image)
        if self.detection_area_mask is not None:
            image[self.detection_area_mask == 0] = 0

        current_line, _ = self.line_factory.get_line(image, self.start_x)

        line_points_count = len(current_line)
        delta = [[100, 0]] * line_points_count
        left_b = current_line - delta
        right_b = current_line + delta

        self.detection_area_mask = Drawing.create_mask_image(image.shape, left_b, right_b, 1)
        self.start_x = int(current_line[700][0])

        return current_line
