import pygame


class Piece:

    BLOC_SIZE = 10
    SIZE = BLOC_SIZE * 6

    def __init__(self, color, blocs):
        self.color = color
        self.blocs = blocs

    def set_color(self, color):
        self.color = color

    def set_bloc(self, blocs):
        self.blocs = blocs

    def rotate(self, clockwise=True):
        if clockwise:
            self.blocs = [(-y, x) for x, y in self.blocs]
        else:
            self.blocs = [(y, -x) for x, y in self.blocs]

    def get_points(self):
        return self.blocs.__len__()

    def draw(self, screen, x, y):
        for bloc in self.blocs:
            pygame.draw.rect(screen, self.color, (x + (bloc[0] + 2) * Piece.BLOC_SIZE,
                             y + (bloc[1] + 2) * Piece.BLOC_SIZE, Piece.BLOC_SIZE, Piece.BLOC_SIZE))

    def __str__(self):
        min_x = min(x for x, y in self.blocs)
        max_x = max(x for x, y in self.blocs)
        min_y = min(y for x, y in self.blocs)
        max_y = max(y for x, y in self.blocs)

        width = max_x - min_x + 1
        height = max_y - min_y + 1

        result = [['.' for _ in range(width)] for _ in range(height)]

        for x, y in self.blocs:
            result[y - min_y][x - min_x] = "■"

        return "\n"+"\n".join("".join(row) for row in result)
