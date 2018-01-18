from image_processor import ImageProcessor
from lane_detector import LaneDetector
from camera import Camera
from image_operations.threshold import ColorAndGradientThresholdOperation
from image_operations.color_threshold import WhiteAndYellowColorThresholdOperation
from image_operations.perspective import Perspective
from image_operations.perspective_transformation import PerspectiveTransformationOperation
from lane.lane import Lane
from lane.lane_validator import LaneValidator
from line_factory.curved_line_coordinates_factory import CurvedLineCoordinatesFactory
from line_factory.sliding_window.sliding_window_container import SlidingWindowsContainer
from line_factory.sliding_window.sliding_window_line_detector import SlidingWindowLineDetector
from line_factory.sliding_window.curved_line_factory import CurvedLineFactory
from logger import Logger
import matplotlib.pyplot as plt
import cv2
import numpy as np

vanishing_point_distance = 300
x_meters_per_pixel = 3.7 / 700
line_projection = True

lane_width_min_max = (600, 1000)
lane_width_deviation_tolerance = 50

w, h = 1280, 720

perspective = Perspective(w, h, vanishing_point_distance, x_meters_per_pixel, 0.85)
perspective_transform = PerspectiveTransformationOperation(perspective)


def convert(image):
    return image[..., [2, 1, 0]]


bgr_frame = cv2.imread("../input/images/straight_lines1.jpg")

frame = perspective_transform.execute(bgr_frame, True)
frame1 = perspective_transform.execute(frame, False)

rgb_frame = convert(frame)
plt.imshow(rgb_frame)
plt.show()