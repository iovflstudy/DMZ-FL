import numpy as np
def iid_partition(labels, num_clients, seed=42):
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(labels))
    return np.array_split(idx, num_clients)
def dirichlet_partition(labels, num_clients, alpha=0.5, seed=42):
    # TODO: Dirichlet non-IID partition
    raise NotImplementedError