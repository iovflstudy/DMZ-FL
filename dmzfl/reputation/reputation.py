"""EMA reputation: rep0=0.5, warmup 5 rounds, decay 0.95.
delta+ = +0.03 (pass), delta- = -0.03 (fail); a rollback round adds an extra
-0.10 on top of the failure penalty, for a total delta_roll = -0.03 - 0.10 = -0.13.
Steady state rep* = 0.03/(1-0.95) = 0.60. Clamped to [0,1].
"""
class Reputation:
    def __init__(self, init=0.5, gamma=0.95):
        self.score = init; self.gamma = gamma
    def update(self, passed, rolled_back=False):
        # rollback round: failure penalty -0.03 plus extra rollback penalty -0.10 = -0.13
        d = (-0.03 - 0.10) if rolled_back else (0.03 if passed else -0.03)
        self.score = max(0.0, min(1.0, self.gamma * self.score + d))
        return self.score