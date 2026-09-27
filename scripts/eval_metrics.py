"""
Evaluation Metrics and Baselines
=================================
Computes accuracy, variance, and comparison metrics across baselines.
"""
import numpy as np

BASELINES = [
    'FedAvg', 'FedProx', 'FedNova', 'MAPPO-FL',
    'VFL-Chain', 'BlockFL', 'DMZ-FL'
]

ATTACK_TYPES = ['Sign-Flip', 'Gradient Scaling', 'Label Flipping']

DATASETS = ['Fashion-MNIST', 'VeReMi', 'CAN-Multi']

MALICIOUS_RATIOS = [0.0, 0.10, 0.20, 0.30]

SEEDS = [42, 142, 242]


def compute_metrics(results, baseline_name):
    """
    Compute mean accuracy and standard deviation across seeds.

    Args:
        results: dict of {seed: accuracy}
        baseline_name: str

    Returns:
        (mean, std): tuple of floats
    """
    accuracies = list(results.values())
    return np.mean(accuracies), np.std(accuracies)


def format_result(mean, std):
    """Format as 'mean ± std' for LaTeX tables."""
    return f"${mean:.4f} \\pm {std:.4f}$"


# Expected baseline comparison results (Table 2 in paper)
# Values averaged over 3 seeds at 100 rounds, Fashion-MNIST (CNN2)
BASELINE_RESULTS_FMNIST = {
    'DMZ-FL':      (0.8609, 0.0033),
    'FedProx':     (0.8527, 0.0093),
    'FedNova':     (0.8136, 0.0075),
    'VFL-Chain':   (0.8052, 0.0096),
    'MAPPO-FL':    (0.8016, 0.0074),
    'FedAvg':      (0.8045, 0.0129),
    'BlockFL':     (0.7920, 0.0176),
}

# Attack robustness at 30% malicious ratio, Fashion-MNIST
ATTACK_RESULTS_SIGNFLIP_30 = {
    'DMZ-FL':      0.8401,
    'FedProx':     0.8217,
    'MAPPO-FL':    0.7963,
    'FedAvg':      0.7726,
}

ATTACK_RESULTS_SCALING_30 = {
    'DMZ-FL':      0.8410,
    'FedProx':     0.8085,
    'MAPPO-FL':    0.7930,
    'FedAvg':      0.7780,
}

ATTACK_RESULTS_LABELFLIP_30 = {
    'DMZ-FL':      0.8241,
    'FedProx':     0.8104,
    'MAPPO-FL':    0.7815,
    'FedAvg':      0.7659,
}

# Ablation study (30% Gradient Scaling, Fashion-MNIST, matches Fig. 8)
# full / -ZKP / -MAPPO / -Reputation
ABLATION_RESULTS = {
    'DMZ-FL (full)': 0.8410,
    '-ZKP':          0.8214,
    '-MAPPO':        0.8372,
    '-Reputation':   0.8395,
}
