import sys
sys.path.append("../")

from image_processor import ImageProcessor
from lane_detector import LaneDetector
from camera import Camera
from image_operations.threshold import ColorAndGradientThresholdOperation
from image_operations.color_threshold import WhiteAndYellowColorThresholdOperation
from image_operations.transformation_parameters import TransformationParameters
from image_operations.perspective_transformation import PerspectiveTransformationOperation
from lane.lane import Lane
from lane.lane_validator import LaneValidator
from line_factory.sliding_window.sliding_window_container import SlidingWindowsContainer
from line_factory.sliding_window.sliding_window_line_detector import SlidingWindowLineDetector
from line_factory.sliding_window.curved_line_factory import CurvedLineFactory
from lane.lane_mask_factory import LaneMaskFactory
from logger import Logger
import matplotlib.pyplot as plt
import cv2
import numpy as np
from lane.drawing import Drawing
from line_factory.curved_line_coordinates_factory import CurvedLineCoordinatesFactory
from line_factory.polynomial import Polynomial


# distance from image bottom to lane lines crossing in pixels, depends on camera position
vanishing_point_distance = 310
x_meters_per_pixel = 3.7 / 700
# max distance will be a result of vanishing_point_distance * max_distance_coefficient multiplication
max_distance_coefficient = 0.85
# allow ar deny lane mask construction for known lane width and one valid lane line case
allow_line_projection = True
# valid lane width boundaries
lane_width_min_max = (650, 1000)
lane_width_deviation_tolerance = 60

w, h = 1280, 720

sliding_window_container = SlidingWindowsContainer()
sliding_window_line_detector = SlidingWindowLineDetector(sliding_window_container)
curved_line_factory = CurvedLineFactory(sliding_window_line_detector)

lane = Lane(curved_line_factory, x_meters_per_pixel)
validator = LaneValidator(lane_width_min_max, lane_width_deviation_tolerance, allow_line_projection)


def convert(image):
    return image[..., [2, 1, 0]]


bgr_frame = cv2.imread("curvature_test_image.png")
bw_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2GRAY)

lane.update(bw_frame)
validation_result = validator.validate(lane)

print("Lane curvature radius: {:.0f}m".format(lane.radius_m))
print("Lane curvature radius: {:.0f}pixels".format(lane.radius_m/x_meters_per_pixel))
print("1000 pixels is {:.0f} meters".format(1000*x_meters_per_pixel))
print("Lane width is: {:.2f}m".format(lane.width*x_meters_per_pixel))
print("-"*20)
print("Left line radius: {:.0f}m".format(lane.line_left.radius*x_meters_per_pixel))
print("Right line radius: {:.0f}m".format(lane.line_right.radius*x_meters_per_pixel))

mask = Drawing.create_mask_image(bw_frame.shape, lane.line_left.coordinates, lane.line_right.coordinates, 255)
line_points = mask.nonzero()
avg_line, coefficients = CurvedLineCoordinatesFactory.create(line_points, bw_frame.shape[0])
y0 = 1600
x0 = avg_line[y0][0]
radius = Polynomial.radius(coefficients, y0)
distance = Polynomial.distance(coefficients, 0, 1600)
print("-"*30)
print("Lane radius: {:.0f}m".format(radius * x_meters_per_pixel))
print("Mask distance: {:.1f}m".format(distance * x_meters_per_pixel))

rgb_frame = convert(bgr_frame)
plt.imshow(rgb_frame)

x2, y2 = avg_line.T
plt.plot(x2, y2, "fuchsia")

tangent_fn = Polynomial.get_tangent_fn(coefficients, x0, y0)
pt1y, pt2y = 10, 1600
pt1x = tangent_fn(pt1y)
pt2x = tangent_fn(pt2y)

normal_fn = Polynomial.get_normal_fn(coefficients, x0, y0)
pn1y, pn2y = 1500, 1604
pn1x = normal_fn(pn1y)
pn2x = normal_fn(pn2y)

cx1, cy1 = Polynomial.center(coefficients, x0, y0, radius)
plt.plot([x0, cx1], [y0, cy1], "b-")

plt.plot([pt1x, pt2x], [pt1y, pt2y], "g-")
plt.plot([pn1x, pn2x], [pn1y, pn2y], "r-")

# x, y = lane.line_left.coordinates.T
# plt.plot(x, y, "g")
# x1, y1 = lane.line_right.coordinates.T
# plt.plot(x1, y1, "b")

plt.show()
