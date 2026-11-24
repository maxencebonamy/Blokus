from typing import Tuple, Union
import pygame
from graphics.colors import Colors
from game.cell import CellState
from game.game import Game


class BoardVue:

    def __init__(self, game: Game, padding: int = 20):
        self.__game = game
        self.__board = game.get_board()
        self.__padding = padding

    def __get_cell_color(self, cell):
        if cell.get_state() == CellState.PLAYER_1:
            return Colors.ORANGE
        elif cell.get_state() == CellState.PLAYER_2:
            return Colors.PURPLE
        else:
            return Colors.WHITE

    def draw(self, window: pygame.Surface):
        board_size = self.__board.get_size()
        cell_size = (window.get_height() - 2 * self.__padding) // board_size
        offset_x = (window.get_width() - (cell_size * board_size)) // 2
        offset_y = self.__padding

        for y in range(board_size):
            for x in range(board_size):
                cell = self.__board.get_cell(x, y)
                rect = (offset_x + x * cell_size, offset_y + y * cell_size, cell_size + 1, cell_size + 1)
                pygame.draw.rect(window, self.__get_cell_color(cell), rect)
                pygame.draw.rect(window, Colors.BLACK, rect, 1)

    def get_rect(self, window: pygame.Surface) -> pygame.Rect:
        board_size = self.__board.get_size()
        cell_size = (window.get_height() - 2 * self.__padding) // board_size
        offset_x = (window.get_width() - (cell_size * board_size)) // 2
        offset_y = self.__padding
        return pygame.Rect(offset_x, offset_y, cell_size * board_size, cell_size * board_size)

    def get_cell_at(self, mouse_pos: Tuple[float, float]) -> Union[Tuple[int, int], None]:
        rect = self.get_rect(pygame.display.get_surface())
        if not rect.collidepoint(mouse_pos):
            return None
        cell_size = rect.width // self.__board.get_size()
        x = (mouse_pos[0] - rect.x) // cell_size
        y = (mouse_pos[1] - rect.y) // cell_size
        return x, y
