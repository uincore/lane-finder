
class CurvedLine:

    def __init__(self, line_image, line_is_valid, raw_points, coordinates):
        self.line_image = line_image
        self.line_is_valid = line_is_valid
        self.raw_points = raw_points
        self.coordinates = coordinates

    @property
    def image(self):
        return self.line_image

    @property
    def is_valid(self):
        return self.line_is_valid

    @property
    def line_coordinates(self):
        return self.coordinates
