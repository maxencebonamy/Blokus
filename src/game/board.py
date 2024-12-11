from game.cell import Cell
from utils.colors import Colors
from game.piece import Piece


class Board:

    SIZE = 14

    def __init__(self, game):
        self.x = (game.WIDTH - self.compute_size()) // 2
        self.y = (game.HEIGHT - self.compute_size()) // 2

        self.starting_points = [(4, 4), (9, 9)]
        self.cells = []
        for j in range(0, Board.SIZE):
            for i in range(0, Board.SIZE):
                starting_cell = (i, j) in self.starting_points
                self.cells.append(Cell(i, j, starting_cell))

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

            # Cell is out of the board [CHECK]
            if (x + bloc[0] < 0 or x + bloc[0] >= Board.SIZE or y + bloc[1] < 0 or y + bloc[1] >= Board.SIZE):
                return False

            # Cell is not empty [CHECK]
            cell = self.search_cell(x + bloc[0], y + bloc[1])
            if cell.color != Colors.WHITE.value and cell.color != Colors.BLUE.value and cell.color != Colors.GREEN.value:
                return False

        if (self.__verify_neighbour_cells(x, y, piece) == False and self.__is_first_piece() == False):
            return False

        for bloc in piece.blocs:
            cell = self.search_cell(x + bloc[0], y + bloc[1])
            cell.set_color(piece.color)

        return True

    def __verify_neighbour_cells(self, x, y, piece):
        adjacent_cells = []
        temp_diagonal_cells = []
        diagonals_cells = []

        for bloc in piece.blocs:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if ((i + bloc[0], j + bloc[1]) in piece.blocs):
                        continue
                    if (i == 0 and j == 0):
                        continue
                    if (x + bloc[0] + i < 0 or x + bloc[0] + i >= Board.SIZE or y + bloc[1] + j < 0 or y + bloc[1] + j >= Board.SIZE):
                        continue
                    if (i == 0 or j == 0):
                        if ((x + bloc[0] + i, y + bloc[1] + j) not in adjacent_cells):
                            adjacent_cells.append((x + bloc[0] + i, y + bloc[1] + j))
                    else:
                        if ((x + bloc[0] + i, y + bloc[1] + j) not in temp_diagonal_cells):
                            temp_diagonal_cells.append((x + bloc[0] + i, y + bloc[1] + j))

        for cell in temp_diagonal_cells:
            if (cell in adjacent_cells):
                continue
            elif (cell not in diagonals_cells):
                diagonals_cells.append(cell)

        for cell in adjacent_cells:
            cell = self.search_cell(cell[0], cell[1])
            if (cell.color == piece.color):
                return False

        for cell in diagonals_cells:
            cell = self.search_cell(cell[0], cell[1])
            if (cell.color == piece.color):
                return True

        return False

    def __is_first_piece(self):
        for cell in self.cells:
            if cell.color != Colors.WHITE.value:
                return False
        return True

    def handle_click(self, mouse_x, mouse_y):
        grid_x = (mouse_x - self.x) // Cell.SIZE
        grid_y = (mouse_y - self.y) // Cell.SIZE

        if 0 <= grid_x < Board.SIZE and 0 <= grid_y < Board.SIZE:
            cell = self.search_cell(grid_x, grid_y)
            if cell.color == Colors.WHITE.value:
                self.place_piece(Piece(Colors.PURPLE.value, [(0, 0), (0, -1), (0, 1), (-1, 0), (1, 0)]), grid_x, grid_y)
