from dmzfl.consensus.pbft import PBFT
def test_quorum():
    pb = PBFT(M=7)
    assert pb.messages_per_block() == 49
    assert pb.quorum_satisfied([1,2,3,4,5]) is True   # >= 5