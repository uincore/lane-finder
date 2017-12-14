from line_factory.sliding_window.frame import Frame
from line_factory.sliding_window.detection_area import DetectionArea


class SlidingWindowLineDetector:

    def __init__(self, sliding_windows):
        self.sliding_windows = sliding_windows

    def detect(self, bw_image, start_x):
        frame = Frame(bw_image)
        current_x = start_x
        line_pieces = []

        for window in self.sliding_windows:
            detection_boundaries = window.detection_area(current_x)
            line_points = frame.get_line_points(detection_boundaries)
            detection_area = DetectionArea(current_x, line_points)
            current_x = detection_area.center_x
            line_pieces.append(detection_area)

        return line_pieces
