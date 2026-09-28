"""RSU binding check: the recomputed slack must re-open the on-chain C_n.

A tampered or over-norm (Gradient Scaling x10) update either yields a negative
slack or fails to open the published commitment, and must be rejected.
"""
import numpy as np

from dmzfl.zkp.commitment import PedersenCommitment
from dmzfl.zkp.norm_proof import quantize_slack, SLACK_MOD


def test_honest_update_binds_and_passes():
    ped = PedersenCommitment()
    B = 15.0                                   # CNN2 bound
    g = np.ones(8) * 1.0                       # norm 2.83 < B
    n = quantize_slack(g, B)
    assert 0 <= n < SLACK_MOD
    r_n = ped.random_blinding()
    C_n = ped.commit(n, r_n)
    assert ped.verify(C_n, n, r_n)


def test_gradient_scaling_is_over_norm():
    B = 15.0
    g = np.ones(8) * 1.0
    assert np.linalg.norm(g * 10.0) > B        # norm 28.3 > B
    assert quantize_slack(g * 10.0, B) < 0     # slack negative -> reject


def test_tampered_local_model_fails_binding():
    ped = PedersenCommitment()
    B = 15.0
    g = np.ones(8) * 1.0
    n = quantize_slack(g, B)
    r_n = ped.random_blinding()
    C_n = ped.commit(n, r_n)
    n_eff = quantize_slack(g * 1.1, B)         # RSU recomputes from w_local'
    assert not ped.verify(C_n, n_eff, r_n)
