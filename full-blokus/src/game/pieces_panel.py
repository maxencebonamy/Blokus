from game.piece import Piece
from utils.colors import Colors
import pygame


class PiecesPanel:

    WIDTH = 3 * Piece.SIZE

    def __init__(self, pieces):
        self.pieces = pieces
        self.cell_to_piece = {}

    def draw(self, screen, x, y):
        for i, piece in enumerate(self.pieces):
            piece_x = x + (i % 3) * Piece.SIZE
            piece_y = y + (i // 3) * Piece.SIZE
            piece.draw(screen, piece_x, piece_y)
            pygame.draw.rect(screen, Colors.BLACK.value, (piece_x, piece_y, Piece.SIZE + 1, Piece.SIZE + 1), 1)
            self.cell_to_piece[(piece_x, piece_y)] = piece

    def get_piece_at(self, mouse_x, mouse_y):
        for (cell_x, cell_y), piece in self.cell_to_piece.items():
            rect = pygame.Rect(cell_x, cell_y, Piece.SIZE, Piece.SIZE)
            if rect.collidepoint(mouse_x, mouse_y):
                return piece
        return None

