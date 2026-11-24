from typing import Union
import pygame

from game.game import Game
from graphics.colors import Colors
from graphics.board_vue import BoardVue
from graphics.score_vue import ScoreVue
from graphics.pieces_vue import PiecesVue


class Window:

    def __init__(self, game: Game, width: int, height: int, title: str):
        self.__game = game
        self.__width = width
        self.__height = height
        self.__title = title

        pygame.init()
        self.__window = pygame.display.set_mode((self.__width, self.__height))
        pygame.display.set_caption(self.__title)

        self.__board_vue = BoardVue(self.__game)
        self.__score_vue = ScoreVue(self.__game, self.__board_vue.get_rect(self.get_window()))
        self.__pieces_vue = PiecesVue(self.__game, self.__board_vue.get_rect(self.get_window()))

        self.__running = True
        self.__selected_piece_index: Union[int, None] = None

    def update(self):
        self.clear()
        for event in self.get_events():
            if event.type == pygame.QUIT:
                self.close()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.__board_target = self.__board_vue.get_cell_at(pygame.mouse.get_pos())
                if self.__board_target is not None and self.__selected_piece_index is not None:
                    self.__game.play(self.__selected_piece_index, *self.__board_target)
                    self.__selected_piece_index = None
                else:
                    self.__selected_piece_index = self.__pieces_vue.get_piece_index_at(pygame.mouse.get_pos())
        self.__board_vue.draw(self.get_window())
        self.__score_vue.draw(self.get_window())
        self.__pieces_vue.draw(self.get_window(), self.__selected_piece_index)
        pygame.display.flip()

        if self.__game.is_terminated():
            winner = self.__game.get_winner()
            if winner is None:
                print('It is a draw')
            else:
                print(f'Player {winner.get_id()} wins')
            exit()

    def close(self):
        self.__running = False

    def clear(self):
        self.__window.fill(Colors.WHITE)

    def get_events(self):
        return pygame.event.get()

    def get_window(self):
        return self.__window

    def run(self):
        while self.__running:
            self.update()

    def is_running(self):
        return self.__running
