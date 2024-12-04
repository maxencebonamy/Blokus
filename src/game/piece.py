
class Piece:

    def __init__(self, color, blocs):
        self.color = color
        self.blocs = blocs

    def set_color(self, color):
        self.color = color

    def setBloc(self, blocs):
        self.blocs = blocs

    def rotate(self, clockwise=True):
        if clockwise:
            self.blocs = [(-y, x) for x, y in self.blocs]
        else:
            self.blocs = [(y, -x) for x, y in self.blocs]

    def get_points(self):
        return self.blocs.__len__()

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

        return "\n".join("".join(row) for row in result)
