from backend.position import Position
from backend.piece import Piece
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

