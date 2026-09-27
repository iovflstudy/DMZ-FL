"""Backend abstraction: RealBulletproofs (Linux pybulletproofs) / MockBulletproofs.

Real: wraps dalek-cryptography Rust bulletproofs (Ristretto, curve25519-dalek)
through pybulletproofs==0.1.0.dev7 (PyO3). Mock: fixed latency for Windows dev.
"""
class MockBulletproofs:
    prove_ms = 6.5
    verify_ms = 3.2
    proof_bytes = 640
    def prove(self, g, B): return b'\x00' * self.proof_bytes
    def verify(self, C, proof): return True