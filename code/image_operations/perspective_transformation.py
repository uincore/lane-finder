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

    def execute(self, image, transform_to):
        """
        :param image: source image
        :param transform_to: acceptable value is 'top_down_view' or 'front_view'
        :return: new image with applied perspective transformation
        """
        assert transform_to == "top_down_view" or transform_to == "front_view", \
            "invalid transform_direction"

        if transform_to == "top_down_view":
            M = self.M_forward
            size = self.transformation_parameters.destination_image_size
        elif transform_to == "front_view":
            M = self.M_back
            size = self.transformation_parameters.source_image_size
        else:
            raise Exception("acceptable value for transform_direction is 'top_down_view' or 'front_view'")

        return cv2.warpPerspective(image, M, size, flags=cv2.INTER_LINEAR)

    def adjust_vanishing_point_distance(self, update_direction=0):
        adjust_step = 1
        vp_distance = 0
        if update_direction > 0:
            vp_distance = self.transformation_parameters.lane_vanishing_point_distance + adjust_step
        if update_direction < 0:
            vp_distance = self.transformation_parameters.lane_vanishing_point_distance - adjust_step

        if vp_distance:
            self.transformation_parameters.update_vanishing_point_distance(vp_distance)
            self.M_forward, self.M_back = self._get_transform_parameters()
