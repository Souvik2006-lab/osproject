# core/paging_core.py

from typing import List, Tuple, Any

class PagingSimulation:
    """
    PagingSimulation supports LRU, Optimal, FIFO and Second Chance (Clock).
    Methods provided:
      - simulate_LRU()
      - simulate_Optimal()
      - simulate_FIFO()
      - simulate_SecondChance()    <-- matches GUI call
      - run_all()                 <-- runs based on self.algorithm
    """

    def __init__(self, reference_string: List[int], n_frames: int = 3, algorithm: str = "LRU"):
        self.reference_string = list(reference_string)
        self.n_frames = int(n_frames)
        self.algorithm = algorithm.upper()
        self.frames: List[Any] = []
        self.page_faults: int = 0
        self.history: List[List[Any]] = []

    def _init_state(self):
        self.frames = []
        self.page_faults = 0
        self.history = []

    # ---------------- LRU ----------------
    def simulate_LRU(self) -> Tuple[int, List[List[Any]]]:
        self._init_state()
        last_used = {}
        for idx, page in enumerate(self.reference_string):
            if page in self.frames:
                last_used[page] = idx
            else:
                self.page_faults += 1
                if len(self.frames) < self.n_frames:
                    self.frames.append(page)
                    last_used[page] = idx
                else:
                    # evict least recently used
                    lru_page = min(self.frames, key=lambda p: last_used.get(p, -1))
                    ev_idx = self.frames.index(lru_page)
                    self.frames[ev_idx] = page
                    if lru_page in last_used:
                        del last_used[lru_page]
                    last_used[page] = idx
            snapshot = list(self.frames)
            while len(snapshot) < self.n_frames:
                snapshot.append(None)
            self.history.append(snapshot.copy())
        return self.page_faults, self.history

    # ---------------- OPTIMAL ----------------
    def simulate_Optimal(self) -> Tuple[int, List[List[Any]]]:
        self._init_state()
        refs = self.reference_string
        for idx, page in enumerate(refs):
            if page in self.frames:
                pass
            else:
                self.page_faults += 1
                if len(self.frames) < self.n_frames:
                    self.frames.append(page)
                else:
                    next_uses = {}
                    for p in self.frames:
                        try:
                            next_idx = refs.index(p, idx + 1)
                        except ValueError:
                            next_idx = float('inf')
                        next_uses[p] = next_idx
                    victim = max(self.frames, key=lambda p: next_uses[p])
                    ev_idx = self.frames.index(victim)
                    self.frames[ev_idx] = page
            snapshot = list(self.frames)
            while len(snapshot) < self.n_frames:
                snapshot.append(None)
            self.history.append(snapshot.copy())
        return self.page_faults, self.history

    # ---------------- FIFO ----------------
    def simulate_FIFO(self) -> Tuple[int, List[List[Any]]]:
        self._init_state()
        from collections import deque
        queue = deque()
        in_frames = set()

        for page in self.reference_string:
            if page in in_frames:
                # hit
                pass
            else:
                self.page_faults += 1
                if len(queue) < self.n_frames:
                    queue.append(page)
                    in_frames.add(page)
                    self.frames.append(page)
                else:
                    oldest = queue.popleft()
                    in_frames.remove(oldest)
                    queue.append(page)
                    in_frames.add(page)
                    # replace oldest in frames list
                    try:
                        idx = self.frames.index(oldest)
                        self.frames[idx] = page
                    except ValueError:
                        # safety fallback
                        self.frames[0] = page
            snapshot = list(self.frames)
            while len(snapshot) < self.n_frames:
                snapshot.append(None)
            self.history.append(snapshot.copy())
        return self.page_faults, self.history

    # ---------------- Second Chance (Clock) ----------------
    def simulate_SecondChance(self) -> Tuple[int, List[List[Any]]]:
        """
        Implements second-chance (clock) algorithm.
        Uses frames[], ref_bits dict and a pointer 'hand'.
        Method name intentionally 'simulate_SecondChance' to match GUI.
        """
        self._init_state()
        ref_bits = {}          # page -> bit (0/1)
        clock_hand = 0         # index into frames list

        for page in self.reference_string:
            if page in self.frames:
                ref_bits[page] = 1
            else:
                self.page_faults += 1
                if len(self.frames) < self.n_frames:
                    self.frames.append(page)
                    ref_bits[page] = 1
                else:
                    # find victim
                    while True:
                        clock_hand %= self.n_frames
                        current_page = self.frames[clock_hand]
                        bit = ref_bits.get(current_page, 0)
                        if bit == 0:
                            # evict current_page
                            evicted = current_page
                            self.frames[clock_hand] = page
                            if evicted in ref_bits:
                                del ref_bits[evicted]
                            ref_bits[page] = 1
                            clock_hand = (clock_hand + 1) % self.n_frames
                            break
                        else:
                            # give second chance
                            ref_bits[current_page] = 0
                            clock_hand = (clock_hand + 1) % self.n_frames
            snapshot = list(self.frames)
            while len(snapshot) < self.n_frames:
                snapshot.append(None)
            self.history.append(snapshot.copy())

        return self.page_faults, self.history

    # ---------------- Generic runner ----------------
    def run_all(self) -> Tuple[int, List[List[Any]]]:
        algo = self.algorithm.upper()
        if algo == "LRU":
            return self.simulate_LRU()
        elif algo in ("OPTIMAL", "OPT"):
            return self.simulate_Optimal()
        elif algo == "FIFO":
            return self.simulate_FIFO()
        elif algo in ("SECOND CHANCE", "SECOND_CHANCE", "SECOND-CHANCE", "SC", "CLOCK", "SECONDCHANCE"):
            return self.simulate_SecondChance()
        else:
            raise ValueError(f"Unknown algorithm: {self.algorithm}")
