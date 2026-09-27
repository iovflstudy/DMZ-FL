"""Encrypted off-chain channel: w_local sent to RSUs, decrypted into a buffer
retained until final confirmation K_final=60 rounds (supports aggregation/rollback)."""
class OffChainChannel:
    def send(self, vehicle, rsu_set, w_local): raise NotImplementedError
    def buffer(self, rid): raise NotImplementedError