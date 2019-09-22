from backend.position import Position


class Piece(Position):
    def __init__(self, x, y, color, is_king=False, is_picked=False):
        Position.__init__(self, x, y)
        self.color = color
        self.is_king = is_king
        self.is_picked = is_picked

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color

    def get_is_king(self):
        return self.is_king

    def set_is_king(self):
        if (self.get_x() == 0 and self.get_color() == "black")\
                or (self.get_x() == 7 and self.get_color() == "red"):
            self.is_king = True

    def get_is_picked(self):
        return self.is_picked

    def set_is_picked(self, flag):
        self.is_picked = flag

    def is_player_piece(self):
        if (self.color == "red") or (self.color == "black"):
            return True
        return False

    def get_all_piece_information(self):
        return {"position": self.get_position(),
                "color": self.get_color(),
                "is_king": self.get_is_king()}

    def possible_move(self):
        row, column = self.get_position()
        if not self.get_is_king():
            return self.not_king_possible_move(row, column)
        else:
            return king_possible_move(row, column)

    def not_king_possible_move(self, row, column):
        if self.get_color() == "red":
            return red_possible_move(row, column)
        elif self.get_color() == "black":
            return black_possible_move(row, column)


def king_possible_move(row, column):

    return (red_possible_move(row, column))\
             +(black_possible_move(row, column))


def something(li):
    if not li == []:
        if isinstance(li[0], list):
            return li
        else:
            return [li]


def red_possible_move(row, column):
    moves = [position_bounds(row + 1, column + 1),
             position_bounds(row + 1, column - 1)]
    return list(filter(None, moves))


def black_possible_move(row, column):
    moves = [position_bounds(row - 1, column + 1),
             position_bounds(row - 1, column - 1)]
    return list(filter(None, moves))


def position_bounds(row, column):
    if num_in_bound(row):
        if num_in_bound(column):
            return [row, column]


def num_in_bound(number):
    if 0 <= number <= 7:
        return True
    return False

