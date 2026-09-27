"""Range proof certifying ||g||_2 <= B (model-adaptive).

No trusted setup; does not reveal individual component values. Amplitude attacks
(g -> 10g) are rejected here; directional attacks go to reputation/cosine.
"""
class NormRangeProof:
    def __init__(self, B): self.B = B
    def prove(self, g, r): raise NotImplementedError
    def verify(self, C, proof): raise NotImplementedError