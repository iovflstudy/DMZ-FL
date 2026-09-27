"""Verify steady-state reputation = 0.03/(1-0.95) = 0.60 (reviewer R1-3/R5-5)."""
from dmzfl.reputation.reputation import Reputation
def test_fixed_point():
    r = Reputation(init=0.5)
    for _ in range(200): r.update(passed=True)
    assert abs(r.score - 0.60) < 0.02, r.score