from backend.position import Position
from backend.piece import Piece
from backend.player import Player
from copy import copy


class Board:
    def __init__(self, white=Player(), black=Player(), empty_tiles=Player()):
        self.white = white
        self.black = black
        self.empty_tiles = empty_tiles
        self.eaten = {}

    def get_white(self):
        return self.white.get_all_pieces()

    def get_black(self):
        return self.black.get_all_pieces()

    def get_empty_tiles(self):
        return self.empty_tiles.get_all_pieces()

    def get_eaten(self):
        return self.eaten

    def is_move_position_in_board(self):
        for piece in self.get_empty_tiles():
            if piece.get_color() == "*":
                return True
            else:
                return False

    def get_player_by_piece(self, piece):
        if piece in self.get_white():
            return self.get_white()
        elif piece in self.get_black():
            return self.get_black()
        elif piece in self.get_empty_tiles():
            return self.get_empty_tiles()
        else:
            return False

    def get_all_pieces(self):
        all_pieces = []
        white_pieces = self.get_white()
        black_pieces = self.get_black()
        empty_pieces = self.get_empty_tiles()
        grouped_pieces = [white_pieces, black_pieces, empty_pieces]
        for index in range(len(grouped_pieces)):
            for piece in grouped_pieces[index]:
                all_pieces.append(piece)
        return all_pieces

    def create_players(self):
        for row in range(8):
            for column in range(8):
                if ((row < 3)or(row > 4))and((row+column) % 2 == 0):
                    if row < 3:
                        self.white.set_pieces(Piece(row, column, "X", is_king=False))
                    elif row > 4:
                        self.black.set_pieces(Piece(row, column, "O"))
                else:
                    self.empty_tiles.set_pieces(Piece(row, column, ""))

    def clear_eaten(self):
        self.eaten = {}

    def remove_piece_from_game(self, position):
        piece = self.get_piece_by_position(position)
        player = self.get_player_by_piece(piece)
        piece.set_color("")
        if player:
            piece.set_color("")
            player.remove(piece)
            self.empty_tiles.set_pieces(piece)

    def add_eaten(self, key, position):
        string_key = str(key)
        if string_key in self.eaten.keys():
            self.eaten[string_key].append(position)
        else:
            self.eaten[string_key] = []
            self.eaten[string_key].append(position)

    def set_white_piece(self, piece):
        self.white.set_pieces(piece)

    def set_black_piece(self, piece):
        self.black.set_pieces(piece)

    def set_empty_tiles(self, piece):
        self.empty_tiles.set_pieces(piece)

    def is_piece_playable(self, piece):
        if (piece in self.get_white()) or (piece in self.get_black()):
            return True
        return False

    def king_impossible_moves(self, picked_piece,  possible_moves, eat_turn=False):
        output = []
        if isinstance(possible_moves, dict):
            for key in possible_moves:
                last_position = []
                last_color = None
                for index in range(len(possible_moves[key])):
                    position = possible_moves[key][index]
                    piece = self.get_piece_by_position(position)
                    if not self.is_piece_playable(piece):
                        if not eat_turn:
                            output.append(position)
                        if bool(last_color):
                            for k in range(index, len(possible_moves[key])):
                                position2 = possible_moves[key][k]
                                self.add_eaten(position2, last_position)

                            if eat_turn:
                                output.append(position)

                    elif last_color == picked_piece.get_color() or last_color == piece.get_color():
                        break

                    last_position = position
                    last_color = piece.get_color()
        print(self.get_eaten())
        return output

    def eat(self, piece, tile):
        row, column = piece.get_position()
        row2, column2 = tile.get_position()
        row3 = (row2-row)*2+row
        column3 = (column2-column)*2+column
        if not (row3 > 7 or column3 > 7 or row3 < 0 or column3 < 0):
            position = [row3, column3]
            piece3 = self.get_piece_by_position(position)
            if piece3.get_color() == "":
                self.add_eaten(position, tile.get_position_as_list())
                return position

    def move_king(self, picked_piece, possible_positions, eat_turn=False):
        possible_positions = self.king_impossible_moves(picked_piece, possible_positions, eat_turn)
        print(possible_positions)
        li = []
        for position in possible_positions:
            tile = self.get_piece_by_position(position)
            if tile.get_color() == "":
                li.append(position)
        return li

    def move_not_king(self, picked_piece, possible_positions, eat_this_turn=False):
        li = []
        for position in possible_positions:
            tile = self.get_piece_by_position(position)
            if self.is_piece_playable(tile):
                if picked_piece.get_color() != tile.get_color():
                    eat_position = self.eat(picked_piece, tile)
                    if bool(eat_position):
                        li.append(self.eat(picked_piece, tile))
                else:
                    pass
            else:
                if not eat_this_turn:
                    li.append(position)
        return li

    def move(self, picked_piece, eat_turn=False):
        possible_positions = picked_piece.possible_move()
        if picked_piece.get_is_king():
            return self.move_king(picked_piece, possible_positions, eat_turn)
        else:
            return self.move_not_king(picked_piece, possible_positions, eat_turn)

    def update_piece(self, position, color):
        piece = self.get_piece_by_position(position)
        print(["aaa",position,piece.get_color(),color])
        if piece.get_color() != color:
            piece.set_color(color)

    def update_pieces(self, positions, color):
        for position in positions:
            self.update_piece(position, color)

    def get_line_row(self, row):
        row_pieces = []
        for column in range(8):
            tile = self.get_piece_by_position([row, column])
            if tile is not None:
                row_pieces.append(tile.get_all_piece_information())
        return row_pieces

    def get_piece_by_position(self, position):
        for piece in self.get_all_pieces():
            if position == piece.get_position_as_list():
                return piece
        return None

    def switch_pieces(self, piece_one, piece_two):
        temp_position = piece_one.get_position_as_list()
        piece_one.set_position(piece_two.get_position_as_list())
        piece_two.set_position(temp_position)
        for piece in [piece_one, piece_two]:
            piece.set_is_king()

    def clean(self):
        all_pieces = self.get_empty_tiles()
        for piece in all_pieces:
            if piece.get_color() == "*":
                self.update_piece(piece.get_position_as_list(), "")

    def no_possible_move(self, color):
        pieces = None
        if color == "X":
            pieces = self.get_white()
        else:
            pieces = self.get_black()
        for piece in pieces:
            if bool(self.move(piece)):
                return False
        return True
