# Bulletproofs norm-slack range proof (Rust)

This is the production cryptographic backend used for the zero-knowledge
micro-benchmark in Section 6.8. It uses the dalek-cryptography crates
[`bulletproofs`](https://github.com/dalek-cryptography/bulletproofs) **v5**
over the Ristretto group of
[`curve25519-dalek`](https://github.com/dalek-cryptography/curve25519-dalek)
**v4**. No trusted setup is required.

## Statement

For the effective gradient `g` and the public model-adaptive bound `B`, the
vehicle encodes the norm slack as a 32-bit fixed-point scalar

```
s^2 = B^2 - ||g||_2^2 ,   n = floor(s^2 * 2^32 / B^2) in [0, 2^32)
```

and produces a Bulletproofs **range proof** for `0 <= n < 2^32`, i.e.
`||g||_2 <= B`, together with a scalar Pedersen commitment `C_n = Commit(n, r_n)`.
The proof reveals neither `n` nor any component of `g`. Over-norm updates
(Gradient Scaling `g -> 10g`) make the slack negative and are rejected;
norm-preserving Sign-Flip is handled separately by cosine detection and
reputation, not by this proof.

## Run

```bash
cd experiments/zkp_bulletproofs
cargo run --release
```

The program first warms up, then (1) reports the per-proof prove/verify
latency and serialized proof size for `m = 1`, and (2) generates up to 1,000
independent proofs (one per selected vehicle) and reports total verification
wall-clock time for `N = 1, 10, 50, 70, 100, 200, 500, 1000`.

## Representative measurements

| Quantity | Value |
|---|---|
| Prove time per proof (m = 1) | ~19.1 ms |
| Verify time per proof (m = 1) | ~2.71 ms |
| Serialized proof size (m = 1) | 608 B |
| 70 independent proofs / round | ~190 ms (< 7% of the 3,229 ms round) |
| 1,000 independent proofs | ~2.3 s (linear; parallel across RSUs) |

Timings are best-of-run wall-clock values on the benchmark host and vary with
the machine and load; verification scales linearly in the number of
independent proofs and the proof size grows only logarithmically when several
scalars are aggregated into one proof.
