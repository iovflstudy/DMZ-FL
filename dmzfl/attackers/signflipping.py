"""Sign-Flip: g -> -g (direction attack; norm unchanged -> caught by cosine)."""
from .base import Attack
class SignFlip(Attack):
    def apply(self, g): return -g