import cv2
import matplotlib.pyplot as plt


class ImageProcessor:

    def __init__(self, camera, threshold, perspective_transform):
        self.camera = camera
        self.threshold = threshold
        self.perspective_transform = perspective_transform

    def process_frame(self, bgr_frame):

        undistorted_image = self.camera.undistort(bgr_frame)

        bw_image_filtered = self.threshold.apply(undistorted_image)
        bw_bird_view = self.perspective_transform.apply(bw_image_filtered, to_bird_view=True)

        # lane detection
        # undo perspective transformation for detected lane
        #i2 = self.perspective_transform.apply(i, to_bird_view=False)
        # initial frame and detection area merge
        # some text info on output image


        return bgr_frame