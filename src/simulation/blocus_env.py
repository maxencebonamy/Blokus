# src/simulation/blocus_env.py
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame
from game.game import Game
from game.board import Board
from gymnasium.envs.registration import register


def registerSimulation():
    register(
        id='Blocus-v0',
        entry_point='simulation.blocus_env:BlocusEnv',
    )


class BlocusEnv(gym.Env):
    metadata = {'render_modes': ['human']}

    def __init__(self):
        super(BlocusEnv, self).__init__()
        self.game = Game()
        self.current_player = self.game.orange_player

        # Définir l'espace d'observation
        self.observation_space = spaces.Dict({
            'board': spaces.Box(low=0, high=255, shape=(Board.SIZE, Board.SIZE, 3), dtype=np.uint8),
            'orange_pieces': spaces.MultiBinary(len(self.game.orange_player.pieces)),
            'purple_pieces': spaces.MultiBinary(len(self.game.purple_player.pieces))
        })

        # Initialiser l'espace d'action
        self._update_action_space()

    def _update_action_space(self):
        num_pieces = len(self.current_player.pieces)
        print(f"Updating action space: {num_pieces} pieces")
        self.action_space = spaces.MultiDiscrete([num_pieces, Board.SIZE, Board.SIZE])

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.game = Game()
        self.current_player = self.game.orange_player
        self._update_action_space()
        return self._get_observation(), {}

    def step(self, action):
        piece_index, x, y = action
        if piece_index >= len(self.current_player.pieces):
            return self._get_observation(), -5, True, False, {}
        print(f"Piece index: {piece_index}, x: {x}, y: {y}")
        print(f"Nombre de pièces: {len(self.current_player.pieces)}")
        piece = list(self.current_player.pieces)[piece_index]

        reward = 0
        terminated = False
        truncated = False
        info = {}

        if self.game.board.place_piece(piece, x, y):
            reward = piece.get_points()
            self.current_player.remove_piece(piece)
            # self.game.switch_player()
            self.current_player = self.game.current_player
            self._update_action_space()
        else:
            reward = -5

        if not self.current_player.pieces:
            terminated = True

        observation = self._get_observation()
        return observation, reward, terminated, truncated, info

    def render(self, mode='human'):
        if mode == 'human':
            self.game.run()

    def _get_observation(self):
        board = self.game.board.get_color_map()
        orange_pieces = np.zeros(len(self.game.orange_player.pieces), dtype=np.int8)
        purple_pieces = np.zeros(len(self.game.purple_player.pieces), dtype=np.int8)

        for i, piece in enumerate(self.game.orange_player.pieces):
            orange_pieces[i] = 1

        for i, piece in enumerate(self.game.purple_player.pieces):
            purple_pieces[i] = 1

        return {
            'board': np.array(board),
            'orange_pieces': orange_pieces,
            'purple_pieces': purple_pieces
        }

    def close(self):
        pygame.quit()
