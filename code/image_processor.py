import cv2


class ImageProcessor:

    def __init__(self, camera, image_operations):
        self.camera = camera
        self.image_operations = image_operations

    def process_frame(self, bgr_frame):

        undistorted_image = self.camera.undistort(bgr_frame)

        bgr_frame_masked = self.image_operations.apply_detection_area(undistorted_image)
        i = self.image_operations.apply_color_and_gradient_threshold(bgr_frame_masked)
        i1 = self.image_operations.apply_perspective_transform(i)

        # lane detection
        # undo perspective transformation for detected lane
        # initial frame and detection area merge
        # some text info on output image

        return bgr_frame