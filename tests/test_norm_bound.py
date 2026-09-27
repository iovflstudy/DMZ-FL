"""Scaling x10 must be rejected; honest updates pass."""
from dmzfl.attackers.gradientscaling import GradientScaling
def test_scaling():
    import numpy as np
    g = np.ones(5) * 1.0
    assert np.linalg.norm(GradientScaling(10.0).apply(g)) > 15.0