from game.cell import Cell
from utils.colors import Colors
import random


class Board:

    SIZE = 14

    def __init__(self):
        self.cells = []
        for x in range(0, Board.SIZE):
            for y in range(0, Board.SIZE):
                self.cells.append(Cell(x, y))

        for _ in range(0, 10):
            self.cells[random.randint(0, len(self.cells) - 1)].set_color(Colors.PURPLE.value)
        for _ in range(0, 10):
            self.cells[random.randint(0, len(self.cells) - 1)].set_color(Colors.ORANGE.value)

    @property
    def compute_size(self):
        return Board.SIZE * Cell.SIZE

    def draw(self, screen, x, y):
        for cell in self.cells:
            cell.draw(screen, x, y)

    def search_cell(self, x, y):
        index = y * Board.SIZE + x
        return self.cells[index]
    
    def place_piece(self, piece, x, y):
        for bloc in piece.blocs:
            cell = self.search_cell(x + bloc[0], y + bloc[1])
            cell.set_color(piece.color)
