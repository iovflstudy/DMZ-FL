# DMZ-FL: Decentralized, verifiable, adaptive federated learning for vehicular networks

> Source code: https://github.com/iovflstudy/DMZ-FL

DMZ-FL integrates a **Tangle-style DAG ledger**, **Bulletproofs zero-knowledge
gradient-norm proofs**, **MAPPO dynamic client selection**, and a **PBFT RSU
consortium** into a closed defense loop (verification -> reputation ->
selection -> aggregation).

> This repository is the released research scaffold. Core modules are implemented;
> the training loop, data loaders, and full experiment runners are under active
> development. A zero-dependency demo that exercises the security primitives is
> provided (`demo.py`).

## Quick start

```bash
pip install numpy pyyaml matplotlib
python demo.py          # no PyTorch / dataset / ZKP library required
```

## Repository structure & function

| Folder | What it does |
|---|---|
| `dmzfl/ledger/` | DAG Tangle: transaction format (C, pi, H, attestations only), MCMC tip selection, confirmation depths, block-based baseline, byte/storage accounting |
| `dmzfl/consensus/` | PBFT over M=7 RSUs, master election, attestations |
| `dmzfl/zkp/` | Pedersen commitment, gradient-norm range proof, real/mock Bulletproofs backend, encrypted off-chain channel for w_local |
| `dmzfl/selection/` | MAPPO actor-critic, replay buffer, scale-invariant reward shaping |
| `dmzfl/reputation/` | EMA reputation (decay 0.95, fixed point 0.60), cosine directional detection, majority-vote rollback |
| `dmzfl/aggregators/` | Robust aggregation registry (DMZ-FL + baselines) |
| `dmzfl/attackers/` | Sign-Flip, Gradient Scaling, Label Flipping |
| `dmzfl/engine/` | worker / client / server / coordinator (training loop, WIP) |
| `dmzfl/algorithms/` | FedAvg / FedProx / FedNova / DMZ-FL |
| `dmzfl/models/` | CNN2 (Fashion-MNIST), MLP3 (VeReMi / Car-Hacking) |
| `datapreprocessor/` | Dataset loaders + IID / Dirichlet non-IID partition |
| `experiments/` | Runnable entries: `run_dag_simulation.py` (DAG vs. block-based ledger sweep), `run_zkp_benchmark.py` (Bulletproofs range-proof micro-benchmark), plus main accuracy / ablation / mobility runners |
| `configs/` | YAML hyperparameters aligned with the manuscript |
| `tests/` | Unit tests (reputation fixed point, norm bound, PBFT quorum, commitment binding) |
| `dag_sim/` | Standalone DAG overhead simulator |

## Datasets, backends, and baselines

See [`references/README.md`](references/README.md) for dataset links, the
dalek-cryptography Rust Bulletproofs backend used in the micro-benchmark, and
the baseline papers.

