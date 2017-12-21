import numpy as np
import cv2


class WhiteAndYellowColorThresholdOperation:

    def __init__(self):
        self._lower_yellow = np.array([20, 0, 170], dtype=np.uint8)
        self._upper_yellow = np.array([55, 255, 255], dtype=np.uint8)

        self._lower_white = np.array([0, 0, 220], dtype=np.uint8)
        self._upper_white = np.array([255, 25, 255], dtype=np.uint8)

    def execute(self, bgr_image):
        hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
        mask_yellow = cv2.inRange(hsv_image, self._lower_yellow, self._upper_yellow)
        mask_white = cv2.inRange(hsv_image, self._lower_white, self._upper_white)

        mask = cv2.add(mask_white, mask_yellow)
        return mask
