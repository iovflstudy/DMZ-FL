"""Gradient Scaling: g -> 10g (amplitude attack; rejected by norm bound B)."""
from .base import Attack
class GradientScaling(Attack):
    def __init__(self, factor=10.0): self.f = factor
    def apply(self, g): return self.f * g