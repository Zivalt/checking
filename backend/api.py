from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from copy import copy
from backend.position import Position
from backend.piece import Piece
from backend.board import Board
from backend.turn import Turn
template_folder_path = os.path.abspath('./frontend/src')
app = Flask(__name__, template_folder=template_folder_path)
CORS(app)


board = Board()
turn = Turn(player="red", eat_turn=False)
output_json = {}
check = False
rows = {}
@app.route("/", methods=['GET'])
def board_output():

    for row in range(8):
        rows["row"+str(row)] = board.get_line_row(row)
    output_json["board"] = rows
    output_json["turn"] = turn.get_player()
    return jsonify(output_json)


@app.route('/restart', methods=['GET'])
def restart():
    board.reset()
    turn.set_player("red")
    return "OK"


@app.route('/pick', methods=['POST'])
def post():
    requested_data = request.get_json()
    data = requested_data["data"]
    if data != "":
        click_piece = board.get_piece_by_position(data["position"])
        picked_piece = board.get_picked_piece()
        pieces_can_eat = board.get_eating_pieces(turn.get_player())
        can_piece_eat = click_piece.get_position() in pieces_can_eat
        if click_piece.get_color() == "*" and bool(picked_piece):
            moving_turn(picked_piece, click_piece)
        elif click_piece.get_color() == turn.get_player()\
                and(can_piece_eat or pieces_can_eat == [])\
                and not turn.get_eat_turn():
            player_turn(click_piece, can_piece_eat)
    elif not turn.get_eat_turn():
        board.clean()

    return jsonify(output_json)


def moving_turn(chosen_piece, click_piece):
    flag = board.get_between_pieces(
        chosen_piece.get_position(),
        click_piece.get_position())
    board.switch_pieces(chosen_piece, click_piece)
    board.clean()
    if flag:
        board.remove_piece(flag)

    eaten = board.move(chosen_piece, eat_turn=True)
    if bool(eaten) and flag:
        additional_jumps(eaten, chosen_piece)
    else:
        no_jumps(chosen_piece)


def additional_jumps(eaten, chosen_piece):
    turn.set_eat_turn(True)
    board.add_move_pieces(eaten)
    chosen_piece.set_is_picked(True)


def no_jumps(chosen_piece):
    turn.change_player()
    chosen_piece.set_is_picked(False)
    turn.set_eat_turn(False)


def player_turn(click_piece, flag):
    board.clean()
    click_piece.set_is_picked(True)
    moves = board.move(click_piece, flag)
    if bool(moves):
        board.add_move_pieces(moves)


app.run(port=5000, debug=True)
