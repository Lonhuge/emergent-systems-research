"""
Evaluate PRE_REGISTRATION_notes.md (paired design, fast notes).

Per note: window mean over 2.0-4.0 s. Snapshots with fewer than 3 partials
(or no triads) count as 0 for harmonicity excess and lock coherence
(intention-to-treat). A note is "viable" if it has >= 3 partials in every
snapshot of the window.

Test: paired differences d_i = full_i - baseline_i. Wilcoxon signed-rank
(zeros dropped, normal approximation with tie correction), one-sided in the
predicted direction, plus matched-pairs rank-biserial r.
SUPPORTED: p < 0.001 and r > 0.3. REVERSED: same in the opposite direction.

Usage: python3 -I analyze_notes.py --tag main
"""
from __future__ import annotations

import argparse
import glob
import json
import math
import os
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")
WIN = (2.0, 4.0)
CONDS = ["full", "no_coupling", "shuffle_phase", "no_migration"]
# id, metric, baseline, sample ("itt" or "viable")
HYP = [
    ("N-H1a", "harmonicity_excess", "no_coupling", "itt"),
    ("N-H1b", "harmonicity_excess", "shuffle_phase", "itt"),
    ("N-H2a", "lock_coherence", "no_coupling", "itt"),
    ("N-H2b", "lock_coherence", "shuffle_phase", "itt"),
    ("N-H3", "harmonicity_excess", "no_migration", "viable"),
]


def load(tag):
    data = defaultdict(dict)
    for f in glob.glob(os.path.join(RESULTS, f"notes_{tag}__*.jsonl")):
        for line in open(f):
            r = json.loads(line)
            data[r["condition"]][r["seed"]] = r
    return data


def win_vals(rec, key):
    vals, viable = [], True
    for s in rec["series"]:
        if WIN[0] - 1e-9 <= s["t_s"] <= WIN[1] + 1e-9:
            v = s.get(key)
            if s["n"] < 3 or v is None or not np.isfinite(v):
                v = 0.0
            if s["n"] < 3:
                viable = False
            vals.append(v)
    return (float(np.mean(vals)) if vals else 0.0), viable


def wilcoxon(d, direction):
    d = np.asarray(d, float)
    d = d[np.abs(d) > 1e-12]
    n = d.size
    if n < 10:
        return np.nan, np.nan, n
    absd = np.abs(d)
    order = np.argsort(absd)
    ranks = np.empty(n)
    sa = absd[order]
    i = 0
    tie_term = 0.0
    while i < n:
        j = i
        while j + 1 < n and sa[j + 1] == sa[i]:
            j += 1
        ranks[order[i:j + 1]] = (i + j) / 2.0 + 1.0
        t = j - i + 1
        tie_term += t ** 3 - t
        i = j + 1
    wp = ranks[d > 0].sum()
    wm = ranks[d < 0].sum()
    mean = n * (n + 1) / 4.0
    var = n * (n + 1) * (2 * n + 1) / 24.0 - tie_term / 48.0
    z = (wp - mean) / math.sqrt(var)
    if direction == "<":
        z = -z
    p = 0.5 * math.erfc(z / math.sqrt(2.0))
    r = (wp - wm) / (wp + wm)
    if direction == "<":
        r = -r
    return p, r, n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="main")
    args = ap.parse_args()
    data = load(args.tag)
    conds = [c for c in CONDS if c in data]
    seeds = sorted(set.intersection(*[set(data[c]) for c in conds]))
    L = [f"# Fast notes: results for tag `{args.tag}`", "",
         f"Paired seeds present in all conditions: {len(seeds)}. Window {WIN[0]}–{WIN[1]} s.", ""]
    L.append("## Survival")
    L.append("")
    L.append("| condition | extinct at 4 s | viable in window | population cap reached |")
    L.append("|---|---|---|---|")
    vals = {}
    for c in conds:
        ext = sum(1 for s in seeds if data[c][s]["series"][-1]["n"] == 0)
        via = 0
        for key in ["harmonicity_excess", "lock_coherence", "harmonicity_raw", "triad_closure_excess",
                    "lock_magnitude", "n", "energy", "centroid_hz", "spectral_entropy_bits"]:
            for s in seeds:
                v, ok = win_vals(data[c][s], key)
                vals[(c, key, s)] = (v, ok)
        via = sum(1 for s in seeds if vals[(c, "n", s)][1])
        cap = sum(1 for s in seeds if data[c][s]["n_max_seen"] >= 160)
        L.append(f"| {c} | {ext} ({ext / len(seeds):.0%}) | {via} ({via / len(seeds):.0%}) | {cap} |")
    L.append("")
    L.append("## Pre-registered hypotheses")
    L.append("")
    L.append("| id | metric | baseline | sample | pairs used | median d | mean full | mean base | r | p (one-sided) | verdict |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for hid, key, base, sample in HYP:
        if base not in data:
            continue
        use = seeds if sample == "itt" else [s for s in seeds if vals[("full", key, s)][1] and vals[(base, key, s)][1]]
        fa = np.array([vals[("full", key, s)][0] for s in use])
        fb = np.array([vals[(base, key, s)][0] for s in use])
        d = fa - fb
        p, r, nz = wilcoxon(d, ">")
        pr, rr, _ = wilcoxon(d, "<")
        if np.isfinite(p) and p < 0.001 and r > 0.3:
            verdict = "SUPPORTED"
        elif np.isfinite(pr) and pr < 0.001 and rr > 0.3:
            verdict = "REVERSED"
        else:
            verdict = "not supported"
        L.append(f"| {hid} | {key} | {base} | {sample} | {len(use)} (nonzero {nz}) | {np.median(d):+.4f} | "
                 f"{fa.mean():+.4f} | {fb.mean():+.4f} | {r:+.2f} | {p:.2g} | **{verdict}** |")
    L.append("")
    L.append("## Exploratory: window means among notes viable in the given condition")
    L.append("")
    keys = ["harmonicity_excess", "lock_coherence", "harmonicity_raw", "triad_closure_excess", "n", "energy",
            "centroid_hz", "spectral_entropy_bits"]
    L.append("| metric | " + " | ".join(conds) + " |")
    L.append("|---|" + "---|" * len(conds))
    for key in keys:
        row = []
        for c in conds:
            v = [vals[(c, key, s)][0] for s in seeds if vals[(c, "n", s)][1]]
            row.append(f"{np.mean(v):.3f} (n={len(v)})" if v else "–")
        L.append(f"| {key} | " + " | ".join(row) + " |")
    L.append("")
    L.append("## Exploratory: time course of harmonicity excess, mean over notes viable at that time")
    L.append("")
    ts = [0.05, 0.1, 0.2, 0.3, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0]
    L.append("| t (s) | " + " | ".join(conds) + " |")
    L.append("|---|" + "---|" * len(conds))
    for t in ts:
        row = []
        for c in conds:
            v = []
            for s in seeds:
                snap = min(data[c][s]["series"], key=lambda x: abs(x["t_s"] - t))
                if snap["n"] >= 3 and snap.get("harmonicity_excess") is not None and np.isfinite(snap["harmonicity_excess"]):
                    v.append(snap["harmonicity_excess"])
            row.append(f"{np.mean(v):+.3f} (n={len(v)})" if v else "–")
        L.append(f"| {t} | " + " | ".join(row) + " |")
    text = "\n".join(L)
    with open(os.path.join(RESULTS, f"summary_notes_{args.tag}.md"), "w") as fh:
        fh.write(text)
    print(text)


if __name__ == "__main__":
    main()
