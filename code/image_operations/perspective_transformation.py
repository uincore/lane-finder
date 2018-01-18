import cv2


class PerspectiveTransformationOperation:

    def __init__(self, transformation_parameters):
        self.transformation_parameters = transformation_parameters
        self.M_forward, self.M_back = self._get_transform_parameters()

    @property
    def vanishing_point_distance(self):
        return self.transformation_parameters.lane_vanishing_point_distance

    def _get_transform_parameters(self):
        src = self.transformation_parameters.source_image_points
        dst = self.transformation_parameters.destination_image_points

        M_forward = cv2.getPerspectiveTransform(src, dst)
        M_back = cv2.getPerspectiveTransform(dst, src)

        return M_forward, M_back

    def execute(self, image, to_bird_view=True):
        if to_bird_view:
            M = self.M_forward
            size = self.transformation_parameters.destination_image_size
        else:
            M = self.M_back
            size = self.transformation_parameters.source_image_size

        return cv2.warpPerspective(image, M, size, flags=cv2.INTER_LINEAR)

    def adjust_vanishing_point_distance(self, update_direction=0):
        adjust_step = 2
        vp_distance = 0
        if update_direction > 0:
            vp_distance = self.transformation_parameters.lane_vanishing_point_distance + adjust_step
        if update_direction < 0:
            vp_distance = self.transformation_parameters.lane_vanishing_point_distance - adjust_step

        if vp_distance:
            self.transformation_parameters.update_vanishing_point_distance(vp_distance)
            self.M_forward, self.M_back = self._get_transform_parameters()
