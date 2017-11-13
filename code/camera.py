import glob
import numpy as np
import cv2


class Camera:

    def __init__(self, image_width, image_height):
        self.object_points = []
        self.image_points = []
        self.width = image_width
        self.height = image_height
        self.camera_matrix = None
        self.dist_coefficients = None
        self.handled_images = {}

    @staticmethod
    def _get_object_points(nx, ny):
        obj_p = np.zeros((nx * ny, 3), np.float32)
        obj_p[:, :2] = np.mgrid[0:nx, 0:ny].T.reshape(-1, 2)

        return obj_p

    def _validate_image(self, image, details_message=""):
        assert image.shape[1] == self.width and image.shape[0] == self.height, \
            "Can't process image taken by different camera. " + details_message

    @property
    def image_width(self):
        return self.width

    @property
    def image_height(self):
        return self.height

    @property
    def perspective_distance(self):
        return 300

    def load_calibration_images(self, nx, ny, path_pattern):
        image_paths = glob.glob(path_pattern)

        obj_p = self._get_object_points(nx, ny)

        for image_path in image_paths:
            if image_path in self.handled_images:
                continue

            image_bgr = cv2.imread(image_path)
            image_gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

            self._validate_image(image_bgr, image_path)

            patternWasFound, corners = cv2.findChessboardCorners(image_gray, (nx, ny), None)

            if patternWasFound is True:
                self.object_points.append(obj_p)
                self.image_points.append(corners)
                self.handled_images[image_path] = True
            else:
                print("Image [{}] has intersection pattern different from {}x{} and will be skipped"
                      .format(image_path, nx, ny))

    def calibrate(self):
        result = cv2.calibrateCamera(self.object_points, self.image_points, (self.width, self.height),
                                     self.camera_matrix, self.dist_coefficients)

        retval, self.camera_matrix, self.dist_coefficients, rvecs, tvecs = result

    def undistort(self, image):
        self._validate_image(image)
        return cv2.undistort(image, self.camera_matrix, self.dist_coefficients, None, self.camera_matrix)