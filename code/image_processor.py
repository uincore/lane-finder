import cv2


class ImageProcessor:

    def __init__(self, camera, image_operations):
        self.camera = camera
        self.image_operations = image_operations

    def process_frame(self, bgr_frame):

        undistorted_image = self.camera.undistort(bgr_frame)

        bgr_frame_masked = self.image_operations.apply_detection_area(undistorted_image)
        i = self.image_operations.highlight_lane_lines(bgr_frame_masked)
        i1 = self.image_operations.perspective_transform(i)

        return bgr_frame