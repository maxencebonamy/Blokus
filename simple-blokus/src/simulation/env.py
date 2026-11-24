from typing import List, Tuple
from gymnasium import Env, spaces
from game.game import Game
import numpy as np
from game.piece import Piece


class GameEnv(Env):

    def __init__(self, board_size: int, pieces: List[Piece]):
        super().__init__()

        self.__board_size = board_size
        self.__pieces = pieces
        self.game = Game(board_size, pieces)

        self.action_space = spaces.MultiDiscrete([len(pieces), board_size, board_size])
        self.observation_space = spaces.Dict({
            'board': spaces.Box(
                low=0, high=2, shape=(self.__board_size, self.__board_size), dtype=np.int64
            ),
            'player_1_remaining_pieces': spaces.Box(
                low=0, high=1, shape=(len(self.__pieces),), dtype=np.int64
            ),
            'player_2_remaining_pieces': spaces.Box(
                low=0, high=1, shape=(len(self.__pieces),), dtype=np.int64
            ),
            'player_1_pieces': spaces.Box(
                low=0, high=1, shape=(len(self.__pieces), Piece.MAX_X - Piece.MIN_X + 1, Piece.MAX_Y - Piece.MIN_Y + 1), dtype=np.int64
            ),
            'player_2_pieces': spaces.Box(
                low=0, high=1, shape=(len(self.__pieces), Piece.MAX_X - Piece.MIN_X + 1, Piece.MAX_Y - Piece.MIN_Y + 1), dtype=np.int64
            )
        })

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.game = Game(self.__board_size, self.__pieces)
        return self.game.get_state(), {}

    def step(self, action: Tuple[int, int, int]):
        piece_index, x, y = action
        if not self.game.play(piece_index, x, y):
            reward = -10
            terminated = False
            truncated = False
            return self.game.get_state(), reward, terminated, truncated, {"info": "Invalid move"}

        terminated = self.game.is_terminated()
        truncated = False

        if terminated:
            winner = self.game.get_winner()
            if winner is None:
                reward = 0
            elif winner.get_id() == 1:
                reward = 5
            elif winner.get_id() == 2:
                reward = -5
            else:
                reward = 0
        else:
            reward = len(self.game.get_current_player().get_pieces()[piece_index].get_blocks())

        return self.game.get_state(), reward, terminated, truncated, {}

    def render(self, mode='human'):
        pass

    def close(self):
        pass
