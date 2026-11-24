import pygame
from game.game import Game
from graphics.colors import Colors


class ScoreVue:

    def __init__(self, game: Game, board_rect: pygame.Rect, padding: int = 20):
        self.__game = game
        self.__board_rect = board_rect
        self.__padding = padding
        self.__font = pygame.font.Font(None, 30)

    def __draw_label(self, window: pygame.Surface, text: str, rect: pygame.Rect, color: tuple):
        pygame.draw.rect(window, color, rect, border_radius=4)
        text_surface = self.__font.render(text, True, Colors.WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        window.blit(text_surface, text_rect)

    def draw(self, window: pygame.Surface):
        label_height = 40
        label_width = 150
        x_padding = (self.__board_rect.left - label_width) // 2

        player1_score = f"Score: {self.__game.get_players()[0].get_score()}"
        player2_score = f"Score: {self.__game.get_players()[1].get_score()}"

        player1_rect = pygame.Rect(self.__board_rect.left - label_width - x_padding, self.__padding, label_width, label_height)
        player2_rect = pygame.Rect(self.__board_rect.right + x_padding, self.__padding, label_width, label_height)

        self.__draw_label(window, player1_score, player1_rect, Colors.ORANGE)
        self.__draw_label(window, player2_score, player2_rect, Colors.PURPLE)
