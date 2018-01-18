
class CurvedLine:

    def __init__(self, line_is_valid, coordinates):
        self.line_is_valid = line_is_valid
        self.line_coordinates = coordinates

    @property
    def is_valid(self):
        return self.line_is_valid

    @property
    def coordinates(self):
        return self.line_coordinates
