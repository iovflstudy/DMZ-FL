"""Reputation- and data-volume-weighted aggregation; BN stats kept local (FedBN)."""
from .aggregatorbase import Aggregator
class DMZFLAgg(Aggregator):
    def aggregate(self, updates): raise NotImplementedError