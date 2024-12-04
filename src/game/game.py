import pygame

from game.board import Board
from game.score_label import ScoreLabel
from utils.colors import Colors

class Game:

    WIDTH = 1000
    HEIGHT = 600

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((Game.WIDTH, Game.HEIGHT))

        self.orange_score_label = ScoreLabel(Colors.ORANGE.value, 0)
        self.purple_score_label = ScoreLabel(Colors.PURPLE.value, 0)

        self.board = Board(self)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(Colors.WHITE.value)

            self.orange_score_label.draw(
                self.screen, self.board.x // 2, self.board.y * 2
            )
            self.purple_score_label.draw(
                self.screen, self.board.x + self.board.compute_size() + self.board.x // 2, self.board.y * 2
            )
            self.board.draw(self.screen)

            pygame.display.flip()
