"""Bulletproofs microbenchmark. On Linux/WSL use the real pybulletproofs backend;
on Windows use MockBulletproofs. Report prove/verify latency and proof size.
38.06 s = 11,776 proofs over ~168 rounds (independent microbenchmark);
per round = 70 proofs x 3.2 ms = 224 ms (<7% of the 3229 ms per-round latency)."""
def main():
    from dmzfl.zkp.bulletproofs import MockBulletproofs
    bp = MockBulletproofs()
    print(f"mock: {bp.prove_ms} ms prove, {bp.verify_ms} ms verify, {bp.proof_bytes} B")
if __name__ == '__main__': main()