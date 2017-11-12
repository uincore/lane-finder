import numpy as np
import cv2


class ImageOperations:

    def __init__(self, image_size):
        self._ignore_mask_color = (255, 255, 255)

        self.s_channel_threshold_min = 170
        self.s_channel_threshold_max = 255

        self.gradient_x_threshold_min = 20
        self.gradient_x_threshold_max = 100

        image_width, image_height = image_size
        self.src = self._get_source_points(image_width, image_height)
        self.dst = self._get_destination_points(image_width)

    @staticmethod
    def _get_source_points(image_width, image_height):
        tan_left_line_angle = 200 / 286
        max_distance = 270
        perspective_difference = max_distance // tan_left_line_angle

        src_points = [[0, image_height],
                      [0, image_height - max_distance],
                      [image_width - perspective_difference, image_height - max_distance],
                      [image_width, image_height]]

        return np.float32(src_points)

    @staticmethod
    def _get_destination_points(dst_image_side):
        dst_points = [[0, dst_image_side],
                      [0, 0],
                      [dst_image_side, 0],
                      [dst_image_side, dst_image_side]]

        return np.float32(dst_points)

    @staticmethod
    def _filter(gray_image, threshold_min, threshold_max):
        binary = np.zeros_like(gray_image)
        binary[(gray_image >= threshold_min) & (gray_image <= threshold_max)] = 1
        return binary

    @staticmethod
    def _get_gradient_x(gray_image):
        gradient_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0)
        abs_gradient_x = np.absolute(gradient_x)
        return np.uint8(255 * abs_gradient_x / np.max(abs_gradient_x))

    def apply_detection_area(self, image, width_adjustment=60, height_adjustment=65):
        im_height, im_width = image.shape[0], image.shape[1]
        im_half_height, im_half_width = im_height // 2, im_width // 2

        area_left_bottom = (0, im_height)
        area_left_top = (im_half_width - width_adjustment, im_half_height + height_adjustment)
        area_right_top = (im_half_width + width_adjustment, im_half_height + height_adjustment)
        area_right_bottom = (im_width, im_height)

        detection_area = [area_left_bottom, area_left_top, area_right_top, area_right_bottom]
        vertices = np.array([detection_area], dtype=np.int32)

        mask = np.zeros_like(image)
        cv2.fillPoly(mask, vertices, self._ignore_mask_color)

        masked_image = cv2.bitwise_and(image, mask)
        return masked_image

    def apply_color_and_gradient_threshold(self, bgr_image):
        image_hls = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HLS)
        s_channel = image_hls[:, :, 2]
        s_channel_bw = self._filter(s_channel, self.s_channel_threshold_min, self.s_channel_threshold_max)

        gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
        gradient_x = self._get_gradient_x(gray_image)
        gradient_x_bw = self._filter(gradient_x, self.gradient_x_threshold_min, self.gradient_x_threshold_max)

        combined_bw_image = np.zeros_like(s_channel_bw)
        combined_bw_image[(s_channel_bw == 1) | (gradient_x_bw == 1)] = 1

        return combined_bw_image

    def apply_perspective_transform(self, image):
        M = cv2.getPerspectiveTransform(self.src, self.dst)
        shape = (1280, 1280)
        warped = cv2.warpPerspective(image, M, shape, flags=cv2.INTER_LINEAR)
        return warped