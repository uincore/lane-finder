import numpy as np
from line_factory.frame import Frame
from line_factory.detection_area import DetectionArea


class SlidingWindowLineFactory:

    def __init__(self, sliding_windows, line_coordinates_factory):
        self.sliding_windows = sliding_windows
        self.line_coordinates_factory = line_coordinates_factory

    def get_line(self, bw_image, start_x):
        frame = Frame(bw_image)
        current_x = start_x
        line_pieces = []

        for window in self.sliding_windows:
            detection_boundaries = window.detection_area(current_x)
            line_points = frame.get_line_points(detection_boundaries)
            detection_area = DetectionArea(current_x, line_points)
            line_pieces.append(detection_area)

        y = []
        x = []

        for line_piece in line_pieces:
            y.extend(line_piece.y)
            x.extend(line_piece.x)

        line_points = np.array(y), np.array(x)
        return self.line_coordinates_factory.create(line_points)
