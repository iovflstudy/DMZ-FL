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
| `experiments/` | One runnable entry per paper table/figure (WIP) |
| `configs/` | YAML hyperparameters aligned with the manuscript |
| `tests/` | Unit tests (reputation fixed point, norm bound, PBFT quorum, commitment binding) |
| `dag_sim/` | Standalone DAG overhead simulator |

## Datasets

| Dataset | Model | Norm bound B | Link |
|---|---|---|---|
| Fashion-MNIST | CNN2 | 15 | https://github.com/zalandoresearch/fashion-mnist |
| VeReMi | MLP3 | 5 | https://github.com/josephkamel/VeReMi-Dataset |
| Car-Hacking | MLP3 | 5 | https://ocslab.hksecurity.net/Datasets/car-hacking-dataset |

## Cryptography backends

- Bulletproofs Python binding: https://pypi.org/project/pybulletproofs/
- Official dalek-cryptography Rust `bulletproofs` (Ristretto, curve25519-dalek): https://github.com/dalek-cryptography/bulletproofs
- `curve25519-dalek`: https://github.com/dalek-cryptography/curve25519-dalek

## Baselines & references

- FedAvg — McMahan et al., *Communication-Efficient Learning of Deep Networks from Decentralized Data*, AISTATS 2017.
- FedProx — Li et al., Federated Optimization in Heterogeneous Networks, MLSys 2020.
- FedNova — Wang et al., Tackling the Objective Inconsistency Problem in Heterogeneous Federated Optimization, NeurIPS 2020.
- MAPPO-FL — Yu et al., 2024.
- VFL-Chain — Smahi et al., *Bulletproofing Federated Learning in the V2X Environments*, Future Generation Computer Systems 2024. https://doi.org/10.1016/j.future.2024.02.012
- BlockFL — Kim et al., 2020.
- Krum / Multi-Krum — Blanchard et al., Machine Learning with Adversaries: Byzantine Tolerant Gradient Descent, NeurIPS 2017.
- FLTrust — Cao et al., Byzantine-Robust Federated Learning via Trust Bootstrapping, NDSS 2021.
- Bulletproofs — Bunz et al., 2018.

## Citation

Cite the corresponding DMZ-FL paper (JSA revision).