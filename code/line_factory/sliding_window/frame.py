import numpy as np


class Frame:

    def __init__(self, bw_image):
        nonzero_y, nonzero_x = bw_image.nonzero()
        self.nonzero_x = np.array(nonzero_x)
        self.nonzero_y = np.array(nonzero_y)

    def get_line_points(self, window_boundaries):
        (x_min, y_min), (x_max, y_max) = window_boundaries

        area_mask = (self.nonzero_x >= x_min) & (self.nonzero_x < x_max) &\
                    (self.nonzero_y >= y_min) & (self.nonzero_y < y_max)

        line_indexes = area_mask.nonzero()[0]

        return self.nonzero_y[line_indexes], self.nonzero_x[line_indexes]
