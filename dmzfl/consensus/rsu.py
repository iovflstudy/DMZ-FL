"""RSU nodes: M=7, one master elected every 20 rounds, f_R < M/3 Byzantine."""
class RSU:
    def __init__(self, rid, byzantine=False):
        self.rid, self.byzantine = rid, byzantine
class RSUSet:
    def __init__(self, M=7):
        self.nodes = [RSU(i) for i in range(M)]
    def elect_master(self, round_no):
        # reputation-weighted election every 20 rounds
        raise NotImplementedError