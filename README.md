# DMZ-FL: Decentralized, verifiable, and adaptive federated learning for vehicular networks

DMZ-FL integrates a **Tangle-style DAG ledger**, **Bulletproofs zero-knowledge
gradient-norm proofs**, **MAPPO dynamic client selection**, and a **PBFT RSU
consortium** into a closed defense loop (verification -> reputation ->
selection -> aggregation).

## Key design points

- **On-chain/off-chain separation.** The DAG transaction carries only
  `(C, pi, H(o_i), w_global, PBFT attestations)`; the plaintext local model
  `w_local` is delivered over an encrypted off-chain channel and never published.
- **Bulletproofs = publicly verifiable norm enforcement.** The proof certifies
  `||g||_2 <= B` (model-adaptive: `B=15` for CNN2, `B=5` for MLP3) without a
  trusted setup; it prevents a quorum of Byzantine RSUs from unilaterally
  relaxing the norm check.
- **Directional vs. amplitude defense.** Sign-Flip (`g -> -g`) is caught by
  cosine-similarity + reputation decay + rollback; Gradient Scaling
  (`g -> 10g`) is rejected by the Bulletproofs norm bound.

## Repository structure

```
DMZ-FL/
  main.py                 # single-experiment entry
  run_benchmark.py        # attack x defense x malicious-ratio sweep
  global_args.py          # CLI + YAML argument loading
  global_utils.py         # registry, seeds, logger
  configs/                # YAML hyperparameters
  datapreprocessor/       # Fashion-MNIST / VeReMi / Car-Hacking loaders + non-IID split
  dmzfl/
    engine/               # worker / client / server / coordinator
    algorithms/           # FedAvg / FedProx / FedNova / DMZ-FL
    models/               # CNN2 (Fashion-MNIST), MLP3 (VeReMi, Car-Hacking)
    ledger/               # DAG Tangle, tip selection, block-based baseline, storage
    consensus/            # PBFT over M=7 RSUs, master election, attestations
    zkp/                  # Pedersen commitment, norm range proof, off-chain channel
    selection/            # MAPPO actor-critic, replay buffer, adaptive reward
    reputation/           # EMA reputation, cosine detection, majority rollback
    aggregators/          # robust aggregation (DMZ-FL + baselines)
    attackers/            # Sign-Flip / Gradient Scaling / Label-Flipping
  experiments/            # one runnable entry per paper table/figure
  tests/                  # unit tests (commitment binding, fixed point, PBFT quorum)
  results/                # logs / figures (gitignored except .gitkeep)
```

## Quick start

```bash
pip install -r requirements.txt

# Main accuracy table (Table 2)
python experiments/run_main_accuracy.py --config configs/dmzfl_fmnist.yaml

# Ablation under 30% Gradient Scaling (Fig. 8)
python experiments/run_ablation.py

# DAG vs. block-based ledger discrete-event simulation
python experiments/run_dag_simulation.py

# ZKP microbenchmark (Linux/WSL; requires pybulletproofs)
python experiments/run_zkp_benchmark.py
```

## Datasets & models

| Dataset       | Model  | Norm bound B | Notes                          |
|---------------|--------|--------------|--------------------------------|
| Fashion-MNIST | CNN2   | 15           | image; quantized conv m=8      |
| VeReMi        | MLP3   | 5            | tabular; extreme class imbalance |
| Car-Hacking   | MLP3   | 5            | tabular; ~9.5K parameters      |

## Citation

Cite the corresponding DMZ-FL paper (JSA revision).