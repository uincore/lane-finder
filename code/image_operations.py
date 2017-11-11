import numpy as np
import cv2


class ImageOperations:

    def __init__(self):
        self._ignore_mask_color = 255

    def apply_detection_area(self, bw_image, width_adjustment=60, height_adjustment=65):
        im_height = bw_image.shape[0]
        im_half_height = im_height // 2
        im_width = bw_image.shape[1]
        im_half_width = im_width // 2

        area_left_bottom = (0, im_height)
        area_left_top = (im_half_width - width_adjustment, im_half_height + height_adjustment)
        area_right_top = (im_half_width + width_adjustment, im_half_height + height_adjustment)
        area_right_bottom = (im_width, im_height)

        detection_area = [area_left_bottom, area_left_top, area_right_top, area_right_bottom]
        vertices = np.array([detection_area], dtype=np.int32)

        mask = np.zeros_like(bw_image)
        cv2.fillPoly(mask, vertices, self._ignore_mask_color)

        masked_image = cv2.bitwise_and(bw_image, mask)
        return masked_image

    # color and gradient threshold
    def apply_color_and_gradient_threshold(self, rgb_image):
        return rgb_image

    def apply_perspective_transform(self, gray_image):
        return gray_image