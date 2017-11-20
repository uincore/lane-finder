from image_processor import ImageProcessor
from lane_detector import LaneDetector
from camera import Camera
from image_operations.threshold import ColorAndGradientThresholdOperation
from image_operations.perspective_transformation import PerspectiveTransformationOperation
from image_operations.drawing.draw_lane import DrawLaneOperation


image0 = "../input/images/test6.jpg"
image1 = "../input/images/straight_lines1.jpg"
image2 = "../input/images/straight_lines2.jpg"
video0 = "../input/project_video.mp4"
video1 = "../input/challenge_video.mp4"
video2 = "../input/harder_challenge_video.mp4"

camera = Camera(1280, 720)
camera.load_calibration_images(nx=9, ny=6, path_pattern="../input/camera_calibration/calibration*.jpg")
camera.load_calibration_images(nx=9, ny=5, path_pattern="../input/camera_calibration/calibration*.jpg")
camera.calibrate()

threshold = ColorAndGradientThresholdOperation()
perspective_transform = PerspectiveTransformationOperation(camera.width, camera.height, camera.perspective_distance)
draw_line = DrawLaneOperation(1280, 720)
image_processor = ImageProcessor(camera, threshold, perspective_transform, draw_line)

lane_detector = LaneDetector(image_processor)

# lane_detector.detect_on_image(image0)
lane_detector.detect_on_video(video0)