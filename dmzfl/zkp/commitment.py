"""Pedersen commitment C = Commit(g, r). Hides g under discrete-log assumption."""
class PedersenCommitment:
    def commit(self, g, r): raise NotImplementedError
    def open(self, C, g, r): raise NotImplementedError