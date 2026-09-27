"""Byte accounting: 764 B/tx -> annual storage.

At N=100, 70 selected/round, 144 rounds/day -> 10080 tx/day.
764 * 10080 * 365 / 1024**3 ~= 2.62 GB/year (DAG).
"""
TX_BYTES = 764
def annual_storage_gb(tx_per_day, tx_bytes=TX_BYTES):
    return tx_bytes * tx_per_day * 365 / (1024 ** 3)