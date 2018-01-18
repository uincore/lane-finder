import numpy as np
from lane.lane import Lane


class LaneValidator:

    def __init__(self, width_min_max, width_deviation_tolerance, allow_line_projection):
        """
        :param width_min_max: valid lane width boundaries in points in (min, max) format
        :param width_deviation_tolerance: lane width deviation tolerance in points
        :param allow_line_projection: boolean value that indicates if lane mask construction is allowed for one valid
                                        lane line and valid lane width. Invalid lane line will be replaced with copy of
                                        width shifted valid line. 
        """
        self.min_lane_width = width_min_max[0]
        self.max_lane_width = width_min_max[1]
        self.width_deviation_tolerance = width_deviation_tolerance
        self.allow_line_projection = allow_line_projection

    @staticmethod
    def _get_width_deviation(line1_coordinates, line2_coordinates):
        return np.std((line1_coordinates - line2_coordinates)[:, 0])

    @staticmethod
    def _line_is_valid(line):
        return line is not None and line.is_valid

    def _car_is_on_lane(self, left_line, right_line, image_width):
        left_line_is_valid = self._line_is_valid(left_line)
        right_line_is_valid = self._line_is_valid(right_line)
        image_center = image_width // 2

        return (left_line_is_valid and left_line.coordinates[0][0] < image_center) or \
               (right_line_is_valid and right_line.coordinates[0][0] > image_center)

    def validate(self, lane):
        assert type(lane) is Lane, "lane parameter expected to Lane instance, but was {}".format(type(lane))

        left_line, right_line, lane_width = lane.line_left, lane.line_right, lane.width
        left_line_is_valid = self._line_is_valid(left_line)
        right_line_is_valid = self._line_is_valid(right_line)
        lane_width_is_valid = self.min_lane_width < lane_width < self.max_lane_width

        if lane_width_is_valid:
            car_is_on_lane = self._car_is_on_lane(left_line, right_line, lane.source_image.shape[0])
            if left_line_is_valid and right_line_is_valid:
                width_deviation = self._get_width_deviation(left_line.coordinates, right_line.coordinates)
                lines_are_parallel = width_deviation < self.width_deviation_tolerance
                message = "" if lines_are_parallel else "Both lines detected but lane width deviation is too high"
                return ValidationResult(lines_are_parallel,
                                        left_line_is_valid,
                                        right_line_is_valid,
                                        message,
                                        car_is_on_lane,
                                        int(width_deviation))

            one_line_is_valid = left_line_is_valid != right_line_is_valid
            if self.allow_line_projection and one_line_is_valid:
                return ValidationResult(True, left_line_is_valid, right_line_is_valid, "", car_is_on_lane)
            else:
                message = "Projection allowed: {}, Both lines are invalid: {}".format(self.allow_line_projection,
                                                                                      not one_line_is_valid)
        else:
            message = "Lane width {:.0f} is invalid".format(lane_width)

        return ValidationResult(False, left_line.is_valid, right_line.is_valid, message)


class ValidationResult:

    def __init__(self, is_valid, ll_is_valid, rl_is_valid, message, car_is_on_lane=False, width_deviation=0):
        self.lane_is_valid = is_valid
        self.left_line_is_valid = ll_is_valid
        self.right_line_is_valid = rl_is_valid
        self.is_on_lane = car_is_on_lane
        self.w_deviation = width_deviation
        self.validation_message = message

    @property
    def lane_is_lost(self):
        return not self.lane_is_valid

    @property
    def left_line_detected(self):
        return self.left_line_is_valid

    @property
    def right_line_detected(self):
        return self.right_line_is_valid

    @property
    def car_is_on_lane(self):
        return self.is_on_lane

    @property
    def width_deviation(self):
        return self.w_deviation

    @property
    def message(self):
        return self.validation_message
