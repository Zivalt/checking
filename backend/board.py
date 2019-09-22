from backend.position import Position
from backend.piece import Piece
from backend.piece import position_bounds
from copy import copy


class Board:
    def __init__(self):
        self.pieces = []
        self.empty_pieces = []
        self.init_board()

    def get_pieces(self):
        return self.pieces

    def add_piece(self, piece):
        self.pieces.append(piece)

    def get_empty_pieces(self):
        return self.empty_pieces

    def set_empty_pieces(self, piece):
        self.empty_pieces.append(piece)

    def init_board(self):
        for row in range(3):
            for column in range(8):
                if (row+column) % 2 == 0:
                    self.add_piece(
                        Piece(row, column, "red", is_king=False))
                else:
                    self.add_piece(Piece(7-row, column, "black"))

    def remove_piece_from_game(self, position):
        piece = self.get_piece_by_position(position)
        pieces = self.get_pieces()
        pieces.remove(piece)

    def is_piece_playable(self, piece):
        if piece in self.get_pieces():
            return True
        return False

    def eat(self, position_one, position_two):
        jump_position = [
            difference(position_one[0], position_two[0]),
            difference(position_one[1], position_two[1])]
        jump_piece = self.get_piece_by_position(jump_position)
        if not (jump_piece in self.get_pieces())\
                and position_bounds(
                jump_position[0], jump_position[1]):
            return jump_position

    def move(self, picked_piece, eat_turn=False):
        possible_positions = picked_piece.possible_move()
        print(possible_positions)
        piece_moves = []
        for position in possible_positions:
            tile = self.get_piece_by_position(position)
            if bool(tile):
                piece_moves.append(
                    self.check_eating(picked_piece, tile))
            elif not eat_turn:
                piece_moves.append(position)
        return list(filter(None, piece_moves))

    def update_piece(self, position, color):
        piece = self.get_piece_by_position(position)
        if piece.get_color() != color:
            piece.set_color(color)

    def get_line_row(self, row):
        row_pieces = []
        for column in range(8):
            tile = self.get_piece_by_position([row, column])
            if tile is not None:
                row_pieces.append(tile.get_all_piece_information())
        return row_pieces

    def get_piece_by_position(self, position):
        for piece in self.get_pieces()+self.get_empty_pieces():
            if position == piece.get_position_as_list():
                return piece
        return None

    def switch_pieces(self, piece_one, piece_two):
        piece_one.set_position(piece_two.get_position_as_list())
        piece_one.set_is_king()

    def clean(self):
        self.empty_pieces = []
        picked = self.get_picked_piece()
        if bool(picked):
            picked.set_is_picked(False)

    def no_possible_move(self):
        pieces = self.get_pieces()
        for piece in pieces:
            if bool(self.move(piece)):
                return False
        return True

    def reset(self):
        self.__init__()

    def remove_piece(self, piece):
        if piece in self.get_pieces():
            self.get_pieces().remove(piece)

    def get_picked_piece(self):
        for piece in self.get_pieces():
            if piece.get_is_picked():
                return piece

    def add_move_pieces(self, moves):
        for position in moves:
            if position is not None:
                self.empty_pieces.append(
                    Piece(position[0], position[1], "*"))

    def get_between_pieces(self, position_one, position_two):
        position_three = [mean(position_two[0], position_one[0]),
                          mean(position_two[1], position_one[1])]
        piece = self.get_piece_by_position(position_three)
        if piece in self.get_pieces():
            return piece

    def check_eating(self, picked_piece, tile):
        if picked_piece.get_color() != tile.get_color()\
                and tile in self.get_pieces():
            eat_position = self.eat(
                picked_piece.get_position(), tile.get_position())
            if bool(eat_position):
                return eat_position

    def get_eating_pieces(self, color):
        li = []
        for piece in self.get_pieces():
            if piece.get_color() == color:
                can_eat = self.move(piece, True)
                if not can_eat == []:
                    li.append(piece.get_position())
        return li


def difference(num, num2):
    return num2*2-num


def mean(num, num2):
    return num+(num2-num)/2
