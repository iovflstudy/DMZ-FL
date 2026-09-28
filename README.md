# DMZ-FL: Decentralized, Verifiable, Adaptive Federated Learning for Vehicular Networks

> Source code: https://github.com/iovflstudy/DMZ-FL

DMZ-FL is a vehicular federated learning (FL) framework built on a Tangle-style
DAG ledger. It removes the central aggregation server, protects local updates
with zero-knowledge gradient-norm proofs, and closes a self-correcting defense
loop among verification, reputation, client selection, and aggregation for
Internet-of-Vehicles (IoV) deployments.

## Motivation

Vehicular FL lets vehicles collaboratively train models without sharing raw data,
but three problems are hard in practice:

1. **Single point of failure.** A central aggregation server is vulnerable and
   becomes a bottleneck; moving it to a single RSU does not remove it.
2. **Gradient exposure.** If local updates are published in the clear, an observer
   that knows the current global model can recover each client's gradient and run
   model/gradient inversion.
3. **Byzantine and poisoning clients.** Malicious vehicles can submit sign-flipped,
   gradient-scaled, or label-flipped updates to distort the global model, and a
   naive norm check is not enough by itself.

DMZ-FL addresses all three together: a PBFT RSU consortium replaces the central
server, a DAG ledger lets updates be confirmed asynchronously, and Bulletproofs
range proofs enforce the gradient-norm bound publicly without revealing the
update.

## System overview

DMZ-FL ties four components into one loop:

- **DAG ledger (`dmzfl/ledger/`).** Each selected vehicle publishes a transaction
  that carries only a Pedersen commitment `C`, a Bulletproofs range proof `π`, a
  hash `H`, the global-model reference, and attestations. The plaintext local
  model `w_local` is sent over an encrypted off-chain channel and is never stored
  on the ledger. Transactions are appended to a Tangle DAG and confirmed
  incrementally by MCMC tip selection and cumulative weight, with no global block
  to seal.
- **Bulletproofs verification (`dmzfl/zkp/`).** A 32-bit range proof certifies
  that the norm slack `B² − ‖g‖²` is non-negative, i.e. the committed gradient is
  within the public bound `B`, without revealing any gradient component and with
  no trusted setup. Pedersen commitment binds the proof to the hidden update.
- **PBFT RSU consortium (`dmzfl/consensus/`).** Seven RSUs run PBFT, elect a
  master, and collectively attest the DAG entries; they tolerate up to `f_R < M/3`
  Byzantine RSUs, so norm enforcement is not a single leader's unilateral call.
- **MAPPO selection + reputation aggregation (`dmzfl/selection/`,
  `dmzfl/reputation/`).** An actor–critic policy picks participating vehicles;
  an EMA reputation (fixed point 0.60), posterior cosine checks, and a 2M/3
  majority-vote rollback punish directional poisoning and roll back bad rounds.

The loop runs as: vehicles train locally → commit + prove → RSU-consensus
verifies → reputation weights the aggregation → cosine/rollback corrects
outliers.

## Threat model

| Adversary | Capability | DMZ-FL defense | Goal |
|---|---|---|---|
| Byzantine RSU (`< M/3`) | Colludes to manipulate attestations / norm checks | PBFT consensus, publicly verifiable Bulletproofs | Consensus safety/liveness, independent of any single RSU |
| Malicious vehicle | Adaptive poisoning: Sign-Flip, Gradient Scaling, Label-Flipping; alternates good/bad updates | Bulletproofs norm bound (amplitude), cosine check + EMA reputation + 2M/3 rollback (directional) | Reject amplitude and directional updates |
| External eavesdropper on DAG | Reads all on-chain transactions | Only `(C, π, H, global ref)` are on-chain; `w_local` goes off-chain | Gradient confidentiality |

The confidentiality guarantee targets external DAG observers, not the authorized
RSU consortium, which legitimately receives `w_local` off-chain to recover the
effective gradient. Norm enforcement is publicly auditable by any RSU and
enforced by the PBFT majority.
## End-to-end workflow

| Step | Actor | Action | Output |
|---|---|---|---|
| 1. Local training | Vehicle | Trains on private data using the latest policy attestation on the DAG | Local update `w_local` |
| 2. Commit & prove | Vehicle | Builds Pedersen commitment `C = Commit(g, r)` and Bulletproofs range proof `π` certifying the norm bound `‖g‖ ≤ B` | Transaction `(C, π, H, w_global, attestations)` |
| 3. Publish | Vehicle | Sends the transaction to the DAG; `w_local` goes over an encrypted off-chain channel to the RSU consortium | On-chain `(C, π, H, …)`; off-chain `w_local` |
| 4. Verify | RSU consortium (PBFT) | Verifies `π`; decrypts `w_local`; recovers `g_eff = w_local − w_global`; cosine check against the current global model | Pass/fail + effective gradient |
| 5. Append & confirm | DAG | MCMC tip selection references the tx; weight accumulates incrementally as more tx arrive; no global block | Confirmed DAG entry |
| 6. Reputation update | RSU consortium | EMA reputation (fixed point 0.60); cosine anomalies decay reputation; warm-up for new vehicles | Updated reputation scores |
| 7. Aggregate | RSU consortium | Weighted aggregation by reputation and data volume over verified updates | New global model `w_global` |
| 8. Rollback | RSU consortium | If a malicious-majority / directional attack is detected, 2M/3 majority vote rolls back the round and forces ε-greedy exploration | Corrected global model |
| 9. Policy update | RSU consortium | Joint PPO update from `(o, a, r)` trajectories; PBFT-attested new policy hash written to the DAG | New MAPPO policy version |
| 10. Next round | Vehicles | Pull the highest-version, depth-≥5 policy attestation; repeat | Continuous FL loop |
## Quick start

```bash
pip install numpy pyyaml matplotlib
python demo.py                          # exercises the security primitives, no PyTorch/dataset
python experiments/run_dag_simulation.py   # DAG vs. block-ledger sweep
python experiments/run_zkp_benchmark.py    # Bulletproofs range-proof numbers
```

## Key results

| What | Result |
|---|---|
| Accuracy | Outperforms FedAvg by **5.64 pp** on Fashion-MNIST (CNN2); ~3× the random baseline on VeReMi (MLP3) |
| Robustness | Stable under **30%** Sign-Flip, Gradient Scaling, and Label-Flipping on all three datasets |
| ZKP overhead | **2.71 ms** verify and **608 B** proof per client (Curve25519, Ristretto); 70 clients/round ≈ 190 ms, <7% of the 3,229 ms round |
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
  confirmation latency, confirmation rate as the arrival rate rises (30→150
  tx/round).
- `experiments/run_zkp_benchmark.py` — Bulletproofs range-proof micro-benchmark
  (prove / verify latency and proof size for m = 1, 8, 32, 70 scalars).
- `experiments/run_main_accuracy.py` — baseline accuracy on the three datasets.
- `experiments/run_ablation.py` — ablation under Gradient Scaling.
- `experiments/run_mobility.py` — MAPPO mobility / client-selection study.

## Datasets & backends

See [`references/README.md`](references/README.md) for dataset links
(Fashion-MNIST, VeReMi, Car-Hacking), the dalek-cryptography Rust Bulletproofs
backend, and baseline papers.
