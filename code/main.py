import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
import os
import numpy as np
from image_processor import ImageProcessor

image1 = "../input/images/test6.jpg"
video1 = "../input/project_video.mp4"

img_processor = ImageProcessor()

def get_path_for(file_path):
    current_directory = os.path.dirname(__file__)
    return os.path.join(current_directory, file_path)

def playVideo(file_path):
    video_path = get_path_for(file_path)
    video = cv2.VideoCapture(video_path)

    while video.isOpened():
        _, bgr_frame = video.read()

        if not isinstance(bgr_frame, np.ndarray):
            # workaround to handle end of video stream.
            break

        frame = img_processor.process_frame(bgr_frame)
        cv2.imshow("output", frame)

        key = cv2.waitKey(1) & 0xFF
        # stop video on ESC key pressed
        if key == 27:
            break

    video.release()
    cv2.destroyAllWindows()


def showImage(file_path):
    def convert(image):
        return image[..., [2, 1, 0]]

    image_path = get_path_for(file_path)
    rgb_image = mpimg.imread(image_path)

    bgr_frame = convert(rgb_image)
    frame = img_processor.process_frame(bgr_frame)
    rgb_frame = convert(frame)

    plt.imshow(rgb_frame)
    plt.show()

showImage(image1)
#playVideo(video1)