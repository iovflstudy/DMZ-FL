import torch.nn as nn
class MLP3(nn.Module):
    """Compact three-layer MLP for the tabular datasets (VeReMi, Car-Hacking)."""
    def __init__(self, input_dim, num_classes):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim,64), nn.ReLU(),
            nn.Linear(64,32), nn.ReLU(),
            nn.Linear(32,num_classes))