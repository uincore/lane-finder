
class SlidingWindow:

    def __init__(self, y_min, y_max, x_padding):
        self.y_min = y_min
        self.y_max = y_max
        self.x_padding = x_padding

    def detection_area(self, window_center_x):
        x_min = window_center_x - self.x_padding
        x_max = window_center_x + self.x_padding

        return (x_min, self.y_min), (x_max, self.y_max)


class SlidingWindowsContainer:

    def __init__(self, image_height, lane_detection_area_width=200, sliding_windows_amount=9):
        self.image_height = image_height
        self.sliding_window_height = self.image_height // sliding_windows_amount
        self.lane_detection_area_padding = lane_detection_area_width // 2

        self.sliding_windows = [self._create_window(i) for i in range(sliding_windows_amount)]

    @property
    def windows(self):
        return self.sliding_windows

    def _create_window(self, index):
        y_min, y_max = self._get_detection_area_y_boundaries(index)
        return SlidingWindow(y_min, y_max, self.lane_detection_area_padding)

    def _get_detection_area_y_boundaries(self, sliding_window_index):
        y_min = self.image_height - (sliding_window_index + 1) * self.sliding_window_height
        y_max = self.image_height - sliding_window_index * self.sliding_window_height
        return y_min, y_max
