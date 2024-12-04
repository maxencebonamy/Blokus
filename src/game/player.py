from game.piece import Piece
from game.score_label import ScoreLabel
from game.pieces_panel import PiecesPanel


class Player:

    def __init__(self, color):
        self.color = color
        self.pieces = self.initialize_pieces()
        self.score = 0

        self.label = ScoreLabel(self.color, self.score)
        self.pieces_panel = PiecesPanel(self.pieces)

    def __str__(self):
        return f"Player {self.color} has score {self.score}"

    def initialize_pieces(self):
        pieces = set()
        pieces.add(Piece(self.color, [(0, 0)]))
        pieces.add(Piece(self.color, [(0, 0), (0, -1)]))
        pieces.add(Piece(self.color, [(0, 0), (0, 1), (0, -1)]))
        pieces.add(Piece(self.color, [(0, 0), (0, -1), (1, 0)]))
        pieces.add(Piece(self.color, [(0, 0), (0, -1), (0, -2), (0, 1)]))
        pieces.add(Piece(self.color, [(0, 0), (0, -1), (0, -2), (-1, 0)]))
        pieces.add(Piece(self.color, [(0, 0), (0, -1), (0, 1), (1, 0)]))
        pieces.add(Piece(self.color, [(0, 0), (0, 1), (1, 1), (1, 0)]))
        pieces.add(Piece(self.color, [(0, 0), (-1, 0), (0, 1), (1, 1)]))
        pieces.add(Piece(self.color, [(0, 0), (0, -1), (0, -2), (0, 1), (0, 2)]))
        pieces.add(Piece(self.color, [(0, 0), (-1, -1), (0, -1), (0, -1), (0, -2)]))
        pieces.add(Piece(self.color, [(0, 0), (0, -1), (0, -2), (1, 0), (2, 0)]))
        pieces.add(Piece(self.color, [(0, 0), (-1, 0), (-1, 1), (0, -1), (0, -2)]))
        pieces.add(Piece(self.color, [(0, 0), (0, -1), (0, 1), (-1, 0), (-1, 1)]))
        pieces.add(Piece(self.color, [(0, 0), (0, -1), (0, 1), (-1, -1), (1, 1)]))
        pieces.add(Piece(self.color, [(0, 0), (0, -1), (0, 1), (0, 2), (1, 0)]))
        pieces.add(Piece(self.color, [(0, 0), (0, -1), (0, -2), (-1, 0), (1, 0)]))
        pieces.add(Piece(self.color, [(0, 0), (0, -1), (0, -2), (1, 0), (2, 0)]))
        pieces.add(Piece(self.color, [(0, 0), (0, -1), (-1, -1), (1, 0), (1, 1)]))
        # pieces.add(Piece(self.color, [(0, 0), (-1, 0), (-1, -1), (1, 0), (1, 1)]))
        pieces.add(Piece(self.color, [(0, 0), (0, 1), (-1, -1), (-1, 0), (1, 0)]))
        pieces.add(Piece(self.color, [(0, 0), (0, -1), (0, 1), (-1, 0), (1, 0)]))
        return pieces

    def add_score(self, score):
        self.score += score
        self.label = ScoreLabel(self.color, self.score)

    def remove_piece(self, piece):
        if piece in self.pieces:
            self.pieces.remove(piece)
            return True
        return False
