"""Encrypted off-chain channel between vehicles and the RSU consortium.

A selected vehicle delivers ``(w_local, r_n)`` over an authenticated,
encrypted channel: ``w_local`` is needed for reputation-/data-volume-weighted
aggregation and rollback, and the blinding factor ``r_n`` lets an RSU recompute
the effective slack ``n_eff`` and re-open/match the on-chain commitment ``C_n``
(the binding check that ties the proven slack to the actual gradient).

Both values are decrypted into an RSU-side buffer retained only until final
confirmation (``K_final = 60`` rounds) and are NEVER written to the public DAG.
"""
from __future__ import annotations


class OffChainChannel:
    def send(self, vehicle, rsu_set, w_local, r_n):
        raise NotImplementedError

    def buffer(self, rid):
        raise NotImplementedError
