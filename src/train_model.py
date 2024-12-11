# src/train_model.py
from stable_baselines3 import PPO
import gymnasium as gym
from simulation.blocus_env import registerSimulation

registerSimulation()


env = gym.make('Blocus-v0')
model = PPO('CnnPolicy', env, verbose=1)
model.learn(total_timesteps=10000)
model.save("ppo_blocus")

# Pour tester le modèle
model = PPO.load("ppo_blocus")
obs = env.reset()
for _ in range(1000):
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()
    if dones:
        obs = env.reset()

env.close()
