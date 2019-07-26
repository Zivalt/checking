from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from copy import copy
template_folder_path = os.path.abspath('./frontend/src')
app = Flask(__name__, template_folder=template_folder_path)
CORS(app)


class Turn:
    def __init__(self, player="X"):
        self.player = player

    def get_player(self):
        return self.player

    def set_player(self):
        if self.player == "X":
            self.player = "O"
        elif self.player == "O":
            self.player = "X"


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
        count = 0
        possible_moves = []
        while(row + count <= 7) and (column + count <= 7):
            possible_moves.append([row+count, column+count])
            count = count+1
        while(row + count <= 7) and (column - count >= 0):
            possible_moves.append([row+count, column-count])
            count = count+1
        while(row - count >= 0) and (column + count <= 7):
            possible_moves.append([row - count, column + count])
            count = count + 1
        while(row - count >= 0) and (column - count >= 0):
            possible_moves.append([row - count, column - count])
            count = count + 1
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


class Player:
    def __init__(self):
        self.pieces = []

    def set_pieces(self, piece):
        self.pieces.append(piece)

    def get_piece(self, num):
        return self.pieces[num]

    def get_all_pieces(self):
        return self.pieces

    def update_piece(self, index, piece):
        self.pieces[index] = piece

    def look_piece_in_player(self, piece):
        if piece in self.pieces:
            return self.pieces
        else:
            return False


class Board:
    def __init__(self, white=Player(), black=Player(), empty_tiles=Player()):
        self.white = white
        self.black = black
        self.empty_tiles = empty_tiles
        self.will_be_eaten = []
        self.eaten = {}

    def get_white(self):
        return self.white.get_all_pieces()

    def get_black(self):
        return self.black.get_all_pieces()

    def get_empty_tiles(self):
        return self.empty_tiles.get_all_pieces()

    def get_eaten(self):
        return self.eaten

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
                        self.white.set_pieces(Piece(row, column, "X"))
                    elif row > 4:
                        self.black.set_pieces(Piece(row, column, "O"))
                else:
                    self.empty_tiles.set_pieces(Piece(row, column, ""))

    def get_will_be_eaten(self):
        return self.will_be_eaten

    def clear_will_be_eaten(self):
        self.will_be_eaten = []

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

    def add_eaten(self, position):
        self.will_be_eaten.append(position)

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

    def eat(self, piece):
        li = []
        possible_positions = piece.possible_eat()
        for position in possible_positions:
            tile = self.get_piece_by_position(position)
            a = piece.get_position_as_list()
            b = [(position[0]-a[0])/2, (position[1]-a[1])/2]
            temp = [int(a[0]+b[0]), int(a[1]+b[1])]
            piece2 = self.get_piece_by_position(temp)
            if (self.is_piece_playable(piece2))and(piece.get_color() != piece2.get_color()):
                if tile.color == "":
                    li = li.__add__(position)
                    self.add_eaten(temp)
                    self.eaten[str(position)] = copy(self.get_will_be_eaten())

        return li

    def move(self, picked_piece):
        possible_positions = picked_piece.possible_move()
        li = []
        for position in possible_positions:
            tile = self.get_piece_by_position(position)
            if self.is_piece_playable(tile):
                if picked_piece.get_color() != tile.get_color():
                    while True:
                        something = self.eat(picked_piece)
                        if len(something) != 0:
                            for i in range(0, len(something)-1, 2):
                                picked_piece = Piece(x=something[i], y=something[i+1], color=picked_piece.get_color())
                                li.append([something[i], something[i+1]])
                        else:
                            break

            else:
                li.append(position)
        return li

    def update_piece(self, position, color):
        piece = self.get_piece_by_position(position)
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


class Picked:

    def __init__(self, piece=Piece()):
        self.piece = piece

    def get_piece(self):
        return self.piece

    def set_piece(self, piece=Piece()):
        self.piece = piece


board = Board()
board.create_players()

chosen_piece = Picked()
turn = Turn("X")
output_json = {}


rows = {}
@app.route("/", methods=['GET'])
def board_output():

    for row in range(8):
        rows["row"+str(row)] = board.get_line_row(row)
    output_json["board"] = rows
    output_json["turn"] = turn.get_player()
    return jsonify(output_json)


@app.route('/pick', methods=['POST'])
def post():
    requested_data = request.get_json()
    data = requested_data["data"]
    click_piece = board.get_piece_by_position(data["position"])
    board.clear_will_be_eaten()
    if click_piece.get_color() == turn.get_player():
        board.clean()
        chosen_piece.set_piece(click_piece)
        move = board.move(click_piece)
        board.update_pieces(move, "*")

    elif click_piece.get_color() == "*":
        if chosen_piece.get_piece().is_player_piece():
            board.switch_pieces(click_piece, chosen_piece.get_piece())
            eaten = board.get_eaten()
            for key in eaten.keys():
                if str(chosen_piece.get_piece().get_position_as_list()) == key:
                    for position in eaten[key]:
                        print(position)
                        board.clean()
                        board.remove_piece_from_game(position)

            turn.set_player()
            board.clear_eaten()

        board.clean()
    else:
        board.clean()

    return jsonify(rows)


app.run(port=5000, debug=True)
