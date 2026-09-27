"""Label Flipping: y -> (y + floor(C/2)) mod C (data poisoning)."""
from .base import Attack
class LabelFlipping(Attack):
    def __init__(self, num_classes): self.C = num_classes
    def apply(self, y): return (y + self.C // 2) % self.C