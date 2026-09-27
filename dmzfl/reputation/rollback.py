"""Majority-vote rollback: >= 2M/3 (M=7), timeout 500 ms; triggers epsilon-greedy."""
class RollbackController:
    def __init__(self, M=7, epsilon=0.2): self.M, self.eps = M, epsilon
    def should_rollback(self, votes):
        return votes >= 2 * (self.M // 3) + 1