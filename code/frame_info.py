import cv2


class FrameInfo:

    @staticmethod
    def create(lane, lane_validation_result, vanishing_point_distance):
        texts = [
            "Lane width: {}".format(lane.width),
            "Left line detected: {}".format(lane_validation_result.left_line_detected),
            "Right line detected: {}".format(lane_validation_result.right_line_detected),
            "Width deviation: {}".format(lane_validation_result.width_deviation),
            "Vanishing point distance: {}".format(vanishing_point_distance)
        ]

        if lane_validation_result.lane_is_lost:
            texts.insert(0, "Lane lost: {}".format(lane_validation_result.message))
        else:
            texts.insert(0, "Lane detected")
            texts.append("Lane curvature radius: {:.0f} m".format(lane.radius_m))
            texts.append("Car is on lane: {}".format(lane_validation_result.car_is_on_lane))

        return texts

    @staticmethod
    def print(image, texts):
        line_height = 40
        v_position = 50
        for text in texts:
            cv2.putText(image, text, (10, v_position), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            v_position += line_height
