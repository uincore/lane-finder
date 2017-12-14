from image_processor import ImageProcessor
from lane_detector import LaneDetector
from camera import Camera
from image_operations.threshold import ColorAndGradientThresholdOperation
from image_operations.color_threshold import WhiteAndYellowColorThresholdOperation
from image_operations.perspective_transformation import PerspectiveTransformationOperation
from lane.lane import Lane
from line_factory.curved_line_coordinates_factory import CurvedLineCoordinatesFactory
from line_factory.sliding_window.sliding_window_container import SlidingWindowsContainer
from line_factory.sliding_window.sliding_window_line_detector import SlidingWindowLineDetector
from line_factory.sliding_window.curved_line_factory import CurvedLineFactory


image0 = "../input/images/test6.jpg"
image1 = "../input/images/straight_lines1.jpg"
image2 = "../input/images/straight_lines2.jpg"
video0 = "../input/project_video.mp4"
video1 = "../input/challenge_video.mp4"
video2 = "../input/harder_challenge_video.mp4"

# distance from image bottom to lane lines crossing in pixels, depends on camera position
perspective_distance = 300
min_distance = 40
max_distance = 200

w, h = 1280, 720

camera = Camera(w, h)
camera.load_calibration_images(nx=9, ny=6, path_pattern="../input/camera_calibration/calibration*.jpg")
camera.calibrate()

threshold = ColorAndGradientThresholdOperation()
color_threshold = WhiteAndYellowColorThresholdOperation()
perspective_transform = PerspectiveTransformationOperation(w, h, perspective_distance, min_distance, max_distance)

curved_line_coordinates_factory = CurvedLineCoordinatesFactory(w, h)

sliding_window_container = SlidingWindowsContainer(h)
sliding_window_line_detector = SlidingWindowLineDetector(sliding_window_container.windows)
curved_line_factory = CurvedLineFactory(sliding_window_line_detector, curved_line_coordinates_factory)

lane = Lane(curved_line_factory)

image_processor = ImageProcessor(camera, color_threshold, perspective_transform, lane)
lane_detector = LaneDetector(image_processor)

# lane_detector.detect_on_image(image0)
lane_detector.detect_on_video(video1)