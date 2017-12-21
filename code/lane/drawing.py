import numpy as np
import cv2


class Drawing:

    @staticmethod
    def create_mask_image(image_shape, left_line, right_line, color):
        r = np.flip(right_line, 0)
        total = np.concatenate([left_line, r]).astype(np.int32)

        mask_image = np.zeros(image_shape, dtype=np.uint8)
        cv2.fillPoly(mask_image, [total], color)

        return mask_image
