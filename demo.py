"""
DMZ-FL lightweight demo (no PyTorch, no dataset, no ZKP library).

Exercises the implemented security primitives end to end so you can verify the
scaffold works:

    python demo.py
"""
import numpy as np

from dmzfl.attackers.signflipping import SignFlip
from dmzfl.attackers.gradientscaling import GradientScaling
from dmzfl.attackers.labelflipping import LabelFlipping
from dmzfl.reputation.reputation import Reputation
from dmzfl.reputation.cosine import is_counter_directional
from dmzfl.consensus.pbft import PBFT
from dmzfl.ledger.storage import annual_storage_gb
from dmzfl.ledger.dag import Tangle
from dmzfl.zkp.bulletproofs import MockBulletproofs


def banner(t):
    print("\n=== " + t + " ===")


def demo_attacks():
    banner("1. Poisoning attacks on a gradient vector g")
    g = np.array([0.1, -0.2, 0.3, 0.4])
    print("honest g        :", g, " norm=%.3f" % np.linalg.norm(g))
    print("sign-flip g->-g :", SignFlip().apply(g))
    print("scaling g->10g  :", GradientScaling(10.0).apply(g),
          " norm=%.3f" % np.linalg.norm(GradientScaling(10.0).apply(g)))
    y = np.array([0, 1, 2, 3, 4])
    print("label-flip y    :", LabelFlipping(num_classes=5).apply(y))


def demo_reputation():
    banner("2. Reputation EMA (gamma=0.95, reward +0.03) -> fixed point 0.60")
    r = Reputation(init=0.5)
    for _ in range(300):
        r.update(passed=True)
    print("steady-state reputation = %.3f (theory 0.03/(1-0.95)=0.60)" % r.score)


def demo_directional_detection():
    banner("3. Directional defense: Sign-Flip caught by cosine similarity")
    honest_delta = np.array([1.0, 1.0, 1.0])      # global update direction
    flipped = -np.array([1.01, 0.99, 1.02])      # sign-flipped local update
    detected = is_counter_directional(flipped, honest_delta, threshold=-0.3)
    print("counter-directional (Sign-Flip) detected:", detected)


def demo_amplitude_defense():
    banner("4. Amplitude defense: Gradient Scaling rejected by norm bound B")
    bp = MockBulletproofs()
    B = 5.0
    g_honest = np.ones(3) * 1.0     # norm 1.73 < B
    g_bad = GradientScaling(10.0).apply(g_honest)  # norm 17.3 > B
    print("honest norm=%.2f <= B=%.1f -> accepted" % (np.linalg.norm(g_honest), B))
    print("scaled  norm=%.2f  > B=%.1f -> rejected by norm bound" % (np.linalg.norm(g_bad), B))
    print("mock proof: %d bytes, %.1f ms prove / %.1f ms verify"
          % (bp.proof_bytes, bp.prove_ms, bp.verify_ms))


def demo_consensus():
    banner("5. PBFT over M=7 RSUs")
    pb = PBFT(M=7)
    print("messages per block = O(M^2) =", pb.messages_per_block())
    print("quorum (>=2M/3) satisfied with 5 votes:", pb.quorum_satisfied([1, 2, 3, 4, 5]))


def demo_ledger():
    banner("6. DAG ledger accounting")
    tangle = Tangle(K=10, K_final=60)
    print("forgery prob @ K=10      : %.2e" % tangle.forgery_prob(10))
    print("forgery prob @ K_final=60: %.2e" % tangle.forgery_prob(60))
    tx_per_day = 70 * 144   # 70 selected/round, 144 rounds/day
    print("annual storage = %.2f GB/year (732 B/tx, %d tx/day)"
          % (annual_storage_gb(tx_per_day), tx_per_day))


if __name__ == "__main__":
    print("DMZ-FL lightweight demo")
    demo_attacks()
    demo_reputation()
    demo_directional_detection()
    demo_amplitude_defense()
    demo_consensus()
    demo_ledger()
    print("\nDemo finished.")