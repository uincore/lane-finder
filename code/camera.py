import glob
import numpy as np
import cv2


class Camera:

    def __init__(self):
        self.object_points = []
        self.image_points = []
        self.camera_image_size = None
        self.camera_matrix = None
        self.dist_coefficients = None

    @staticmethod
    def _get_object_points(nx, ny):
        obj_p = np.zeros((nx * ny, 3), np.float32)
        obj_p[:, :2] = np.mgrid[0:nx, 0:ny].T.reshape(-1, 2)

        return obj_p

    def _validate_image(self, image, details_message=""):
        image_size = (image.shape[1], image.shape[0])
        assert image_size == self.camera_image_size, "Can't process image taken by different camera. "+details_message

    def load_calibration_images(self, nx=9, ny=6, path_pattern="../input/camera_calibration/calibration*.jpg"):
        image_paths = glob.glob(path_pattern)

        obj_p = self._get_object_points(nx, ny)

        for image_path in image_paths:
            image_bgr = cv2.imread(image_path)
            image_gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

            if self.camera_image_size is None:
                self.camera_image_size = image_gray.shape[::-1]

            self._validate_image(image_bgr, image_path)

            patternWasFound, corners = cv2.findChessboardCorners(image_gray, (nx, ny), None)

            if patternWasFound is True:
                self.object_points.append(obj_p)
                self.image_points.append(corners)
            else:
                print("Image [{}] has intersection pattern different from {}x{} and will be skipped"
                      .format(image_path, nx, ny))

    def calibrate(self):
        result = cv2.calibrateCamera(self.object_points, self.image_points, self.camera_image_size,
                                     self.camera_matrix, self.dist_coefficients)

        retval, self.camera_matrix, self.dist_coefficients, rvecs, tvecs = result

    def undistort(self, image):
        self._validate_image(image)
        return cv2.undistort(image, self.camera_matrix, self.dist_coefficients, None, self.camera_matrix)