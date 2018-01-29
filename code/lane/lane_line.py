class LaneLine:

    def __init__(self, start_x, curved_line_factory):
        self.start_x = start_x
        self.end_x = None
        self.curved_line_factory = curved_line_factory

        self.line = None

    @property
    def x_bottom(self):
        return self.start_x

    @property
    def x_top(self):
        return self.end_x

    @property
    def coordinates(self):
        return self.line.coordinates

    @property
    def radius(self):
        return self.line.radius

    @property
    def is_valid(self):
        return self.line.is_valid

    def update(self, bw_image):
        self.line = self.curved_line_factory.create(bw_image, self.start_x)

        if self.line.is_valid:
            self.start_x = int(self.line.coordinates[-20][0])
            self.end_x = int(self.line.coordinates[0][0])
