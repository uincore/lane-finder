import sys
sys.path.append("../")

from image_operations.transformation_parameters import TransformationParameters
from image_operations.perspective_transformation import PerspectiveTransformationOperation
import cv2


# distance from image bottom to lane lines crossing in pixels, depends on camera position
initial_vanishing_point_distance = 300
# max distance will be a result of vanishing_point_distance * max_distance_coefficient multiplication
max_distance_coefficient = 0.75
# camera output image size
w, h = 1280, 720

transform_parameters = TransformationParameters(w, h, initial_vanishing_point_distance, max_distance_coefficient)
perspective_transform = PerspectiveTransformationOperation(transform_parameters)

bgr_frame = cv2.imread("001_undistorted_image.png")

top_down_view = perspective_transform.execute(bgr_frame, transform_to="top_down_view")

p = transform_parameters.source_image_points.astype(int)
p = p.reshape((-1,1,2))
cv2.polylines(bgr_frame, [p] ,True,(0,0,255), 3)

cv2.imwrite("front_view_with_lines.png", bgr_frame)
cv2.imwrite("top_view.png", top_down_view)



