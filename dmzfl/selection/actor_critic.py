"""CTDE networks: Actor [128,64], Critic [256,128]."""
import torch.nn as nn
class Actor(nn.Module):
    def __init__(self, state_dim, action_dim):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(state_dim,128), nn.ReLU(),
                                 nn.Linear(128,64), nn.ReLU(),
                                 nn.Linear(64, action_dim))
class Critic(nn.Module):
    def __init__(self, state_dim):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(state_dim,256), nn.ReLU(),
                                 nn.Linear(256,128), nn.ReLU(), nn.Linear(128,1))