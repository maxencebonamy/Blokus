from game.cell import Cell
from game.piece import Piece
import numpy as np


BoardState = np.ndarray


class Board:

    def __init__(self, size: int, game):
        self.__size = size
        self.__game = game
        self.__cells = [[Cell(x, y) for x in range(size)] for y in range(size)]

    def get_size(self) -> int:
        return self.__size

    def get_cell(self, x: int, y: int) -> Cell:
        return self.__cells[y][x]

    def can_be_placed(self, piece: Piece, player_id: int) -> bool:
        for y in range(self.__size):
            for x in range(self.__size):
                if self.is_valid_position(piece, x, y, player_id):
                    return True
        return False

    def is_valid_position(self, piece: Piece, x: int, y: int, player_id: int) -> bool:
        player = self.__game.get_players()[player_id - 1]
        if player.is_started() and not self.__verify_neighbour_cells(x, y, piece, player_id):
            return False
        for dx, dy in piece.get_blocks():
            if not (0 <= x + dx < self.__size and 0 <= y + dy < self.__size):
                return False
            if not self.get_cell(x + dx, y + dy).is_empty():
                return False
        return True

    def place_piece(self, piece: Piece, x: int, y: int, player_id: int) -> bool:
        if piece.is_placed():
            return False
        if not self.is_valid_position(piece, x, y, player_id):
            return False
        for dx, dy in piece.get_blocks():
            self.__cells[y + dy][x + dx].set_state(player_id)
        player = self.__game.get_players()[player_id - 1]
        if not player.is_started():
            player.set_started(True)
        piece.place()
        return True

    def get_state(self) -> BoardState:
        return np.array([[cell.get_state() for cell in row] for row in self.__cells])

    def __verify_neighbour_cells(self, x: int, y: int, piece: Piece, player_id: int) -> bool:
        adjacent_cells = []
        temp_diagonal_cells = []
        diagonals_cells = []

        blocks = piece.get_blocks()
        for block in blocks:
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if (block[0] + i, block[1] + j) in blocks:
                        continue
                    if not (0 <= x + block[0] + i < self.__size) or not (0 <= y + block[1] + j < self.__size):
                        continue
                    if i == 0 or j == 0:
                        if ((x + block[0] + i, y + block[1] + j) not in adjacent_cells):
                            adjacent_cells.append((x + block[0] + i, y + block[1] + j))
                    else:
                        if ((x + block[0] + i, y + block[1] + j) not in temp_diagonal_cells):
                            temp_diagonal_cells.append((x + block[0] + i, y + block[1] + j))

        for cell in temp_diagonal_cells:
            if cell not in adjacent_cells and cell not in diagonals_cells:
                diagonals_cells.append(cell)

        for cell in adjacent_cells:
            if self.get_cell(cell[0], cell[1]).get_state() == player_id:
                return False

        for cell in diagonals_cells:
            if self.get_cell(cell[0], cell[1]).get_state() == player_id:
                return True

        return False
