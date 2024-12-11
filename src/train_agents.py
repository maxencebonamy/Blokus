# src/train_agents.py
from stable_baselines3 import PPO
from stable_baselines3.common.policies import ActorCriticPolicy
import gymnasium as gym
from simulation.blocus_env import registerSimulation
from custom_cnn import CustomCNN

registerSimulation()

policy_kwargs = dict(
    features_extractor_class=CustomCNN,
    features_extractor_kwargs=dict(features_dim=256),
)

# Entraîner le premier agent
env1 = gym.make('Blocus-v0')
model1 = PPO(ActorCriticPolicy, env1, policy_kwargs=policy_kwargs, verbose=1)
model1.learn(total_timesteps=10000)
model1.save("ppo_agent1")

# Entraîner le deuxième agent
env2 = gym.make('Blocus-v0')
model2 = PPO(ActorCriticPolicy, env2, policy_kwargs=policy_kwargs, verbose=1)
model2.learn(total_timesteps=10000)
model2.save("ppo_agent2")