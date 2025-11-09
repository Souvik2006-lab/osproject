# visualization/visualizer.py

import matplotlib.pyplot as plt
from typing import List, Dict, Any


def plot_paging(history: List[List[Any]], title: str = "Paging Simulation"):
    """
    history: list of snapshots, each snapshot is list of length n_frames (page numbers or None)
    We'll plot a table-like grid: rows = steps, columns = frames. Use text annotations.
    """
    n_steps = len(history)
    if n_steps == 0:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "No data", ha="center")
        return fig

    n_frames = len(history[0])

    fig, ax = plt.subplots(figsize=(max(6, n_frames * 1.2), max(3, n_steps * 0.3)))
    ax.set_axis_off()
    table_data = []
    for row in history:
        # convert None to empty string
        table_data.append([("" if v is None else str(v)) for v in row])

    # draw table
    table = ax.table(cellText=table_data, colLabels=[f"F{i}" for i in range(n_frames)],
                     loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.2)
    ax.set_title(title)
    plt.tight_layout()
    return fig


def plot_segmentation(segments: List[Dict], total_memory: int):
    """
    segments: list of dicts with 'name','size','start','end'
    Plot a horizontal bar showing segments and free space.
    """
    fig, ax = plt.subplots(figsize=(10, 2))
    # Sort segments by start
    segs_sorted = sorted(segments, key=lambda s: s['start'])
    # Build bars: use start positions and sizes; we'll color segments, free spaces will be gray
    current = 0
    for seg in segs_sorted:
        if seg['start'] > current:
            # free space before this segment
            free_size = seg['start'] - current
            ax.barh(0, free_size, left=current, color='lightgray', edgecolor='black')
            current += free_size
        ax.barh(0, seg['size'], left=seg['start'], color='tab:blue', edgecolor='black')
        ax.text(seg['start'] + seg['size']/2, 0, f"{seg['name']} ({seg['size']})", va='center', ha='center', color='white', fontsize=9)
        current = seg['end'] + 1
    # trailing free space
    if current < total_memory:
        ax.barh(0, total_memory - current, left=current, color='lightgray', edgecolor='black')
    ax.set_xlim(0, total_memory)
    ax.set_yticks([])
    ax.set_xlabel("Memory Address")
    ax.set_title("Segmentation Layout")
    plt.tight_layout()
    return fig
