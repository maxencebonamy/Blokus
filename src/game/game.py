import pygame

from game.player import Player
from game.board import Board
from game.pieces_panel import PiecesPanel
from utils.colors import Colors


class Game:

    WIDTH = 1000
    HEIGHT = 600

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((Game.WIDTH, Game.HEIGHT))

        self.orange_player = Player(Colors.ORANGE.value)
        self.purple_player = Player(Colors.PURPLE.value)

        self.board = Board(self)
        self.current_player = self.orange_player

    def switch_player(self):
        if self.current_player == self.orange_player:
            self.current_player = self.purple_player
        else:
            self.current_player = self.orange_player

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.purple_player.add_score(1)
                        self.orange_player.add_score(1)

            self.screen.fill(Colors.WHITE.value)

            self.orange_player.label.draw(
                self.screen, self.board.x // 2, 60
            )
            self.orange_player.pieces_panel.draw(
                self.screen, (self.board.x - PiecesPanel.WIDTH) // 2, 100
            )
            self.purple_player.label.draw(
                self.screen, self.board.x + self.board.compute_size() + self.board.x // 2, 60
            )
            self.purple_player.pieces_panel.draw(
                self.screen, self.board.x + self.board.compute_size() + (self.board.x - PiecesPanel.WIDTH) // 2, 100
            )
            self.board.draw(self.screen)

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clic gauche
                    mouse_x, mouse_y = event.pos
                    self.board.handle_click(mouse_x, mouse_y)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    self.board.handle_right_button()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    self.board.handle_left_button()
