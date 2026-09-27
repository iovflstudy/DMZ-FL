"""EMA reputation: rep0=0.5, warmup 5 rounds, decay 0.95.
delta+ = +0.03 (pass), delta- = -0.03 (fail), -0.10 extra on rollback.
Steady state rep* = 0.03/(1-0.95) = 0.60. Clamped to [0,1].
"""
class Reputation:
    def __init__(self, init=0.5, gamma=0.95):
        self.score = init; self.gamma = gamma
    def update(self, passed, rolled_back=False):
        d = -0.10 if rolled_back else (0.03 if passed else -0.03)
        self.score = max(0.0, min(1.0, self.gamma * self.score + d))
        return self.score