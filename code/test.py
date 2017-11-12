import cv2
from image_operations import ImageOperations

bgr_frame = cv2.imread("../input/images/test6.jpg")
o = ImageOperations()
o.apply_detection_area(bgr_frame)
