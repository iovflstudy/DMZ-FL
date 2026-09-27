import torch.nn as nn
class CNN2(nn.Module):
    """Two-conv + two-fc backbone for Fashion-MNIST (28x28)."""
    def __init__(self, num_classes=10):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1,32,3,padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32,64,3,padding=1), nn.ReLU(), nn.MaxPool2d(2))
        self.classifier = nn.Sequential(
            nn.Linear(64*7*7,128), nn.ReLU(), nn.Linear(128,num_classes))