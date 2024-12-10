from game.cell import Cell
from game.piece import Piece
from utils.colors import Colors
import random


class Board:

    SIZE = 14

    def __init__(self, game):
        self.x = (game.WIDTH - self.compute_size()) // 2
        self.y = (game.HEIGHT - self.compute_size()) // 2

        self.cells = []
        for j in range(0, Board.SIZE):
            for i in range(0, Board.SIZE):
                self.cells.append(Cell(i, j))

        # for _ in range(0, 10):
        #     self.cells[random.randint(0, len(self.cells) - 1)].set_color(Colors.PURPLE.value)
        # for _ in range(0, 10):
        #     self.cells[random.randint(0, len(self.cells) - 1)].set_color(Colors.ORANGE.value)

        self.preview_piece = None
        self.preview_position = None
        self.selected_piece = None
        self.occupied_cells = []

    def compute_size(self):
        return Board.SIZE * Cell.SIZE

    def draw(self, screen):
        for cell in self.cells:
            cell.draw(screen, self.x, self.y)

        if self.preview_piece and self.preview_position:
            x, y = self.preview_position
            for bloc in self.preview_piece.blocs:
                preview_x = x + bloc[0]
                preview_y = y + bloc[1]
                if 0 <= preview_x < Board.SIZE and 0 <= preview_y < Board.SIZE:
                    preview_cell = self.search_cell(preview_x, preview_y)
                    preview_cell.set_color(self.lighten_color(self.preview_piece.color))


    @staticmethod
    def lighten_color(color):
        return tuple(min(c + 180, 250) for c in color)

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
            if cell.color != Colors.WHITE.value and cell.color != self.lighten_color(piece.color):
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

    def handle_click(self, mouse_x, mouse_y, player):
        # Vérifier si le clic est sur le panneau de pièces
        if 0 > mouse_x > Board.SIZE and 0 > mouse_y > Board.SIZE:
            # Appeler handle_click_panel pour gérer le clic sur le panneau
            selected_piece = self.handle_click_panel(mouse_x, mouse_y, player)
            if selected_piece:
                self.preview_piece = selected_piece
                print(f"Pièce sélectionnée : {selected_piece}")
        else:
            # Sinon, gérer le clic sur la grille
            self.handle_click_grid(mouse_x, mouse_y)


    def handle_click_grid(self, mouse_x, mouse_y):
        grid_x = (mouse_x - self.x) // Cell.SIZE
        grid_y = (mouse_y - self.y) // Cell.SIZE

        if 0 <= grid_x < Board.SIZE and 0 <= grid_y < Board.SIZE:
            if self.preview_position == (grid_x, grid_y):
                # Validate the position if the user clicks again on the same cell
                if self.place_piece(self.preview_piece, grid_x, grid_y):
                    print("Piece placed successfully!")
                    self.preview_piece = None
                    self.preview_position = None
                else:
                    print("Cannot place the piece here.")
            else:
                # Clear the previous preview and set the new preview position
                if self.preview_position:
                    self.clear_preview()
                self.preview_piece = Piece(Colors.PURPLE.value, [(0, 0), (0, 1), (-1, -1), (-1, 0), (1, 0)])
                self.preview_position = (grid_x, grid_y)
                self.occupied_cells.clear()
                for bloc in self.preview_piece.blocs:
                    if self.search_cell(grid_x + bloc[0], grid_y + bloc[1]).color != Colors.WHITE.value:
                        self.occupied_cells.append((grid_x + bloc[0], grid_y + bloc[1]))
                        print(self.occupied_cells)


    def clear_preview(self):
        if self.preview_piece and self.preview_position:
            x, y = self.preview_position
            for bloc in self.preview_piece.blocs:
                preview_x = x + bloc[0]
                preview_y = y + bloc[1]
                if 0 <= preview_x < Board.SIZE and 0 <= preview_y < Board.SIZE:
                    preview_cell = self.search_cell(preview_x, preview_y)
                    if (preview_x, preview_y) not in self.occupied_cells:
                        preview_cell.set_color(Colors.WHITE.value)
                    else:
                        preview_cell.set_color(Colors.PURPLE.value)


    def handle_click_panel(self, mouse_x, mouse_y, player):
        for i, piece in enumerate(player.pieces):
            piece_x = mouse_x + (i % 3) * Piece.SIZE
            piece_y = mouse_y + (i // 3) * Piece.SIZE
            rect = pygame.Rect(piece_x, piece_y, Piece.SIZE, Piece.SIZE)
            if rect.collidepoint(mouse_x, mouse_y):
                print(f"Pièce sélectionnée : {piece}")
                return piece
        return None

    def handle_right_button(self):
        if self.preview_piece:
            self.clear_preview()
            self.preview_piece.rotate(True)
            self.occupied_cells.clear()
            for bloc in self.preview_piece.blocs:
                if self.search_cell(self.preview_position[0] + bloc[0],
                                    self.preview_position[1] + bloc[1]).color != Colors.WHITE.value:
                    self.occupied_cells.append((self.preview_position[0] + bloc[0], self.preview_position[1] + bloc[1]))
                    print(self.occupied_cells)

    def handle_left_button(self):
        if self.preview_piece:
            self.clear_preview()
            self.preview_piece.rotate(False)
            self.occupied_cells.clear()
            for bloc in self.preview_piece.blocs:
                if self.search_cell(self.preview_position[0] + bloc[0], self.preview_position[1] + bloc[1]).color != Colors.WHITE.value:
                    self.occupied_cells.append((self.preview_position[0] + bloc[0], self.preview_position[1] + bloc[1]))
                    print(self.occupied_cells)

