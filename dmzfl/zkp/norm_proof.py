"""32-bit Bulletproofs range proof over the quantized norm slack.

Statement.  Given the effective gradient ``g`` and public model-adaptive bound
``B``, the vehicle computes the slack and its 32-bit fixed-point encoding::

    s^2 = B^2 - ||g||_2^2 ,   n = floor(s^2 * 2^32 / B^2) in [0, 2^32)

and proves ``0 <= n < 2^32`` with a Bulletproofs range proof, i.e. ``s^2 >= 0``
and hence ``||g||_2 <= B``. The proof reveals neither ``n`` nor ``g`` and needs
no trusted setup.

Scope.  Amplitude attacks (e.g. Gradient Scaling ``g -> 10g``) drive the slack
negative and are rejected here. Directional attacks (Sign-Flip ``g -> -g``)
preserve the norm and therefore pass the range check; they are handled by
posterior cosine detection and reputation decay, not by this proof.
"""
from __future__ import annotations

SLACK_BITS = 32
SLACK_MOD = 1 << SLACK_BITS


def quantize_slack(g, B: float) -> int:
    """Return n = floor((B^2 - ||g||^2) * 2^32 / B^2).

    Negative iff ||g||_2 > B (the update must then be rejected).
    """
    import numpy as np
    g = np.asarray(g, dtype=float)
    b2 = float(B) * float(B)
    s2 = b2 - float(np.dot(g, g))
    return int(__import__("math").floor(s2 * SLACK_MOD / b2))


class NormRangeProof:
    """Thin wrapper that binds a backend to a fixed norm bound."""

    def __init__(self, B: float, backend):
        self.B = float(B)
        self.backend = backend

    def statement(self, g) -> int:
        return quantize_slack(g, self.B)

    def in_range(self, n: int) -> bool:
        return 0 <= n < SLACK_MOD

    def prove(self, n: int, r_n: int) -> bytes:
        return self.backend.prove(n, r_n)

    def verify(self, C_n, proof: bytes) -> bool:
        return self.backend.verify(C_n, proof)
