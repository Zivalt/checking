class Position:
    def __init__(self, x=8, y=8):
        self.x = x
        self.y = y

    def get_position(self):
        return self.x, self.y

    def get_position_as_list(self):
        return [self.x, self.y]

    def set_position(self, position):
        self.x = position[0]
        self.y = position[1]

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y