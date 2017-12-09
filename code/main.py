from image_processor import ImageProcessor
from lane_detector import LaneDetector
from camera import Camera
from image_operations.threshold import ColorAndGradientThresholdOperation
from image_operations.perspective_transformation import PerspectiveTransformationOperation
from lane.lane import Lane
from line_factory.sliding_window import SlidingWindowsContainer
from line_factory.sliding_window_line_detector import SlidingWindowLineDetector
from line_factory.line_coordinates_factory import CurvedLineCoordinatesFactory


image0 = "../input/images/test6.jpg"
image1 = "../input/images/straight_lines1.jpg"
image2 = "../input/images/straight_lines2.jpg"
video0 = "../input/project_video.mp4"
video1 = "../input/challenge_video.mp4"
video2 = "../input/harder_challenge_video.mp4"

camera = Camera(1280, 720)
camera.load_calibration_images(nx=9, ny=6, path_pattern="../input/camera_calibration/calibration*.jpg")
camera.calibrate()

threshold = ColorAndGradientThresholdOperation()
perspective_transform = PerspectiveTransformationOperation(camera.width, camera.height, camera.perspective_distance)

sliding_window_container = SlidingWindowsContainer(720)
line_coordinates_factory = CurvedLineCoordinatesFactory(1280, 720)
line_factory = SlidingWindowLineDetector(sliding_window_container.windows, line_coordinates_factory)
lane = Lane(line_factory)

image_processor = ImageProcessor(camera, threshold, perspective_transform, lane)

lane_detector = LaneDetector(image_processor)

# lane_detector.detect_on_image(image0)
lane_detector.detect_on_video(video0)