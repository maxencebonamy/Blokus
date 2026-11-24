from typing import List
from game.game import Game
import random
from simulation.env import GameEnv
from game.piece import Piece


class RandomOpponent:

    def __init__(self):
        pass

    def select_action(self, game: Game):
        available_actions = self.get_available_actions(game)
        return random.choice(available_actions)

    def get_available_actions(self, game: Game):
        actions = []
        player = game.get_current_player()
        for piece_index, piece in enumerate(player.get_pieces()):
            if piece.is_placed():
                continue
            for y in range(game.get_board().get_size()):
                for x in range(game.get_board().get_size()):
                    if game.get_board().is_valid_position(piece, x, y, player.get_id()):
                        actions.append((piece_index, x, y))
        return actions


class GameEnvWithOpponent(GameEnv):

    def __init__(self, board_size: int, pieces: List[Piece]):
        super().__init__(board_size, pieces)
        self.opponent = RandomOpponent()

    def step(self, action):
        opponent_action = self.opponent.select_action(self.game)
        self.game.play(*opponent_action)

        terminated = self.game.is_terminated()
        if terminated:
            winner = self.game.get_winner()
            if winner is None:
                reward = 0
            elif winner.get_id() == 1:
                reward = -5
            elif winner.get_id() == 2:
                reward = 5
            else:
                reward = 0
            return self.game.get_state(), reward, terminated, False, {}

        piece_index, x, y = action
        score = self.game.play(piece_index, x, y)
        if not score:
            return self.game.get_state(), -10, False, False, {"info": "Invalid move"}

        terminated = self.game.is_terminated()
        if terminated:
            winner = self.game.get_winner()
            if winner is None:
                reward = 0
            elif winner.get_id() == 1:
                reward = -5
            elif winner.get_id() == 2:
                reward = 5
            else:
                reward = 0
            return self.game.get_state(), reward, terminated, False, {}
        else:
            reward = len(self.game.get_current_player().get_pieces()[piece_index].get_blocks()) * 2

        # TODO: increase reward if the player blocks the opponent

        return self.game.get_state(), reward, terminated, False, {}
