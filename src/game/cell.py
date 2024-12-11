import pygame
from utils.colors import Colors


class Cell:

    SIZE = 40

    def __init__(self, x, y, starting_cell=False, color=Colors.WHITE.value):
        self.x = x
        self.y = y

        self.rect = pygame.Rect(x * Cell.SIZE, y * Cell.SIZE, Cell.SIZE + 1, Cell.SIZE + 1)
        self.color = color
        self.starting_cell = starting_cell

    def set_color(self, color):
        self.color = color

    def draw(self, screen, board_x, board_y):
        display_rect = self.rect.move(board_x, board_y)
        pygame.draw.rect(screen, self.color, display_rect)
        pygame.draw.rect(screen, Colors.BLACK.value, display_rect, 1)
        if self.starting_cell and self.color == Colors.WHITE.value:
            pygame.draw.circle(screen, Colors.BLACK.value, display_rect.center, Cell.SIZE // 4, 1)

    def __str__(self):
        return f"Cell({self.x}, {self.y})"
