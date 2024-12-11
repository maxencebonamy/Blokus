# src/run_simulation.py
import gymnasium as gym
from simulation.blocus_env import registerSimulation

registerSimulation()
env = gym.make('Blocus-v0')

observation = env.reset()
for _ in range(1000):
    action = env.action_space.sample()  # Remplacez par votre politique d'action
    observation, reward, done, info = env.step(action)
    env.render()
    if done:
        observation = env.reset()

env.close()
