from image_processor import ImageProcessor
from lane_detector import LaneDetector
from camera import Camera
from image_operations import ImageOperations


image1 = "../input/images/test6.jpg"
video1 = "../input/project_video.mp4"

camera = Camera()
camera.calibrate()

image_operations = ImageOperations()
image_processor = ImageProcessor(camera, image_operations)
lane_detector = LaneDetector(image_processor)

lane_detector.detect_on_image(image1)
#lane_detector.detect_on_video(video1)