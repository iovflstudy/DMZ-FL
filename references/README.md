# Datasets, backends, and baseline references

Links for the experiments in this repository.

## Datasets

| Dataset | Model | Norm bound B | Link |
|---|---|---|---|
| Fashion-MNIST | CNN2 | 15 | https://github.com/zalandoresearch/fashion-mnist |
| VeReMi | MLP3 | 5 | https://github.com/josephkamel/VeReMi-Dataset |
| Car-Hacking | MLP3 | 5 | https://ocslab.hksecurity.net/Datasets/car-hacking-dataset |

## Cryptography backends

- Official dalek-cryptography Rust `bulletproofs` (Ristretto, curve25519-dalek):
  https://github.com/dalek-cryptography/bulletproofs
- `curve25519-dalek`: https://github.com/dalek-cryptography/curve25519-dalek
- The micro-benchmark in `experiments/run_zkp_benchmark.py` uses this Rust backend
  (release build, invoked through a thin native interface from Python).

## Baselines & references

- FedAvg — McMahan et al., *Communication-Efficient Learning of Deep Networks
  from Decentralized Data*, AISTATS 2017.
- FedProx — Li et al., *Federated Optimization in Heterogeneous Networks*,
  MLSys 2020.
- FedNova — Wang et al., *Tackling the Objective Inconsistency Problem in
  Heterogeneous Federated Optimization*, NeurIPS 2020.
- MAPPO-FL — Yu et al., 2024.
- VFL-Chain — Smahi et al., *Bulletproofing Federated Learning in the V2X
  Environments*, Future Generation Computer Systems, 2024.
  https://doi.org/10.1016/j.future.2024.02.012
- BlockFL — Kim et al., 2020.
- Bulletproofs — Bunz et al., *Bulletproofs: Short Proofs for Confidential
  Transactions and More*, IEEE S&P 2018.
- HotStuff — Yin et al., *HotStuff: BFT Consensus with Linearity and
  Responsiveness*, PODC 2019.
