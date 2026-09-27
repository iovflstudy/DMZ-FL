"""Adaptive reward shaping.

norm term: exp(-3 * | ||g||_2/B - 1/3 |) -- scale-invariant w.r.t. model bound B
(CNN2 B=15 / MLP3 B=5). Prefers updates well below the ceiling; penalizes zero
and ceiling-hugging updates.
"""
import math
def norm_reward(g_norm, B):
    return math.exp(-3 * abs(g_norm / B - 1.0/3.0))