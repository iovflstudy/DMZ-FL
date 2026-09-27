"""PPO with GAE (gamma=0.99, lambda=0.95), clip=0.2, target_kl=0.015, grad clip 10."""
class MAPPO:
    def __init__(self, actor, critic): self.actor, self.critic = actor, critic
    def update(self, buffer): raise NotImplementedError