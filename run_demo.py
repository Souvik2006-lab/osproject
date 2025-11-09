"""
run_demo.py
Small CLI to run demo paging and segmentation scenarios.
"""

from core.paging_core import PagingSimulation
from core.segmentation_core import SegmentationMemory

def demo_paging():
    refs = [7,0,1,2,0,3,0,4,2,3,0,3]
    for alg in ("LRU","OPTIMAL"):
        sim = PagingSimulation(n_frames=3, algorithm=alg, reference_string=refs)
        sim.run_all()
        print(f"=== {alg} Summary ===")
        print(sim.summary())
        print(sim.get_log().to_string(index=False))
        print()

def demo_segmentation():
    mgr = SegmentationMemory(total_size=1024)
    print("Initial blocks:", mgr.dump())
    mgr.allocate("P1.S1", 200, policy="first")
    mgr.allocate("P2.S1", 300, policy="best")
    mgr.allocate("P3.S1", 50, policy="worst")
    print("After allocations:", mgr.dump())
    mgr.free("P2.S1")
    print("After freeing P2.S1:", mgr.dump())
    print("Fragmentation:", mgr.fragmentation())

if __name__ == "__main__":
    demo_paging()
    demo_segmentation()
