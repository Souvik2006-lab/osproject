"""
tests/test_integration.py
Sanity checks combining modules.
"""

from core.paging_core import PagingSimulation
from core.segmentation_core import SegmentationMemory

def test_integration_sanity():
    # run paging
    refs = [1,2,3,4,1,2,5,1,2,3]
    sim = PagingSimulation(n_frames=3, algorithm="LRU", reference_string=refs)
    sim.run_all()
    assert sim.total_accesses == len(refs)

    # segmentation
    mgr = SegmentationMemory(total_size=500)
    assert mgr.allocate("A", 100, policy="first")
    assert mgr.free("A")
