# src/custom_cnn.py
import torch as th
import torch.nn as nn
import gymnasium as gym
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor

class CustomCNN(BaseFeaturesExtractor):
    def __init__(self, observation_space: gym.spaces.Dict, features_dim: int = 256):
        super(CustomCNN, self).__init__(observation_space, features_dim)
        self.extractors = nn.ModuleDict()
        total_concat_size = 0

        # Build the CNN for each subspace
        for key, subspace in observation_space.spaces.items():
            if isinstance(subspace, gym.spaces.Box):
                n_input_channels = subspace.shape[0]
                cnn = nn.Sequential(
                    nn.Conv2d(n_input_channels, 32, kernel_size=3, stride=1, padding=1),
                    nn.ReLU(),
                    nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1),
                    nn.ReLU(),
                    nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1),
                    nn.ReLU(),
                    nn.Flatten(),
                )

                # Compute shape by doing one forward pass
                with th.no_grad():
                    n_flatten = cnn(th.as_tensor(subspace.sample()[None]).float()).shape[1]

                self.extractors[key] = cnn
                total_concat_size += n_flatten
            elif isinstance(subspace, gym.spaces.MultiBinary):
                self.extractors[key] = nn.Flatten()
                total_concat_size += subspace.shape[0]

        self.linear = nn.Sequential(
            nn.Linear(total_concat_size, features_dim),
            nn.ReLU()
        )

    def forward(self, observations: th.Tensor) -> th.Tensor:
        encoded_tensor_list = []

        for key, extractor in self.extractors.items():
            encoded_tensor_list.append(extractor(observations[key]))

        # Concatenate all extracted features
        concatenated = th.cat(encoded_tensor_list, dim=1)
        return self.linear(concatenated)