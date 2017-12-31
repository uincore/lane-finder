from os import path
from os import makedirs
from datetime import datetime
import json
import cv2
from lane.lane_validator import ValidationResult
from lane.lane import Lane


class Logger:

    def __init__(self, log_output_dir="..\\logs"):
        run_folder_name =  datetime.now().strftime("%Y_%m_%d.%H-%M-%S")
        self.log_output_dir = path.join(log_output_dir, run_folder_name)

        if not path.exists(self.log_output_dir):
            makedirs(self.log_output_dir)

        self.log_file_path = path.join(self.log_output_dir, "_logs.txt")

    def info(self, validation_result, bgr_image, bw_image):
        assert type(validation_result) is ValidationResult, "validation_result expected to be type of ValidationResult"

        timestamp = datetime.now().strftime("%Y_%m_%d.%H-%M-%S-%f")
        bw_image_path = path.join(self.log_output_dir, timestamp + "_bw.png")
        color_image_path = path.join(self.log_output_dir, timestamp + "_color.png")

        log_entry = {
            "timestamp": timestamp,
            "message": validation_result.message
        }
        log_message = json.dumps(log_entry)

        with open(self.log_file_path, "a") as log_file:
            log_file.write(log_message)
            log_file.write("\n")

        cv2.imwrite(bw_image_path, bw_image)
        cv2.imwrite(color_image_path, bgr_image)
