import sys
sys.path.append("../")

from camera import Camera
import matplotlib.pyplot as plt
import cv2
import numpy as np


def convert(image):
    return image[..., [2, 1, 0]]


w, h = 1280, 720

camera = Camera(w, h)
camera.load_calibration_images(nx=9, ny=6, path_pattern="../../input/camera_calibration/calibration*.jpg")
camera.load_calibration_images(nx=9, ny=5, path_pattern="../../input/camera_calibration/calibration*.jpg")
camera.load_calibration_images(nx=7, ny=5, path_pattern="../../input/camera_calibration/calibration*.jpg")
camera.load_calibration_images(nx=5, ny=6, path_pattern="../../input/camera_calibration/calibration*.jpg")
camera.calibrate()

bgr_frame = cv2.imread("../../images/distorted.jpg")

bgr_undistorted = camera.undistort(bgr_frame)
rgb_result = convert(bgr_undistorted)

plt.imshow(rgb_result)
plt.show()

cv2.imwrite("ttt.png", bgr_undistorted)