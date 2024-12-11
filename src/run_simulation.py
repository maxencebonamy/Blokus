# src/run_simulation.py
import gymnasium as gym

# Assurez-vous que l'environnement est enregistré
import simulation

env = gym.make('Blocus-v0')

observation = env.reset()
for _ in range(1000):
    action = env.action_space.sample()  # Remplacez par votre politique d'action
    observation, reward, done, info = env.step(action)
    env.render()
    if done:
        observation = env.reset()

env.close()