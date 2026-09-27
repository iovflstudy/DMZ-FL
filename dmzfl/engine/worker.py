"""Base trainer: holds local data, local model, produces an update vector."""
class Worker:
    def __init__(self, wid, train_idx): self.wid = wid; self.train_idx = train_idx
    def load_global_model(self, global_vec): raise NotImplementedError
    def local_training(self): raise NotImplementedError