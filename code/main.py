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


image0 = "../input/images/test6.jpg"
image1 = "../input/images/straight_lines1.jpg"
image2 = "../input/images/straight_lines2.jpg"
video0 = "../input/project_video.mp4"
video1 = "../input/challenge_video.mp4"
video2 = "../input/harder_challenge_video.mp4"

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

camera = Camera(w, h)
camera.load_calibration_images(nx=9, ny=6, path_pattern="../input/camera_calibration/calibration*.jpg")
camera.calibrate()

# threshold = ColorAndGradientThresholdOperation()
threshold = WhiteAndYellowColorThresholdOperation()
transform_parameters = TransformationParameters(w, h, vanishing_point_distance, max_distance_coefficient)
perspective_transform = PerspectiveTransformationOperation(transform_parameters)

sliding_window_container = SlidingWindowsContainer()
sliding_window_line_detector = SlidingWindowLineDetector(sliding_window_container)
curved_line_factory = CurvedLineFactory(sliding_window_line_detector)

lane = Lane(curved_line_factory, x_meters_per_pixel)
validator = LaneValidator(lane_width_min_max, lane_width_deviation_tolerance, allow_line_projection)
lane_mask_factory = LaneMaskFactory(allow_line_projection)

logger = Logger()

image_processor = ImageProcessor(camera, threshold, perspective_transform, lane, validator, lane_mask_factory, logger)
lane_detector = LaneDetector(image_processor)

lane_detector.detect_on_image(image0)
# lane_detector.detect_on_video(video0)