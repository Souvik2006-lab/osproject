"""
tests/test_segmentation_core.py
pytest tests for segmentation_core.
"""

from core.segmentation_core import SegmentationMemory

def test_allocate_and_free():
    mgr = SegmentationMemory(total_size=1000)
    assert mgr.allocate("P1.S1", 200, policy="first")
    assert mgr.allocate("P2.S1", 300, policy="best")
    # Free and ensure merge
    mgr.free("P1.S1")
    frag = mgr.fragmentation()
    assert frag['total_free'] > 0
