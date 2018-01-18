from lane.lane import Lane
from lane.lane_validator import ValidationResult
from lane.drawing import Drawing


class LaneMaskFactory:

    def __init__(self, allow_line_projection):
        """
        :param allow_line_projection: boolean value that indicates if lane mask construction is allowed for one valid
                                        lane line and valid lane width. Invalid lane line will be replaced with copy of
                                        width shifted valid line.
        """
        self.allow_line_projection = allow_line_projection
        self.mask_color = (0, 255, 0)

    def create(self, lane, validation_result):
        assert type(lane) is Lane, "lane expected to be type of Lane"
        assert type(validation_result) is ValidationResult, "validation_result expected to be type of ValidationResult"

        h, w = lane.source_image.shape
        left_line, right_line = self._get_lane_lines(lane, validation_result, self.allow_line_projection)

        return Drawing.create_mask_image((h, w, 3), left_line, right_line, self.mask_color)

    @staticmethod
    def _get_lane_lines(lane, validation_result, allow_line_projection):
        if validation_result.left_line_detected and validation_result.right_line_detected:
            return lane.line_left.coordinates, lane.line_right.coordinates

        assert allow_line_projection is True, "unexpected method invocation"

        shift_unit = [[lane.width, 0]]
        if validation_result.left_line_detected:
            return lane.line_left.coordinates, \
                   lane.line_left.coordinates + shift_unit * lane.line_left.coordinates.shape[0]
        if validation_result.right_line_detected:
            return lane.line_right.coordinates - shift_unit * lane.line_right.coordinates.shape[0], \
                   lane.line_right.coordinates
