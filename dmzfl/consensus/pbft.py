"""PBFT: pre-prepare/prepare/commit; O(M^2)=49 msgs/block for M=7."""
class PBFT:
    def __init__(self, M=7): self.M = M
    def messages_per_block(self): return self.M ** 2
    def quorum_satisfied(self, votes): return len(votes) >= 2 * (self.M // 3) + 1