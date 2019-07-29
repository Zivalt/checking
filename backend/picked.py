from backend.piece import Piece


class Picked:

    def __init__(self, piece=Piece()):
        self.piece = piece

    def get_piece(self):
        return self.piece

    def set_piece(self, piece=Piece()):
        self.piece = piece
