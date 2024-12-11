import gymnasium as gym
from GridWorldEnv import registerSimulation

registerSimulation()
env = gym.make('GridWorld-v0')

observation = env.reset()
for _ in range(1000):
    action = env.action_space.sample()  # Remplacez par votre politique d'action
    observation, reward, terminated, truncated, info = env.step(action)
    env.render()
    if terminated:
        observation = env.reset()

env.close()
