# src/play_robots.py
from stable_baselines3 import PPO
import gymnasium as gym
from simulation.blocus_env import registerSimulation

registerSimulation()

# Charger les modèles entraînés
model1 = PPO.load("ppo_robot1")
model2 = PPO.load("ppo_robot2")

# Créer l'environnement
env = gym.make('Blocus-v0')

obs = env.reset()
done = False

while not done:
    # Robot 1 joue
    action1, _states1 = model1.predict(obs)
    obs, reward, done, info = env.step(action1)
    env.render()
    if done:
        break

    # Robot 2 joue
    action2, _states2 = model2.predict(obs)
    obs, reward, done, info = env.step(action2)
    env.render()
    if done:
        break

env.close()
