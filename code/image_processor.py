import cv2
from lane.drawing import Drawing
from lane.lane import Lane
from lane.lane_validator import ValidationResult


class ImageProcessor:

    def __init__(self, camera, threshold, perspective_transform, lane, lane_validator, allow_line_projection, logger):
        assert type(lane) is Lane, "lane parameter expected to point to Lane instance, but was {}".format(type(lane))

        self.camera = camera
        self.threshold = threshold
        self.perspective_transform = perspective_transform
        self.lane = lane
        self.lane_validator = lane_validator
        self.allow_line_projection = allow_line_projection
        self.logger = logger
        self.mask_color = (0, 255, 0)

    def process_frame(self, bgr_frame):

        undistorted_image = self.camera.undistort(bgr_frame)
        bw_image_filtered = self.threshold.execute(undistorted_image)
        bw_bird_view = self.perspective_transform.execute(bw_image_filtered, to_bird_view=True)

        self.lane.update(bw_bird_view)

        validation_result = self.lane_validator.validate(self.lane, self.allow_line_projection)

        if validation_result.lane_is_lost:
            self.lane.reset()
            result_image = bgr_frame
            texts = [
                "Lane lost: {}".format(validation_result.message),
                "Lane width: {}".format(self.lane.width),
                "Left line detected: {}".format(validation_result.left_line_detected),
                "Right line detected: {}".format(validation_result.right_line_detected),
                "Width deviation: {}".format(validation_result.width_deviation),
                "Vanishing point distance: {}".format(self.perspective_transform.vanishing_point_distance)
            ]

            self.logger.info(validation_result, bgr_frame, bw_bird_view, texts)
        else:
            left_line, right_line = self._get_lane_lines(self.lane, validation_result)
            perspective_distance_adjust_direction = self.lane.top_width - self.lane.width
            texts = [
                "Lane detected",
                "Lane width: {}".format(self.lane.width),
                "Left line detected: {}".format(validation_result.left_line_detected),
                "Right line detected: {}".format(validation_result.right_line_detected),
                "Width deviation: {}".format(validation_result.width_deviation),
                "Vanishing point distance: {}".format(self.perspective_transform.vanishing_point_distance),
                "Car is on lane: {}".format(validation_result.car_is_on_lane),
                "Left X: {:.0f}   Right X: {:.0f}".format(left_line[0][0], right_line[0][0])
            ]

            lane_mask_bird_view = Drawing.create_mask_image(bgr_frame.shape, left_line, right_line, self.mask_color)
            lane_mask = self.perspective_transform.execute(lane_mask_bird_view, to_bird_view=False)
            result_image = cv2.addWeighted(lane_mask, 0.9, bgr_frame, 1, 0)

            self.perspective_transform.adjust_vanishing_point_distance(perspective_distance_adjust_direction)

            if not validation_result.car_is_on_lane:
                self.lane.reset()

        # result_image = bw_bird_view
        self._add_text(result_image, texts)
        return result_image

    def _get_lane_lines(self, lane, validation_result):
        assert type(validation_result) is ValidationResult, "validation_result expected to be type of ValidationResult"

        if validation_result.left_line_detected and validation_result.right_line_detected:
            return lane.line_left.coordinates, lane.line_right.coordinates

        assert self.allow_line_projection is True, "unexpected method invocation"

        shift = [[lane.width, 0]] * self.camera.image_height
        if validation_result.left_line_detected:
            return lane.line_left.coordinates, lane.line_left.coordinates + shift
        if validation_result.right_line_detected:
            return lane.line_right.coordinates - shift, lane.line_right.coordinates

    def _add_text(self, image, texts):
        line_height = 40
        v_position = 50
        for text in texts:
            cv2.putText(image, text, (10, v_position), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            v_position += line_height
