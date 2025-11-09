"""
experiments/analysis_tools.py
Simple helpers for loading results and plotting (used by experiment_runner or for reports).
"""

import pandas as pd
import matplotlib.pyplot as plt


def load_summary(csv_path: str) -> pd.DataFrame:
    return pd.read_csv(csv_path)


def plot_faults_vs_frames(df: pd.DataFrame, out_path: str):
    plt.figure(figsize=(8,5))
    for alg in df['algorithm'].unique():
        sub = df[df['algorithm'] == alg].sort_values('frames')
        plt.plot(sub['frames'], sub['total_faults'], marker='o', label=alg)
    plt.xlabel("Frames")
    plt.ylabel("Total Faults")
    plt.title("Faults vs Frames")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
