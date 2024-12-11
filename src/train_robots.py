# src/train_robots.py
from stable_baselines3 import PPO
import gymnasium as gym
from simulation.blocus_env import registerSimulation

registerSimulation()

# Entraîner le premier robot
env1 = gym.make('Blocus-v0')
model1 = PPO('CnnPolicy', env1, verbose=1)
model1.learn(total_timesteps=10000)
model1.save("ppo_robot1")

# Entraîner le deuxième robot
env2 = gym.make('Blocus-v0')
model2 = PPO('CnnPolicy', env2, verbose=1)
model2.learn(total_timesteps=10000)
model2.save("ppo_robot2")
