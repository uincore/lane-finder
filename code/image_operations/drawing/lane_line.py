import numpy as np


class LaneLine:

    def __init__(self, start_x, image_height, threshold=50, lane_detection_area_width=200, sliding_windows_amount=9):
        self.start_x = start_x

        self.image_height = image_height
        self.pixels_threshold = threshold
        self.lane_detection_area_padding = lane_detection_area_width//2
        self.sliding_windows_amount = sliding_windows_amount
        self.sliding_window_height = self.image_height // self.sliding_windows_amount

    def detect(self, nonzero_x_indexes, nonzero_y_indexes):
        current_x = self.start_x
        lane_indexes_frames = []

        for window_index in range(self.sliding_windows_amount):
            x_min, x_max = self._get_detection_area_x_boundaries(current_x)
            y_min, y_max = self._get_detection_area_y_boundaries(window_index)
            detection_boundaries = (x_min, y_min), (x_max, y_max)

            frame_lane_indexes = self._get_lane_indexes(detection_boundaries, nonzero_x_indexes, nonzero_y_indexes)

            lane_indexes_frames.append(frame_lane_indexes)

            if len(frame_lane_indexes) > self.pixels_threshold:
                current_x = np.int(np.mean(nonzero_x_indexes[frame_lane_indexes]))

        lane_indexes = np.concatenate(lane_indexes_frames)
        x = nonzero_x_indexes[lane_indexes]
        y = nonzero_y_indexes[lane_indexes]

        return y, x

    def _get_detection_area_x_boundaries(self, x):
        x_min = x - self.lane_detection_area_padding
        x_max = x + self.lane_detection_area_padding
        return x_min, x_max

    def _get_detection_area_y_boundaries(self, sliding_window_index):
        y_min = self.image_height - (sliding_window_index + 1) * self.sliding_window_height
        y_max = self.image_height - sliding_window_index * self.sliding_window_height
        return y_min, y_max

    @staticmethod
    def _get_lane_indexes(detection_boundaries, nonzero_x, nonzero_y):
        (x_min, y_min), (x_max, y_max) = detection_boundaries
        good_indexes = (nonzero_x >= x_min) & (nonzero_x < x_max) & (nonzero_y >= y_min) & (nonzero_y < y_max)

        return good_indexes.nonzero()[0]
