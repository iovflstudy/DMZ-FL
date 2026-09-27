"""Tangle DAG: optimistic confirmation K=10, final confirmation K_final=60."""
class Tangle:
    def __init__(self, K=10, K_final=60, p_h=0.67, alpha=0.33):
        self.K, self.K_final = K, K_final
        self.p_h, self.alpha = p_h, alpha
        self.transactions = {}
    def attach(self, tx): raise NotImplementedError
    def confirmation_depth(self, tx_id): raise NotImplementedError
    def forgery_prob(self, depth):
        # exp(-depth * ln(p_h/alpha)); 8.4e-4 at K=10, 3.4e-19 at K_final=60
        import math
        return math.exp(-depth * math.log(self.p_h / self.alpha))