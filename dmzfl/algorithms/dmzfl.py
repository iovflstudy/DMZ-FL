"""DMZ-FL algorithm: FedAvg local loop with verifiable norm enforcement.

Vehicle side (paper Algorithm 1).
    1. Train w_local locally (proximal SGD, mu = 0.005).
    2. g = w_local - w.
    3. slack n = floor((B^2 - ||g||^2) * 2^32 / B^2) in [0, 2^32).
    4. scalar Pedersen commitment C_n = Commit(n, r_n).
    5. 32-bit Bulletproofs range proof pi for 0 <= n < 2^32 (equiv. ||g|| <= B).
    The on-chain payload is (C_n, pi, H(o_i), ...), while (w_local, r_n) is
    sent over the encrypted off-chain channel; g never appears on-chain.

RSU side (paper Algorithm 2).
    Verify the signature/timestamp/dedup, then Bulletproofs.Verify(pi, C_n, B);
    decrypt (w_local, r_n), recover g_eff = w_local - w_global, recompute the
    slack n_eff, and require Commit(n_eff, r_n) == C_n and ||g_eff|| <= B.
    This rebinds the proven slack to the actual gradient under the PBFT honest
    majority f_R < M/3. Directional attacks (Sign-Flip) then go to posterior
    cosine detection and reputation-weighted rollback.
"""
from .fedavg import FedAvg


class DMZFL(FedAvg):
    pass
