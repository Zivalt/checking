from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from copy import copy
from backend.position import Position
from backend.piece import Piece
from backend.player import Player
from backend.board import Board
from backend.turn import Turn
from backend.picked import Picked
template_folder_path = os.path.abspath('./frontend/src')
app = Flask(__name__, template_folder=template_folder_path)
CORS(app)


board = Board()
board.create_players()
chosen_piece = Picked()
turn = Turn(player="red")
output_json = {}

rows = {}
@app.route("/", methods=['GET'])
def board_output():

    for row in range(8):
        rows["row"+str(row)] = board.get_line_row(row)
    output_json["board"] = rows
    output_json["turn"] = turn.get_player()
    return jsonify(output_json)


@app.route('/restart', methods=['POST'])
def restart():
    board.rest()
    board.create_players()
    turn.set_player("red")


@app.route('/pick', methods=['POST'])
def post():
    requested_data = request.get_json()
    data = requested_data["data"]
    click_piece = board.get_piece_by_position(data["position"])

    if click_piece.get_color() == "*":
        if chosen_piece.get_piece().is_player_piece():
            board.switch_pieces(click_piece, chosen_piece.get_piece())
            board.clean()
            eaten = board.get_eaten()
            board.clear_eaten()
            if not bool(eaten):
                turn.change_player()

            else:
                key = str(chosen_piece.get_piece().get_position_as_list())
                if key in eaten.keys():
                    for position in eaten[key]:
                        board.remove_piece_from_game(position)
                    move = board.move(chosen_piece.get_piece(), eat_turn=True)
                    if bool(move):
                        board.update_pieces(move, "*")
                    else:
                        turn.change_player()
                else:
                    turn.change_player()

    elif click_piece.get_color() == turn.get_player():
        board.clean()
        chosen_piece.set_piece(click_piece)
        move = board.move(click_piece)
        if bool(move):
            board.update_pieces(move, "*")
        else:
            pass

    else:
        board.clean()

    if board.no_possible_move(turn.get_player()):
        return jsonify(click_piece.get_color()+"have won")
    return jsonify(output_json)


app.run(port=5000, debug=True)
