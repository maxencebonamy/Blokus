
from game.cell import Cell
from utils.colors import Colors


class Board:

    SIZE = 14

    def __init__(self, game):
        self.game = game
        self.x = (game.WIDTH - self.compute_size()) // 2
        self.y = (game.HEIGHT - self.compute_size()) // 2

        self.starting_points = [(4, 4), (9, 9)]
        self.cells = []
        for j in range(0, Board.SIZE):
            for i in range(0, Board.SIZE):
                starting_cell = (i, j) in self.starting_points
                self.cells.append(Cell(i, j, starting_cell))

        self.preview_piece = None
        self.preview_position = None
        self.selected_piece = None
        self.occupied_cells = {}

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
                preview_cell = self.search_cell(preview_x, preview_y)
                if preview_cell:
                    preview_cell.set_color(self.lighten_color(self.preview_piece.color))

    @staticmethod
    def lighten_color(color):
        return tuple(min(c + 180, 250) for c in color)

    def search_cell(self, x, y):
        if 0 <= x < Board.SIZE and 0 <= y < Board.SIZE:
            index = y * Board.SIZE + x
            return self.cells[index]
        return None

    def get_cell_color(self, x, y):
        if (x, y) in self.occupied_cells.keys():
            return self.occupied_cells[(x, y)]
        cell = self.search_cell(x, y)
        if cell is None:
            return None
        return self.search_cell(x, y).color

    def place_piece(self, piece, x, y):
        for bloc in piece.blocs:
            cell = self.search_cell(x + bloc[0], y + bloc[1])
            if cell is None:
                return False
            if not cell.is_empty() or (x + bloc[0], y + bloc[1]) in self.occupied_cells.keys():
                return False

        if (not self.__verify_starting_points(x, y, piece) or not self.__verify_neighbour_cells(x, y, piece)):
            return False

        for bloc in piece.blocs:
            cell = self.search_cell(x + bloc[0], y + bloc[1])
            if cell is None:
                return False
            cell.set_color(piece.color)

        self.game.switch_player()
        return True

    def __verify_neighbour_cells(self, x, y, piece):
        not_covered_points = []
        for starting_point in self.starting_points:
            cell = self.search_cell(starting_point[0], starting_point[1])
            if cell is not None and cell.is_empty():
                not_covered_points.append(starting_point)
        if len(not_covered_points) > 0:
            return True

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
            if (self.get_cell_color(cell[0], cell[1]) == piece.color):
                print("ADJACENT", cell, self.get_cell_color(cell[0], cell[1]), piece.color)
                return False

        for cell in diagonals_cells:
            if (self.get_cell_color(cell[0], cell[1]) == piece.color):
                print("DIAGONAL", cell, self.get_cell_color(cell[0], cell[1]), piece.color)
                return True

        print("NO NEIGHBOURS")
        return False

    def __verify_starting_points(self, x, y, piece):
        not_covered_points = []
        for starting_point in self.starting_points:
            cell = self.search_cell(starting_point[0], starting_point[1])
            if cell is not None and cell.is_empty():
                not_covered_points.append(starting_point)
        if len(not_covered_points) == 0:
            return True

        for bloc in piece.blocs:
            if (x + bloc[0], y + bloc[1]) in not_covered_points:
                return True
        return False

    def handle_click(self, mouse_x, mouse_y, player):
        # Check if the click is on the left panel
        if 0 <= mouse_x < self.x and 0 <= mouse_y < Board.SIZE * Cell.SIZE:
            print("Click on the left panel")
            selected_piece = self.handle_click_panel(mouse_x, mouse_y, player)
            if selected_piece:
                self.preview_piece = selected_piece
                print(f"Piece selected: {selected_piece}")
        # Check if the click is on the right panel
        elif self.x + self.compute_size() <= mouse_x < self.x + self.compute_size() + self.x and 0 <= mouse_y < Board.SIZE * Cell.SIZE:
            print("Click on the right panel")
            selected_piece = self.handle_click_panel(mouse_x, mouse_y, player)
            if selected_piece:
                self.preview_piece = selected_piece
                print(f"Piece selected: {selected_piece}")
        else:
            # Otherwise, handle the click on the grid
            self.handle_click_grid(mouse_x, mouse_y, player)

    def handle_click_grid(self, mouse_x, mouse_y, player):
        if self.preview_piece is None:
            print("Error: No piece selected for preview.")
            return

        grid_x = (mouse_x - self.x) // Cell.SIZE
        grid_y = (mouse_y - self.y) // Cell.SIZE

        if 0 <= grid_x < Board.SIZE and 0 <= grid_y < Board.SIZE:
            if self.preview_position == (grid_x, grid_y):
                # Validate the position if the user clicks again on the same cell
                if self.place_piece(self.preview_piece, grid_x, grid_y):
                    print("Piece placed successfully!")
                    player.remove_piece(self.preview_piece)
                    self.preview_piece = None
                    self.preview_position = None
                else:
                    print("Cannot place the piece here.")
            else:
                # Clear the previous preview and set the new preview position
                if self.preview_position:
                    self.clear_preview()
                self.preview_position = (grid_x, grid_y)
                self.occupied_cells.clear()
                for bloc in self.preview_piece.blocs:
                    cell = self.search_cell(grid_x + bloc[0], grid_y + bloc[1])
                    if cell is not None and cell.color != Colors.WHITE.value:
                        self.occupied_cells[(grid_x + bloc[0], grid_y + bloc[1])] = cell.color
                        print(self.occupied_cells)

    def clear_preview(self):
        if self.preview_piece and self.preview_position:
            x, y = self.preview_position
            for bloc in self.preview_piece.blocs:
                preview_x = x + bloc[0]
                preview_y = y + bloc[1]
                if 0 <= preview_x < Board.SIZE and 0 <= preview_y < Board.SIZE:
                    preview_cell = self.search_cell(preview_x, preview_y)
                    if (preview_x, preview_y) not in self.occupied_cells.keys():
                        preview_cell.set_color(Colors.WHITE.value)
                    else:
                        preview_cell.set_color(self.occupied_cells.get((preview_x, preview_y)))

    def handle_click_panel(self, mouse_x, mouse_y, player):
        piece = player.pieces_panel.get_piece_at(mouse_x, mouse_y)
        if piece:
            print(f"Piece selected: {piece}")
            return piece
        return None

    def handle_right_button(self):
        if self.preview_piece:
            self.clear_preview()
            self.preview_piece.rotate(True)
            self.occupied_cells.clear()
            for bloc in self.preview_piece.blocs:
                cell = self.search_cell(self.preview_position[0] + bloc[0], self.preview_position[1] + bloc[1])
                if cell.color != Colors.WHITE.value:
                    self.occupied_cells[(self.preview_position[0] + bloc[0], self.preview_position[1] + bloc[1])] = cell.color
                    print(self.occupied_cells)

    def handle_left_button(self):
        if self.preview_piece:
            self.clear_preview()
            self.preview_piece.rotate(False)
            self.occupied_cells.clear()
            for bloc in self.preview_piece.blocs:
                cell = self.search_cell(self.preview_position[0] + bloc[0], self.preview_position[1] + bloc[1])
                if cell.color != Colors.WHITE.value:
                    self.occupied_cells[(self.preview_position[0] + bloc[0], self.preview_position[1] + bloc[1])] = cell.color
                    print(self.occupied_cells)
