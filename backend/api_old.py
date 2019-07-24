from flask import Flask,render_template,request,jsonify
from flask_cors import CORS
import os
template_folder_path = os.path.abspath('./frontend/src')
app = Flask(__name__, template_folder=template_folder_path)
CORS(app)

class Turn:
    def __init__(self, player="X"):
        self.player = player

    def get_player(self):
        return self.player

    def set_player(self, player):
        self.player = player


class Position:
    def __init__(self, x=8,y=8):
        self.x = x
        self.y = y

    def get_position(self):
        return self.x, self.y

    def set_position(self, x, y):
        self.x = x
        self.y = y
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y


class Piece(Position):
    def __init__(self, x=9, y=9, color="", is_king=False):
        self.set_position(x, y)
        self.color = color
        self.is_king = is_king

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color

    def get_is_king(self):
        return self.is_king

    def set_is_king(self):
        self.is_king = True

    def get_all_piece_information(self):
        return {"position": self.get_position(),
                "color": self.get_color(),
                "is_king": self.get_is_king()}

    def move_not_king(self):
        row, column = self.get_position()
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

    def move_king(self):
        row, column = self.get_position()
        count = 0
        possible_moves = []
        while(row + count <= 7) and (column + count <= 7):
            possible_moves.append(row+count, column+count)
            count = count+1
        while(row + count <= 7) and (column - count >= 0):
            possible_moves.append(row+count, column-count)
            count = count+1
        while(row - count >= 0) and (column + count <= 7):
            possible_moves.append(row - count, column + count)
            count = count + 1
        while(row - count >= 0) and (column - count >= 0):
            possible_moves.append(row - count, column - count)
            count = count + 1
        return possible_moves


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

    def piece_move(self, num):
        if self.pieces[num].get_is_king():
            self.pieces[num].move_king()
        else:
            self.pieces[num].move_not_king()

    def look_piece_in_player(self, row, column):
        for piece in self.pieces:
            x, y = piece.get_position()
            if x == row and y == column:
                return [x, y]
            else:
                pass
        return None


class Board:
    def __init__(self, white=Player(), black=Player(), empty_tiles=Player()):
        self.white = white
        self.black = black
        self.empty_tiles = empty_tiles

    def get_white(self):
        return self.white

    def get_black(self):
        return self.black
    
    def get_empty_tiles(self):
        return self.empty_tiles

    def create_players(self):
        for row in range(8):
            for column in range(8):
                if ((row < 3)or(row > 4))and((row+column) % 2 == 0):
                    if row < 3:
                        self.white.set_pieces(Piece(row, column, "X"))
                    elif row > 4:
                        self.white.set_pieces(Piece(row, column, "O"))
                else:
                    self.white.set_pieces(Piece(row, column, ""))

    def set_white_piece(self, piece):
        self.white.append(piece)

    def set_black_piece(self, piece):
        self.black.append(piece)

    def move(self, positions, picked_piece):
        li = []
        for position in positions:
            piece = self.get_piece_by_position(position)
            if piece.get_color() == "X" or piece.get_color() == "O":
                if picked_piece.get_color() != piece.get_color():
                    n = [(position[0]-picked_piece.get_x())*2, (position[1]-picked_piece.get_y())*2]
                    print([n,position, picked_piece.get_color(), "hi"])
                    temp = ([picked_piece.get_x()+n[0], picked_piece.get_y()+n[1]])
                    print([temp[0], temp[1]])
                    if ((temp[0] >= 0) and (temp[0] <= 7)) and ((temp[1] >= 0) and (temp[1] <= 7)):
                        if self.get_piece_by_position(temp).color == "":
                            li.append(temp)
            else:
                li.append(position)
        return li

    def update_piece(self, positions, color):
        for i in range(len(self.white.get_all_pieces())):
            for position in positions:
                x, y = self.white.get_piece(i).get_position()
                if [x, y] == position:
                    p = self.white.get_piece(i)
                    print(p.get_position())
                    if p.get_color() != color:
                        p.set_color(color)

        return


    def get_line_row(self, row):
        temp = []
        pieces = self.white.get_all_pieces()
        for p in pieces:
            x, y = p.get_position()
            if x == row:
                temp.append(p.get_all_piece_information())
            else:
                pass
        return temp

    def get_piece_by_position(self, position):
        for piece in self.white.get_all_pieces():
            x, y = piece.get_position()
            if position == [x, y]:
                return piece
        return None

    def clean(self):
        for i in range(len(self.white.get_all_pieces())):
            piece = self.white.get_piece(i)
            if piece.get_color() == "*":
                x, y = piece.get_position()
                self.update_piece([[x, y]], "")








def create_board():
    board = Board()
    board.create_players()
    return board


def possible_move(board,player,piece):
    for pie in board.get_white():
        pass

    return


class Picked:

    def __init__(self, piece=Piece()):
        self.piece = piece

    def get_piece(self):
        return self.piece

    def set_piece(self,piece=Piece()):
        self.piece = piece


board = create_board()
print(board.get_line_row(0))
p = Picked()
turn = Turn("X")
b = {}

white = {}
@app.route("/", methods=['GET'])
def proj():

    for i in range(8):
        white["row"+str(i)] = board.get_line_row(i)
    b["board"] = white
    b["turn"] = turn.get_player()
    return jsonify(b)


@app.route('/pick', methods=['POST'])
def post():
    data = request.get_json()
    piece = data["data"]
    if (piece["color"] == turn.get_player())or(piece["color"] == "*"):
        if (piece["color"] == "O")or(piece["color"] == "X"):
            board.clean()
            piece_in_board = board.get_piece_by_position(piece["position"])
            p.set_piece(piece_in_board)
            print(p.get_piece().get_all_piece_information())
            move = piece_in_board.move_not_king()
            move = board.move(move, piece_in_board)
            print(move)
            board.update_piece(move, "*")
        elif piece["color"] == "*":
            if p.get_piece().get_color() == "X":
                turn.set_player("O")
            elif p.get_piece().get_color() == "O":
                turn.set_player("X")
            print([p.get_piece().get_all_piece_information(), "hi"])
            board.update_piece([piece["position"]], p.get_piece().get_color())
            x, y = p.get_piece().get_position()
            board.update_piece([[x, y]], "")
            board.clean()

        else:
            board.clean()

    return jsonify(white)




app.run(port=5000, debug=True)
