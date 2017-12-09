import cv2


class ImageProcessor:

    def __init__(self, camera, threshold, perspective_transform, lane):
        self.camera = camera
        self.threshold = threshold
        self.perspective_transform = perspective_transform
        self.lane = lane

    def process_frame(self, bgr_frame):

        undistorted_image = self.camera.undistort(bgr_frame)

        bw_image_filtered = self.threshold.execute(undistorted_image)
        bw_bird_view = self.perspective_transform.execute(bw_image_filtered, to_bird_view=True)
        lane_mask_bird_view = self.lane.create_mask_image(bw_bird_view)
        lane_mask = self.perspective_transform.execute(lane_mask_bird_view, to_bird_view=False)

        #TODO: add lane validation
        #TODO: add image text details

        result_image = cv2.addWeighted(lane_mask, 0.9, bgr_frame, 1, 0)



        # some text info on output image
        return result_image