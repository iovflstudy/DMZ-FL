from .aggregatorbase import Aggregator
class FedAvg(Aggregator):
    def aggregate(self, updates): raise NotImplementedError