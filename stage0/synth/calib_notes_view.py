"""Viability view for fast-note calibration. Prints no emergence metrics, by design."""
import glob, json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
tag = sys.argv[1]
for f in sorted(glob.glob(os.path.join(HERE, "results", f"notes_{tag}__*.jsonl"))):
    recs = [json.loads(l) for l in open(f)]
    c = recs[0]["condition"]
    def at(r, t):
        return min(r["series"], key=lambda s: abs(s["t_s"] - t))
    n1 = [at(r, 1.0)["n"] for r in recs]; n4 = [at(r, 4.0)["n"] for r in recs]
    e4 = [at(r, 4.0).get("energy", 0) for r in recs]
    ext = sum(1 for r in recs if r["series"][-1]["n"] == 0)
    few = sum(1 for r in recs if r["series"][-1]["n"] < 3)
    cap = sum(1 for r in recs if r["n_max_seen"] >= 160)
    print(f"{c:14s} notes={len(recs)} extinct={ext} n<3={few} cap_hits={cap} "
          f"n@1s med={np.median(n1):.0f} n@4s med={np.median(n4):.0f} [{min(n4)}-{max(n4)}] E@4s med={np.median(e4):.2f}")
