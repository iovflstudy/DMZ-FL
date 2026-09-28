"""Pedersen commitment to the quantized norm slack.

The on-chain commitment is the scalar Pedersen commitment
``C_n = Commit(n, r_n) = g^{r_n} h^n`` over a Ristretto prime-order group
(production backend: dalek ``curve25519-dalek``, driven by the Rust crate in
``experiments/zkp_bulletproofs/``). It is perfectly hiding and computationally
binding under the discrete-logarithm problem.

The gradient ``g`` itself is *never* committed to or published on-chain; only
the scalar norm-slack ``n`` is hidden behind ``C_n``. The plaintext model
``w_local`` and the blinding factor ``r_n`` travel over the encrypted
off-chain channel so an RSU can recompute and re-open ``C_n`` (binding check).

A tiny integer-group implementation is included for the lightweight demo and
unit tests only; it is NOT a production backend (use the elliptic-curve crate).
"""
from __future__ import annotations

# Mersenne prime P = 2^61 - 1; the quadratic-residue subgroup has order (P-1)/2.
_P = (1 << 61) - 1
_G = pow(2, 2, _P)
_H = pow(3, 2, _P)
_Q = (_P - 1) // 2


class PedersenCommitment:
    """Scalar Pedersen commitment C_n = g^{r_n} h^n (toy integer group)."""

    def random_blinding(self) -> int:
        import secrets
        return secrets.randbelow(_Q - 1) + 1

    def commit(self, n: int, r_n: int) -> int:
        return (pow(_G, r_n, _P) * pow(_H, int(n), _P)) % _P

    def verify(self, C_n: int, n: int, r_n: int) -> bool:
        return C_n == self.commit(n, r_n)
