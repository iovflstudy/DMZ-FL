"""Plotting helpers: accuracy curves, ablation bars, DAG overhead comparison."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def plot_accuracy(records, path):
    plt.figure(figsize=(5, 3.5))
    for name, ys in records.items():
        plt.plot(range(len(ys)), ys, label=name)
    plt.xlabel('Communication round'); plt.ylabel('Test accuracy')
    plt.legend(); plt.tight_layout(); plt.savefig(path, dpi=200); plt.close()