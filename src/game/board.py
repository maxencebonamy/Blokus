from game.cell import Cell
from utils.colors import Colors


class Board:

    SIZE = 14

    def __init__(self):
        self.cells = []
        for x in range(0, Board.SIZE):
            for y in range(0, Board.SIZE):
                self.cells.append(Cell(x, y))
        self.cells[0].set_color(Colors.RED.value)

    def draw(self, screen):
        for cell in self.cells:
            cell.draw(screen)
