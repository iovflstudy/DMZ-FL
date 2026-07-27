# DMZ-FL: DAG Blockchain Vehicular Federated Learning with MAPPO and Bulletproofs ZKP

Experimental code repository for the DMZ-FL framework.

## Repository Structure

```
dmz-fl-code/
  configs/         Hyperparameter configurations and experiment settings
  scripts/         Example scripts and evaluation utilities
  dag_sim/         DAG consensus overhead simulator
  figures/         Generated figures and visualization scripts
```

## Requirements

- Python 3.9+
- PyTorch 2.2+
- NumPy, Matplotlib
- pybulletproofs (dalek-cryptography)

## Usage

The DAG consensus overhead simulator is self-contained and can be run independently:

```bash
cd dag_sim
python plot_dag_overhead.py          # Full simulation
python plot_dag_overhead.py --quick  # Quick test (N=50 only)
```

For federated learning experiments, configuration files and evaluation scripts
are provided in `configs/` and `scripts/`. Core algorithm implementations will
be released upon paper acceptance.

## Citation

If you use this code, please cite the corresponding paper.

## License

MIT License
