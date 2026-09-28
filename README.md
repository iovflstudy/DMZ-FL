# DMZ-FL: Decentralized, Verifiable, Adaptive Federated Learning for Vehicular Networks

> Source code: https://github.com/iovflstudy/DMZ-FL

DMZ-FL is a vehicular federated learning framework that closes the loop among
**verification**, **reputation**, **client selection**, and **aggregation** on a
Tangle-style DAG ledger. It combines a DAG ledger, Bulletproofs zero-knowledge
gradient-norm proofs, MAPPO dynamic client selection, and a PBFT RSU consortium
to tolerate Byzantine vehicles without a central aggregation server.

## Key ideas

- **DAG ledger, not a chain.** Vehicle model updates are appended directly to a
  DAG and confirmed incrementally as they accumulate weight, instead of waiting
  for a globally sealed block. Throughput tracks the transaction arrival rate.
- **Gradient-norm proofs, not plaintext gradients.** Each on-chain transaction
  carries only a Pedersen commitment and a Bulletproofs range proof; the plaintext
  update is delivered over an encrypted off-chain channel. The proof enforces the
  norm bound publicly, with no trusted setup.
- **Closed-loop defense.** Reputation-weighted aggregation, cosine-based
  directional-poisoning detection, and majority-vote rollback form a
  self-correcting loop.
- **MAPPO client selection.** An actor–critic policy selects participating
  vehicles under the PBFT RSU consortium, removing the centralized policy server.

## Quick start

```bash
pip install numpy pyyaml matplotlib
python demo.py                 # no PyTorch / dataset / ZKP library required
python experiments/run_dag_simulation.py   # DAG vs. block-ledger sweep
python experiments/run_zkp_benchmark.py     # Bulletproofs range-proof numbers
```

## Highlights

| What | Result |
|---|---|
| Accuracy | Outperforms FedAvg by **5.64 pp** on Fashion-MNIST; ~3× the random baseline on VeReMi |
| Robustness | Stable under **30%** Sign-Flip / Gradient Scaling / Label-Flipping |
| ZKP overhead | **2.71 ms** verify, **608 B** proof per client (Curve25519, Ristretto) |
| DAG throughput | **348 tx / 5 rounds** vs. 104.5 for a block-based ledger |
| DAG confirmation rate | **93.5%** vs. 29.9% at 70 updates/round |
| On-chain footprint | **732 B** per transaction; ~2.67 GB/year |

## Repository layout

| Folder | What it does |
|---|---|
| `dmzfl/ledger/` | DAG Tangle: transaction format, MCMC tip selection, confirmation depths, block-based baseline, storage accounting |
| `dmzfl/consensus/` | PBFT over M=7 RSUs, master election, attestations |
| `dmzfl/zkp/` | Pedersen commitment, gradient-norm range proof, real/mock backend, encrypted off-chain channel |
| `dmzfl/selection/` | MAPPO actor–critic, replay buffer, reward shaping |
| `dmzfl/reputation/` | EMA reputation (fixed point 0.60), cosine detection, majority-vote rollback |
| `dmzfl/aggregators/` | Robust aggregation registry (DMZ-FL + baselines) |
| `dmzfl/attackers/` | Sign-Flip, Gradient Scaling, Label-Flipping |
| `dmzfl/engine/` | Worker / client / server / coordinator training loop |
| `dmzfl/algorithms/` | FedAvg / FedProx / FedNova / DMZ-FL |
| `dmzfl/models/` | CNN2 (Fashion-MNIST), MLP3 (VeReMi / Car-Hacking) |
| `datapreprocessor/` | Dataset loaders + IID / Dirichlet non-IID partition |
| `experiments/` | Runnable entry per paper table/figure |
| `configs/` | YAML hyperparameters aligned with the manuscript |
| `tests/` | Unit tests (reputation fixed point, norm bound, PBFT quorum, commitment binding) |
| `results/figures/` | Manuscript figures (PDF) |
| `references/` | Dataset links, cryptographic backends, baseline papers |

## Experiment runners

- `experiments/run_dag_simulation.py` — DAG vs. block-based ledger: throughput,
  confirmation latency, confirmation rate as arrival rate rises.
- `experiments/run_zkp_benchmark.py` — Bulletproofs range-proof micro-benchmark
  (prove / verify latency and proof size for m = 1, 8, 32, 70 scalars).
- `experiments/run_main_accuracy.py` — baseline accuracy on the three datasets.
- `experiments/run_ablation.py` — ablation under Gradient Scaling.
- `experiments/run_mobility.py` — MAPPO mobility / client-selection study.

## Datasets & backends

See [`references/README.md`](references/README.md) for dataset links
(Fashion-MNIST, VeReMi, Car-Hacking), the dalek-cryptography Rust Bulletproofs
backend, and baseline papers.

## Citation

If you use this code, please cite the corresponding DMZ-FL manuscript.
