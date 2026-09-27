"""On-chain transaction.

The payload contains ONLY (commitment C, range proof pi, observation hash H(o_i),
global model w_global, PBFT attestations). The plaintext local model w_local is
delivered off-chain (see dmzfl.zkp.offchannel) and is deliberately NOT a field
here -- this is the structural fix for the reviewer-noted gradient disclosure.
"""
from dataclasses import dataclass, field

@dataclass
class Transaction:
    tx_id: str
    commitment: bytes        # Pedersen commitment C = Commit(g, r)
    proof: bytes             # Bulletproofs range proof pi
    obs_hash: bytes          # H(o_i): rep, comp, snr, vel, wd
    global_model_version: int
    attestations: list = field(default_factory=list)
    tip_refs: tuple = (None, None)   # two referenced tips
    timestamp: float = 0.0

    PAYLOAD_BYTES = 32 + 640 + 92   # commitment + proof + metadata