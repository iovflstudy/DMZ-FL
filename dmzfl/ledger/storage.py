"""Byte accounting: 732 B/tx -> annual storage.

On-chain payload = 32 B commitment C_n + 608 B range proof + 92 B metadata.
At N=100, 70 selected/round, 144 rounds/day -> 10080 tx/day.
732 * 10080 * 365 / 1e9 ~= 2.69 GB/year (2.51 GiB), matching the ~2.67 GB/year
working-point figure reported for the DAG.
"""
TX_BYTES = 732
def annual_storage_gb(tx_per_day, tx_bytes=TX_BYTES):
    return tx_bytes * tx_per_day * 365 / 1e9
