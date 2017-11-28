class LaneLine:

    def __init__(self, start_x, line_factory):
        self.start_x = start_x
        self.line_factory = line_factory
        self.current_line = None
        self.detection_area_mask = None

    def detect(self, bw_image):
        self.current_line = self.line_factory.get_line(bw_image, self.start_x)
        self.start_x = int(self.current_line[700][0])

        return self.current_line
