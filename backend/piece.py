from backend.position import Position


class Piece(Position):
    def __init__(self, x=9, y=9, color="", is_king=False):
        Position.__init__(self, x, y)
        self.color = color
        self.is_king = is_king

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color

    def get_is_king(self):
        return self.is_king

    def set_is_king(self):
        if (self.get_x() == 0 and self.get_color() == "O") or (self.get_x() == 7 and self.get_color() == "X"):
            print("meow")
            self.is_king = True

    def is_player_piece(self):
        if (self.color == "X") or (self.color == "O"):
            return True
        return False

    def get_all_piece_information(self):
        return {"position": self.get_position(),
                "color": self.get_color(),
                "is_king": self.get_is_king()}

    def possible_move(self):
        row, column = self.get_position()
        if self.get_is_king():
            return self.king_possible_move(row, column)
        else:
            return self.not_king_possible_move(row, column)

    def not_king_possible_move(self, row, column):
        moves = []
        if self.color == "X":
            if column > 0:
                moves.append([row+1, column-1])
            if column < 7:
                moves.append([row+1, column+1])

        if self.color == "O":
            if column > 0:
                moves.append([row - 1, column - 1])
            if column < 7:
                moves.append([row - 1, column + 1])
        return moves

    def king_possible_move(self, row, column):
        possible_moves = {}
        for i in range(4):
            possible_moves[i] = []
        for i in range(1, 7, 1):
            print(row+i > 7 or column+i > 7) and (row - i < 0 or column-i < 0)
            if not (row+i > 7) and (column+i > 7) and (row - i < 0) and (column-i < 0):
                break
            else:
                if(row + i <= 7) and (column + i <= 7):
                    possible_moves[0].append([row+i, column+i])
                if(row + i <= 7) and (column - i >= 0):
                    possible_moves[1].append([row+i, column-i])
                if(row - i >= 0) and (column + i <= 7):
                    possible_moves[2].append([row - i, column + i])
                if(row - i >= 0) and (column - i >= 0):
                    possible_moves[3].append([row - i, column - i])

        return possible_moves

    def possible_eat(self):
        row, column = self.get_position()
        moves = []
        if self.color == "X":
            if row < 6:
                if column > 1:
                    moves.append([row + 2, column - 2])
                if column < 6:
                    moves.append([row + 2, column + 2])

        elif self.color == "O":
            if row > 1:
                if column > 1:
                    moves.append([row - 2, column - 2])
                if column < 6:
                    moves.append([row - 2, column + 2])
        return moves