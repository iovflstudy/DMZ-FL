"""Directional poisoning detection: cosine(g_eff, global_delta) < -0.3
(angle > 107.5 deg). Applies to Sign-Flip; NOT to amplitude attacks."""
import numpy as np
def is_counter_directional(g_eff, global_delta, threshold=-0.3):
    cos = float(np.dot(g_eff, global_delta) /
                (np.linalg.norm(g_eff)*np.linalg.norm(global_delta) + 1e-12))
    return cos < threshold