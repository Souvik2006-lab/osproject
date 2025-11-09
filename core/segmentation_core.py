# core/segmentation_core.py

from typing import List, Dict, Optional


class SegmentationSimulation:
    """
    Simple segmentation manager:
    - segments: list of dicts with keys {'name', 'size', 'start', 'end'}
    - allocate(name, size) -> message string
    - deallocate(name) -> message string
    """

    def __init__(self, total_memory: int):
        self.total_memory = int(total_memory)
        self.segments: List[Dict] = []
        self.free_memory = int(total_memory)

    def allocate(self, name: str, size: int) -> str:
        size = int(size)
        if size <= 0:
            return f"❌ Invalid size for segment {name}."
        if size > self.free_memory:
            return f"❌ Not enough memory to allocate segment {name} (requested {size}, free {self.free_memory})."
        # compute start as next available address (simple contiguous allocation)
        start = 0
        for seg in self.segments:
            start = max(start, seg['end'] + 1)
        end = start + size - 1
        self.segments.append({'name': name, 'size': size, 'start': start, 'end': end})
        self.free_memory -= size
        return f"✅ Segment '{name}' allocated [{start}..{end}] size={size}."

    def deallocate(self, name: str) -> str:
        for seg in list(self.segments):
            if seg['name'] == name:
                self.free_memory += seg['size']
                self.segments.remove(seg)
                # Optionally: we do not compact other segments (simple model)
                return f"🗑️ Segment '{name}' deallocated."
        return f"❌ Segment '{name}' not found."

    # helper accessors used by GUI
    def get_segments(self) -> List[Dict]:
        return self.segments

    def get_free_memory(self) -> int:
        return self.free_memory
