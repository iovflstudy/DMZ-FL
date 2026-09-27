"""MCMC tip selection (Tangle). L=10 walk steps, beta=0.5, k=2 tips."""
import random
class MCMCTipSelector:
    def __init__(self, L=10, beta=0.5, k=2):
        self.L, self.beta, self.k = L, beta, k
    def select_tips(self, tips):
        # TODO: weighted MCMC random walk; return k tips
        raise NotImplementedError