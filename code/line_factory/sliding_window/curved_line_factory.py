import numpy as np
from line_factory.curved_line import CurvedLine


class CurvedLineFactory:

    def __init__(self, sliding_window_line_detector, line_coordinates_factory):
        self.sliding_window_line_detector = sliding_window_line_detector
        self.line_coordinates_factory = line_coordinates_factory

    def create(self, line_image, start_x):
        detection_area_array = self.sliding_window_line_detector.detect(line_image, start_x)
        line_is_valid = self._validate(detection_area_array)
        raw_points = None
        coordinates = None

        if line_is_valid:
            raw_points = self._get_raw_line(detection_area_array)
            coordinates = self.line_coordinates_factory.create(raw_points)

        return CurvedLine(line_image, line_is_valid, raw_points, coordinates)

    @staticmethod
    def _get_raw_line(detection_area_array):
        y = []
        x = []

        for detection_area in detection_area_array:

            y.extend(detection_area.y)
            x.extend(detection_area.x)

        line_points = np.array(y), np.array(x)
        return line_points

    @staticmethod
    def _validate(detection_area_array):
        valid_areas = [x for x in detection_area_array if x.is_valid]
        return len(valid_areas) > 3 # TODO: distance should be more then 1
