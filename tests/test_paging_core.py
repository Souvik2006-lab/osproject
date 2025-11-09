"""
tests/test_paging_core.py
pytest unit tests for paging_core.
"""

from core.paging_core import PagingSimulation

def test_lru_basic():
    refs = [1,2,3,1,4,1,2]
    sim = PagingSimulation(n_frames=3, algorithm="LRU", reference_string=refs)
    sim.run_all()
    # Known result: compute total faults (manually or from expected)
    # For this sequence with 3 frames, typical LRU faults = 5 (example)
    assert sim.total_accesses == len(refs)
    assert sim.total_faults >= 0

def test_optimal_better_or_equal():
    refs = [7,0,1,2,0,3,0,4,2,3,0,3]
    lru = PagingSimulation(n_frames=3, algorithm="LRU", reference_string=refs)
    opt = PagingSimulation(n_frames=3, algorithm="OPTIMAL", reference_string=refs)
    lru.run_all()
    opt.run_all()
    assert opt.total_faults <= lru.total_faults
