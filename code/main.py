from image_processor import ImageProcessor
from lane_detector import LaneDetector
from camera import Camera
from image_operations.threshold import ColorAndGradientThresholdOperation
from image_operations.color_threshold import WhiteAndYellowColorThresholdOperation
from image_operations.perspective_transformation import PerspectiveTransformationOperation
from lane.lane import Lane
from lane.lane_validator import LaneValidator
from line_factory.curved_line_coordinates_factory import CurvedLineCoordinatesFactory
from line_factory.sliding_window.sliding_window_container import SlidingWindowsContainer
from line_factory.sliding_window.sliding_window_line_detector import SlidingWindowLineDetector
from line_factory.sliding_window.curved_line_factory import CurvedLineFactory
from logger import Logger


image0 = "../input/images/test6.jpg"
image1 = "../input/images/straight_lines1.jpg"
image2 = "../input/images/straight_lines2.jpg"
video0 = "../input/project_video.mp4"
video1 = "../input/challenge_video.mp4"
video2 = "../input/harder_challenge_video.mp4"

# distance from image bottom to lane lines crossing in pixels, depends on camera position
vanishing_point_distance = 320
max_distance, x_meters_per_pixel = 200, 3.7 / 700
line_projection = True

lane_width_min_max = (600, 1000)
lane_width_deviation_tolerance = 150

w, h = 1280, 720

camera = Camera(w, h)
camera.load_calibration_images(nx=9, ny=6, path_pattern="../input/camera_calibration/calibration*.jpg")
camera.calibrate()

# threshold = ColorAndGradientThresholdOperation()
threshold = WhiteAndYellowColorThresholdOperation()
perspective_transform = PerspectiveTransformationOperation(w, h, vanishing_point_distance, max_distance)

curved_line_coordinates_factory = CurvedLineCoordinatesFactory()

sliding_window_container = SlidingWindowsContainer()
sliding_window_line_detector = SlidingWindowLineDetector(sliding_window_container)
curved_line_factory = CurvedLineFactory(sliding_window_line_detector, curved_line_coordinates_factory)

lane = Lane(curved_line_factory)
validator = LaneValidator(w, lane_width_min_max, lane_width_deviation_tolerance)

logger = Logger()

image_processor = ImageProcessor(camera, threshold, perspective_transform, lane, validator, line_projection, logger)
lane_detector = LaneDetector(image_processor)

# lane_detector.detect_on_image(image1)
lane_detector.detect_on_video(video0)