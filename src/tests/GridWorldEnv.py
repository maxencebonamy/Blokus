import gymnasium as gym
import numpy as np
from typing import Optional
from gymnasium.envs.registration import register


class GridWorldEnv(gym.Env):

    def __init__(self, size: int = 5):

        self.size = size

        self.agent_location = np.array([-1, -1], dtype=np.int32)
        self.target_location = np.array([-1, -1], dtype=np.int32)

        self.observation_space = gym.spaces.Dict({
            "agent": gym.spaces.Box(low=0, high=size - 1, shape=(2,), dtype=np.int32),
            "target": gym.spaces.Box(low=0, high=size - 1, shape=(2,), dtype=np.int32)
        })

        self.action_space = gym.spaces.Discrete(4)
        self.action_to_direction = {
            0: np.array([1, 0], dtype=np.int32),
            1: np.array([0, 1], dtype=np.int32),
            2: np.array([-1, 0], dtype=np.int32),
            3: np.array([0, -1], dtype=np.int32)
        }

    def _get_obs(self):
        return {"agent": self.agent_location, "target": self.target_location}

    def _get_info(self):
        return {
            "distance": np.linalg.norm(
                self.agent_location - self.target_location, ord=1
            )
        }

    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        # Choose the agent's location uniformly at random
        self.agent_location = self.np_random.integers(0, self.size, size=2, dtype=int)

        # We will sample the target's location randomly until it does not coincide with the agent's location
        self.target_location = self.agent_location
        while np.array_equal(self.target_location, self.agent_location):
            self.target_location = self.np_random.integers(
                0, self.size, size=2, dtype=int
            )

        observation = self._get_obs()
        info = self._get_info()

        return observation, info

    def step(self, action):
        # Map the action (element of {0,1,2,3}) to the direction we walk in
        direction = self.action_to_direction[action]
        # We use `np.clip` to make sure we don't leave the grid bounds
        self.agent_location = np.clip(
            self.agent_location + direction, 0, self.size - 1
        )

        # An environment is completed if and only if the agent has reached the target
        terminated = np.array_equal(self.agent_location, self.target_location)
        truncated = False
        reward = 1 if terminated else 0  # the agent is only reached at the end of the episode
        observation = self._get_obs()
        info = self._get_info()

        return observation, reward, terminated, truncated, info

    def render(self, mode='human'):
        print(f"Agent: {self.agent_location}, Target: {self.target_location}")


def registerSimulation():
    register("GridWorld-v0", entry_point="GridWorldEnv:GridWorldEnv")
