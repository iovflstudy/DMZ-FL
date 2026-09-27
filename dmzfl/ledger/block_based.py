"""Traditional block-based ledger baseline (same simulation clock as DAG).

Block interval = 5 rounds, max 100 tx/block, sealed by PBFT over M=7 RSUs.
All metrics sampled per 5 rounds for a fair comparison.
"""
class BlockBasedLedger:
    def __init__(self, block_interval=5, max_txs=100, M=7):
        self.block_interval, self.max_txs, self.M = block_interval, max_txs, M
    def on_tx(self, tx): raise NotImplementedError
    def end_of_round(self, r): raise NotImplementedError