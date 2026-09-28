"""Bulletproofs backend abstraction.

Production backend.  dalek-cryptography Rust ``bulletproofs`` v5 over the
Ristretto group of ``curve25519-dalek`` v4, compiled in release mode and
invoked through a thin native interface. The reproducible crate (including
the multi-client batch-verification benchmark) lives in
``experiments/zkp_bulletproofs/`` and runs with ``cargo run --release``.
There is no trusted setup.

Mock backend.  Fixed *measured* constants for Windows development and the
lightweight demo. The numbers are the real 32-bit single-scalar (m = 1)
measurements reported in the manuscript: prove 19.1 ms, verify 2.71 ms,
608 B serialized proof.
"""
from __future__ import annotations


class MockBulletproofs:
    prove_ms = 19.1
    verify_ms = 2.71
    proof_bytes = 608

    def prove(self, n: int, r_n: int) -> bytes:
        return b"\x00" * self.proof_bytes

    def verify(self, C_n, proof: bytes) -> bool:
        return isinstance(proof, (bytes, bytearray)) and len(proof) == self.proof_bytes
