"""On-chain transaction.

The payload contains ONLY the Pedersen commitment ``C_n`` to the quantized
norm slack, the Bulletproofs 32-bit range proof ``pi``, the observation hash
``H(o_i)``, the global-model reference, and PBFT attestations. The plaintext
local model ``w_local`` (and the blinding factor ``r_n``) are delivered
off-chain (see ``dmzfl.zkp.offchannel``) and are deliberately NOT fields here
-- this is the structural fix for the reviewer-noted gradient disclosure.
"""
from dataclasses import dataclass, field


@dataclass
class Transaction:
    tx_id: str
    commitment: bytes        # Pedersen C_n = Commit(n, r_n): 1 compressed Ristretto point (32 B)
    proof: bytes             # Bulletproofs 32-bit range proof pi (608 B)
    obs_hash: bytes          # H(o_i): rep, comp, snr, vel, wd
    global_model_version: int
    attestations: list = field(default_factory=list)
    tip_refs: tuple = (None, None)   # two referenced tips
    timestamp: float = 0.0

    # 32 B commitment + 608 B proof + 92 B metadata = 732 B.
    PAYLOAD_BYTES = 32 + 608 + 92
