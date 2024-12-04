from game.piece import Piece


class Player:
    def __init__(self, color):
        self.color = color
        self.pieces = self.initialize_pieces()
        self.score = 0

    def __str__(self):
        return f'Player {self.color} has score {self.score}'

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
        pieces.add(Piece(self.color, [(0, 0), (-1, 0), (0, -1), (0, -2), (0, -3)]))
        pieces.add(Piece(self.color, [(0, 0), (0, -1), (0, -2), (1, 0), (2, 0)]))
        pieces.add(Piece(self.color, [(0, 0), (-1, 0), (-1, 1), (0, -1), (0, -2)]))
        pieces.add(Piece(self.color, [(0, 0), (0, -1), (0, 1), (-1, 0), (-1, 1)]))
        pieces.add(Piece(self.color, [(0, 0), (0, -1), (0, 1), (-1, -1), (1, 1)]))
        pieces.add(Piece(self.color, [(0, 0), (0, -1), (0, 1), (0, 2), (1, 0)]))
        pieces.add(Piece(self.color, [(0, 0), (0, -1), (0, -2), (-1, 0), (1, 0)]))
        pieces.add(Piece(self.color, [(0, 0), (0, -1), (0, -2), (1, 0), (2, 0)]))
        pieces.add(Piece(self.color, [(0, 0), (0, -1), (-1, -1), (1, 0), (1, 1)]))
        pieces.add(Piece(self.color, [(0, 0), (-1, 0), (-1, -1), (1, 0), (1, 1)]))
        pieces.add(Piece(self.color, [(0, 0), (0, 1), (-1, -1), (-1, 0), (1, 0)]))
        pieces.add(Piece(self.color, [(0, 0), (0, -1), (0, 1), (-1, 0), (1, 0)]))
        return pieces

    def update_score(self):
        self.score += self.count_score()

    def count_score(self):
        score = 0
        for piece in self.pieces:
            score += piece.get_points()
        return score

    def remove_piece(self, piece):
        if piece in self.pieces:
            self.pieces.remove(piece)
            print(f"Pièce {piece.shape} supprimée pour le joueur {self.color}.")
            return True
        else:
            print(f"Erreur : la pièce {piece.shape} n'est pas disponible pour le joueur {self.color}.")
            return False