import cv2
from frame_info import FrameInfo


class ImageProcessor:

    def __init__(self, camera, threshold, perspective_transform, lane, lane_validator, lane_mask_factory, logger):
        self.camera = camera
        self.threshold = threshold
        self.perspective_transform = perspective_transform
        self.lane = lane
        self.lane_validator = lane_validator
        self.lane_mask_factory = lane_mask_factory
        self.logger = logger
        self.mask_color = (0, 255, 0)

    def process_frame(self, bgr_frame):
        undistorted_image = self.camera.undistort(bgr_frame)

        bw_image_filtered = self.threshold.execute(undistorted_image)
        bw_bird_view = self.perspective_transform.execute(bw_image_filtered, to_bird_view=True)

        self.lane.update(bw_bird_view)

        validation_result = self.lane_validator.validate(self.lane)
        texts = FrameInfo.create(self.lane, validation_result, self.perspective_transform.vanishing_point_distance)

        if validation_result.lane_is_lost:
            self.lane.reset()
            self.logger.info(validation_result, bgr_frame, bw_bird_view, texts)

            result_image = undistorted_image
        else:
            lane_mask_bird_view = self.lane_mask_factory.create(self.lane, validation_result)
            lane_mask = self.perspective_transform.execute(lane_mask_bird_view, to_bird_view=False)

            result_image = cv2.addWeighted(lane_mask, 0.9, undistorted_image, 1, 0)

            perspective_distance_adjust_direction = self.lane.top_width - self.lane.width
            self.perspective_transform.adjust_vanishing_point_distance(perspective_distance_adjust_direction)

            if not validation_result.car_is_on_lane:
                self.lane.reset()

        FrameInfo.print(result_image, texts)
        return result_image
