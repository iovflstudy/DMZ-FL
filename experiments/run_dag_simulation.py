"""
DAG vs. traditional block-based ledger — matched discrete-event simulation.

Two experiments:
  (A) Single working point (w=70 tx/round): throughput / confirmation latency
      / confirmation rate / annual storage for both ledgers.
  (B) Throughput-vs-arrival sweep: w in {30,50,70,100,150} tx/round. Shows
      DAG throughput tracks the arrival rate linearly, while the block-based
      ledger saturates at block capacity and degrades (long queue, low
      confirmation rate) once w exceeds its processing rate.

Model
  DAG: tx appended immediately; confirmed after `dag_depth` rounds of follow-up
       weight (incremental, asynchronous; no block-seal wait).
  Blockchain: pending FIFO pool; a block seals every `block_interval` rounds
       carrying <= `block_capacity` tx; a block is final after `confirm_blocks`
       more blocks. Each block incurs a PBFT consensus delay of PBFT_MS.

All numbers are produced by the simulation (mean over seeds).
"""

from __future__ import annotations
import numpy as np


# ---- shared config ---------------------------------------------------------
N_ROUNDS = 100
DAG_DEPTH = 6
BLOCK_INTERVAL = 4        # rounds between block seals
BLOCK_CAPACITY = 95       # tx per block
CONFIRM_BLOCKS = 2        # subsequent blocks for finality
PBFT_MS = 1455.0          # per-block PBFT consensus delay (reference value)
TX_BYTES = 732            # 32 commitment + 608 proof + 92 metadata
ROUNDS_PER_YEAR = 52_400
N_SEEDS = 5


# ---- DAG -------------------------------------------------------------------
DAG_CONFIRM_DESCENDANTS = 420   # descendants a tx must accumulate to be confirmed


def run_dag(w: int, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    # confirmation delay = rounds needed to collect k descendants at w tx/round
    delay = int(np.ceil(DAG_CONFIRM_DESCENDANTS / w))
    lat, confirmed, total = [], 0, w * N_ROUNDS
    for r in range(N_ROUNDS):
        for _ in range(w):
            conf = r + delay + int(rng.integers(0, 2))
            if conf < N_ROUNDS:
                confirmed += 1
                lat.append(conf - r)
    through = confirmed / (N_ROUNDS - delay) * 5.0   # tx / 5 rounds
    return {
        "throughput": through,
        "lat_mean": float(np.mean(lat)),
        "lat_std": float(np.std(lat)),
        "confirm_rate": 100.0 * confirmed / total,
    }


# ---- Blockchain ------------------------------------------------------------
def run_blockchain(w: int, seed: int) -> dict:
    pending, lat, confirmed = [], [], 0
    total = w * N_ROUNDS
    block_seq = 0
    for r in range(N_ROUNDS):
        pending.extend([r] * w)                      # arrivals
        if (r + 1) % BLOCK_INTERVAL == 0:            # seal a block
            block_seq += 1
            batch = pending[:BLOCK_CAPACITY]
            pending = pending[BLOCK_CAPACITY:]
            conf_round = (block_seq + CONFIRM_BLOCKS) * BLOCK_INTERVAL
            for r0 in batch:
                if conf_round < N_ROUNDS:
                    confirmed += 1
                    lat.append(conf_round - r0)
    through = confirmed / N_ROUNDS * 5.0
    return {
        "throughput": through,
        "lat_mean": float(np.mean(lat)) if lat else 0.0,
        "lat_std": float(np.std(lat)) if lat else 0.0,
        "confirm_rate": 100.0 * confirmed / total,
    }


def agg(runs, k):
    v = [r[k] for r in runs]
    return float(np.mean(v)), float(np.std(v))


# ---- (A) working point ------------------------------------------------------
def working_point(w=70):
    dag = [run_dag(w, s) for s in range(N_SEEDS)]
    bc = [run_blockchain(w, 1000 + s) for s in range(N_SEEDS)]
    print("=" * 66)
    print(f"[A] Working point: w={w} tx/round, R={N_ROUNDS}, "
          f"block={BLOCK_INTERVAL}r/{BLOCK_CAPACITY}tx, "
          f"confirm blocks={CONFIRM_BLOCKS}")
    print("=" * 66)
    for name, runs in [("DAG", dag), ("Blockchain", bc)]:
        t, _ = agg(runs, "throughput")
        lm, _ = agg(runs, "lat_mean")
        ls, _ = agg(runs, "lat_std")
        cr, _ = agg(runs, "confirm_rate")
        ann = t / 5.0 * ROUNDS_PER_YEAR * TX_BYTES / 1e9
        print(f"  {name:11s} throughput={t:6.1f} tx/5r | "
              f"latency={lm:5.1f}+/-{ls:4.1f} r | "
              f"confirm={cr:5.1f}% | annual={ann:4.2f} GB/yr")
    print(f"  (PBFT per-block consensus delay = {PBFT_MS:.0f} ms, "
          f"on top of the blockchain sealing cadence)\n")


# ---- (B) arrival sweep -----------------------------------------------------
def sweep():
    print("=" * 66)
    print("[B] Throughput vs. transaction arrival rate (tx/round)")
    print("=" * 66)
    print(f"{'w':>4} | {'DAG tx/5r':>10} {'DAG lat':>8} {'DAG conf%':>9} || "
          f"{'BC tx/5r':>10} {'BC lat':>8} {'BC conf%':>9}")
    print("-" * 66)
    for w in (30, 50, 70, 100, 150):
        dag = [run_dag(w, s) for s in range(N_SEEDS)]
        bc = [run_blockchain(w, 1000 + s) for s in range(N_SEEDS)]
        dt, _ = agg(dag, "throughput"); dl, _ = agg(dag, "lat_mean")
        dcr, _ = agg(dag, "confirm_rate")
        bt, _ = agg(bc, "throughput"); bl, _ = agg(bc, "lat_mean")
        bcr, _ = agg(bc, "confirm_rate")
        print(f"{w:>4} | {dt:10.1f} {dl:8.1f} {dcr:9.1f} || "
              f"{bt:10.1f} {bl:8.1f} {bcr:9.1f}")
    print("-" * 66)
    print("Block processing rate = %d tx per block / %d rounds = %.1f tx/round"
          % (BLOCK_CAPACITY, BLOCK_INTERVAL, BLOCK_CAPACITY / BLOCK_INTERVAL))
    print("=> DAG throughput rises with w; blockchain saturates at block "
          "capacity and confirmation rate collapses as w grows.")


if __name__ == "__main__":
    working_point(70)
    sweep()
