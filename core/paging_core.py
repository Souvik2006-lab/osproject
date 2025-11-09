# core/paging_core.py

from collections import OrderedDict, deque
from typing import List, Tuple


class PagingSimulation:
    """
    Simple paging simulator with LRU and Optimal replacement.
    Constructor:
        PagingSimulation(reference_string: List[int], n_frames: int, algorithm: str)
    Methods:
        simulate_LRU() -> (total_faults:int, history: List[List[int]])
        simulate_Optimal() -> (total_faults:int, history: List[List[int]])
    Where `history` is a list of frame-lists after each reference (useful for plotting).
    """

    def __init__(self, reference_string: List[int], n_frames: int = 3, algorithm: str = "LRU"):
        self.reference_string = list(reference_string)
        self.n_frames = int(n_frames)
        self.algorithm = algorithm.upper()
        # history will be list of snapshots (list of pages in frames) per step
        self.history = []

    def _init_state(self):
        self.frames = []  # list of pages currently in frames (length <= n_frames)
        self.page_faults = 0
        self.history = []

    def simulate_LRU(self) -> Tuple[int, List[List[int]]]:
        self._init_state()
        # Keep last-used index map
        last_used = {}

        for idx, page in enumerate(self.reference_string):
            if page in self.frames:
                # hit: update last used
                last_used[page] = idx
            else:
                # fault
                self.page_faults += 1
                if len(self.frames) < self.n_frames:
                    # empty slot available
                    self.frames.append(page)
                    last_used[page] = idx
                else:
                    # evict least recently used
                    # choose page in frames with smallest last_used (if some not in last_used, treat as -inf)
                    lru_page = min(self.frames, key=lambda p: last_used.get(p, -1))
                    ev_idx = self.frames.index(lru_page)
                    # replace
                    self.frames[ev_idx] = page
                    # update last used dict
                    if lru_page in last_used:
                        del last_used[lru_page]
                    last_used[page] = idx
            # record snapshot copy (pad with None for empty frames to keep width consistent)
            snapshot = list(self.frames)
            # ensure snapshot length equals n_frames (for plotting)
            while len(snapshot) < self.n_frames:
                snapshot.append(None)
            self.history.append(snapshot.copy())

        return self.page_faults, self.history

    def simulate_Optimal(self) -> Tuple[int, List[List[int]]]:
        self._init_state()
        refs = self.reference_string

        for idx, page in enumerate(refs):
            if page in self.frames:
                # hit
                pass
            else:
                # fault
                self.page_faults += 1
                if len(self.frames) < self.n_frames:
                    self.frames.append(page)
                else:
                    # For each page in frames, find next use index (or infinity)
                    next_uses = {}
                    for p in self.frames:
                        try:
                            next_idx = refs.index(p, idx + 1)
                        except ValueError:
                            next_idx = float('inf')
                        next_uses[p] = next_idx
                    # choose page with farthest next use
                    victim = max(self.frames, key=lambda p: next_uses[p])
                    ev_idx = self.frames.index(victim)
                    self.frames[ev_idx] = page
            snapshot = list(self.frames)
            while len(snapshot) < self.n_frames:
                snapshot.append(None)
            self.history.append(snapshot.copy())

        return self.page_faults, self.history
