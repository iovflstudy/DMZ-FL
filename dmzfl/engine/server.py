"""Server (RSU consortium). collect_updates -> aggregator -> update_global."""
class Server:
    def collect_updates(self, epoch): raise NotImplementedError
    def aggregation(self): raise NotImplementedError
    def update_global(self): raise NotImplementedError