"""Rollout buffer, capacity 4096; trajectories mined from DAG transactions."""
class RolloutBuffer:
    def __init__(self, capacity=4096): self.capacity = capacity; self.data = []