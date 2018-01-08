
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

    def __init__(self, lane_detection_area_width=200, sliding_windows_amount=9):
        self.detection_area_padding = lane_detection_area_width // 2
        self.windows_amount = sliding_windows_amount

    def get_windows(self, image_height):
        assert type(image_height) is int, "invalid image_height parameter"

        window_height = image_height // self.windows_amount

        sliding_windows = [self._create_window(i, image_height, window_height) for i in range(self.windows_amount)]
        return sliding_windows

    def _create_window(self, index, image_height, window_height):
        y_min, y_max = self._get_detection_area_y_boundaries(index, image_height, window_height)
        return SlidingWindow(y_min, y_max, self.detection_area_padding)

    def _get_detection_area_y_boundaries(self, window_index, image_height, window_height):
        y_min = image_height - (window_index + 1) * window_height
        y_max = image_height - window_index * window_height
        return y_min, y_max
