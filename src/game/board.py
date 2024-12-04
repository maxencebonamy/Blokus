from game.cell import Cell
from utils.colors import Colors
import random


class Board:

    SIZE = 14

    def __init__(self, game):
        self.x = (game.WIDTH - self.compute_size()) // 2
        self.y = (game.HEIGHT - self.compute_size()) // 2

        self.cells = []
        for i in range(0, Board.SIZE):
            for j in range(0, Board.SIZE):
                self.cells.append(Cell(j, i))

        for _ in range(0, 10):
            self.cells[random.randint(0, len(self.cells) - 1)].set_color(Colors.PURPLE.value)
        for _ in range(0, 10):
            self.cells[random.randint(0, len(self.cells) - 1)].set_color(Colors.ORANGE.value)

    def compute_size(self):
        return Board.SIZE * Cell.SIZE

    def draw(self, screen):
        for cell in self.cells:
            cell.draw(screen, self.x, self.y)

    def search_cell(self, x, y):
        index = y * Board.SIZE + x
        return self.cells[index]

    def place_piece(self, piece, x, y):

        for bloc in piece.blocs:

            # Cell is out of the board
            if (x + bloc[0] < 0 or x + bloc[0] > Board.SIZE or y + bloc[1] < 0 or y + bloc[1] > Board.SIZE):
                return False
            # Cell is not empty
            cell = self.search_cell(x + bloc[0], y + bloc[1])
            if cell.color != Colors.WHITE.value:
                return False
            
        if(not self.__verify_place(piece, x, y)):
            return False

        for bloc in piece.blocs:
            cell = self.search_cell(x + bloc[0], y + bloc[1])
            cell.set_color(piece.color)
        return True

    def __verify_place(self, piece, x, y):
        adjacent_cells = []
        diagonals_cells = []

        for bloc in piece.blocs:
            adjacents, diagonals = self.__neighbour_cells(bloc, x, y)
            adjacent_cells += adjacents
            diagonals_cells += diagonals
        
        # Check if the adjacent cells don't have the same color
        for cell in adjacent_cells:
            if self.search_cell(cell[0], cell[1]).color == piece.color:
                return False
        
        # Check if one of diagonals cells have the same color
        for cell in diagonals_cells:
            if self.search_cell(cell[0], cell[1]).color == piece.color:
                return True
        
        return False


    def __neighbour_cells(self, bloc , x, y):
        adjacents = []
        diagonals = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if (x + i < 0 or x + i > Board.SIZE or y + j < 0 or y + j > Board.SIZE):
                    continue
                if i == 0 or j == 0:
                    adjacents.append((x + i, y + j))
                else:
                    diagonals.append((x + i, y + j))
        return (adjacents, diagonals)



            

