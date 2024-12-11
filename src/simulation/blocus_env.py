# src/simulation/blocus_env.py
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame
from game.game import Game


class BlocusEnv(gym.Env):
    metadata = {'render_modes': ['human']}

    def __init__(self):
        super(BlocusEnv, self).__init__()
        self.game = Game()
        self.action_space = spaces.Discrete(4)  # Exemple: 4 actions possibles (à adapter selon votre jeu)
        self.observation_space = spaces.Box(low=0, high=255, shape=(self.game.HEIGHT, self.game.WIDTH, 3), dtype=np.uint8)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.game = Game()
        return self._get_observation(), {}

    def step(self, action):
        reward = 0
        done = False
        info = {}

        # Exemple de gestion d'action (à adapter selon votre jeu)
        if action == 0:
            self.game.board.handle_right_button()
        elif action == 1:
            self.game.board.handle_left_button()
        elif action == 2:
            # Implémenter d'autres actions
            pass
        elif action == 3:
            # Implémenter d'autres actions
            pass

        observation = self._get_observation()
        return observation, reward, done, info

    def render(self, mode='human'):
        if mode == 'human':
            self.game.run()

    def _get_observation(self):
        pygame.display.flip()
        screen = pygame.surfarray.array3d(pygame.display.get_surface())
        return np.transpose(screen, (1, 0, 2))

    def close(self):
        pygame.quit()
