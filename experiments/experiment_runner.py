"""
experiments/experiment_runner.py
Run batch experiments that sweep frames and algorithms, save CSV summary and plots.
"""

import os
from core.paging_core import PagingSimulation
import pandas as pd
import matplotlib.pyplot as plt


def run_batch(reference_string, frames_list, algos, out_dir="experiments/results"):
    os.makedirs(out_dir, exist_ok=True)
    results = []
    for alg in algos:
        for nf in frames_list:
            sim = PagingSimulation(n_frames=nf, algorithm=alg, reference_string=reference_string)
            sim.run_all()
            s = sim.summary()
            s.update({"algorithm": alg, "frames": nf})
            results.append(s)
            # save log
            logdf = sim.get_log()
            logdf.to_csv(os.path.join(out_dir, f"log_{alg}_f{nf}.csv"), index=False)
    df = pd.DataFrame(results)
    summary_csv = os.path.join(out_dir, "summary_results.csv")
    df.to_csv(summary_csv, index=False)

    # Plot faults vs frames
    plt.figure(figsize=(8,5))
    for alg in algos:
        sub = df[df["algorithm"] == alg].sort_values("frames")
        plt.plot(sub["frames"], sub["total_faults"], marker="o", label=alg)
    plt.title("Total Page Faults vs Frames")
    plt.xlabel("Frames")
    plt.ylabel("Total Faults")
    plt.grid(True)
    plt.legend()
    plt.savefig(os.path.join(out_dir, "faults_vs_frames.png"))
    plt.close()

    return summary_csv


if __name__ == "__main__":
    # demo run
    refs = [7,0,1,2,0,3,0,4,2,3,0,3]
    csv = run_batch(reference_string=refs, frames_list=[2,3,4,5], algos=["LRU","OPTIMAL"])
    print("Saved summary to:", csv)
