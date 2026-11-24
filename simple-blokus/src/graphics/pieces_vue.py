from typing import Tuple, Union
import pygame
from game.game import Game
from game.piece import Piece
from graphics.colors import Colors


class PiecesVue:

    def __init__(self, game: Game, board_rect: pygame.Rect, padding: int = 60):
        self.__game = game
        self.__board_rect = board_rect
        self.__padding = padding

    def __draw_piece(self, window: pygame.Surface, piece: Piece, rect: pygame.Rect, color: tuple, selected: bool = False):
        block_size = rect.width // (Piece.MAX_X - Piece.MIN_X + 1)
        for dx, dy in piece.get_blocks():
            block_rect = pygame.Rect(rect.x + (dx - Piece.MIN_X) * block_size, rect.y + (dy - Piece.MIN_Y)
                                     * block_size, block_size + 1, block_size + 1)
            pygame.draw.rect(window, color, block_rect)
            pygame.draw.rect(window, Colors.BLACK, block_rect, 1)
            if (dx, dy) == (0, 0):
                pygame.draw.circle(window, Colors.WHITE, block_rect.center, 2)
        if selected:
            pygame.draw.rect(window, Colors.BLACK, (rect.x, rect.y, rect.w + 1, rect.h + 1), 1)

    def draw(self, window: pygame.Surface, selected_piece: Union[int, None] = None):
        piece_size = 50
        piece_padding = 10
        columns = 3
        x_padding = (self.__board_rect.left - (piece_size + piece_padding) * columns) // 2

        player1_pieces = self.__game.get_players()[0].get_pieces()
        player2_pieces = self.__game.get_players()[1].get_pieces()

        for i, piece in enumerate(player1_pieces):
            if piece.is_placed():
                continue
            col = i % columns
            row = i // columns
            piece_rect = pygame.Rect(self.__board_rect.left - (piece_size + piece_padding) * (columns - col) - x_padding,
                                     self.__board_rect.top + row * (piece_size + piece_padding) + self.__padding, piece_size, piece_size)
            self.__draw_piece(window, piece, piece_rect, Colors.ORANGE, selected_piece == i and self.__game.get_current_player().get_id() == 1)

        for i, piece in enumerate(player2_pieces):
            if piece.is_placed():
                continue
            col = i % columns
            row = i // columns
            piece_rect = pygame.Rect(self.__board_rect.right + x_padding + col * (piece_size + piece_padding),
                                     self.__board_rect.top + row * (piece_size + piece_padding) + self.__padding, piece_size, piece_size)
            self.__draw_piece(window, piece, piece_rect, Colors.PURPLE, selected_piece == i and self.__game.get_current_player().get_id() == 2)

    def get_piece_index_at(self, mouse_pos: Tuple[float, float]) -> int:
        piece_size = 50
        piece_padding = 10
        columns = 3
        x_padding = (self.__board_rect.left - (piece_size + piece_padding) * columns) // 2

        player1_pieces = self.__game.get_players()[0].get_pieces()
        player2_pieces = self.__game.get_players()[1].get_pieces()

        for i, piece in enumerate(player1_pieces):
            if self.__game.get_current_player().get_id() != 1:
                break
            if piece.is_placed():
                continue
            col = i % columns
            row = i // columns
            piece_rect = pygame.Rect(self.__board_rect.left - (piece_size + piece_padding) * (columns - col) - x_padding,
                                     self.__board_rect.top + row * (piece_size + piece_padding) + self.__padding, piece_size, piece_size)
            if piece_rect.collidepoint(mouse_pos):
                return i

        for i, piece in enumerate(player2_pieces):
            if self.__game.get_current_player().get_id() != 2:
                break
            if piece.is_placed():
                continue
            col = i % columns
            row = i // columns
            piece_rect = pygame.Rect(self.__board_rect.right + x_padding + col * (piece_size + piece_padding),
                                     self.__board_rect.top + row * (piece_size + piece_padding) + self.__padding, piece_size, piece_size)
            if piece_rect.collidepoint(mouse_pos):
                return i

        return None
