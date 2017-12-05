import numpy as np
import cv2


class ColorAndGradientThresholdOperation:

    def __init__(self):
        self.s_channel_threshold_min = 170
        self.s_channel_threshold_max = 255

        self.gradient_x_threshold_min = 20
        self.gradient_x_threshold_max = 100

    def execute(self, bgr_image):
        image_hls = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HLS)
        s_channel = image_hls[:, :, 2]
        s_channel_bw = self._filter(s_channel, self.s_channel_threshold_min, self.s_channel_threshold_max)

        gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
        gradient_x = self._get_gradient_x(gray_image)
        gradient_x_bw = self._filter(gradient_x, self.gradient_x_threshold_min, self.gradient_x_threshold_max)

        combined_bw_image = np.zeros_like(s_channel_bw)
        combined_bw_image[(s_channel_bw == 1) | (gradient_x_bw == 1)] = 1

        return combined_bw_image

    @staticmethod
    def _get_gradient_x(gray_image):
        gradient_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0)
        abs_gradient_x = np.absolute(gradient_x)
        return np.uint8(255 * abs_gradient_x / np.max(abs_gradient_x))

    @staticmethod
    def _filter(gray_image, threshold_min, threshold_max):
        binary = np.zeros_like(gray_image)
        binary[(gray_image >= threshold_min) & (gray_image <= threshold_max)] = 1
        return binary
