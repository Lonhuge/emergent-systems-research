"""
Evaluate the pre-registered hypotheses (see PRE_REGISTRATION.md).

Per run: mean of each metric over the last 25% of the run (the tail).
Per comparison: ROBUST only if the seed distributions are fully separated
AND |Cohen's d| > 2. With 5 vs 5 seeds full separation alone corresponds to an
exact Mann-Whitney p = 0.008 (two-sided 0.016).

Usage: python3 -I analyze.py --tag main
"""
from __future__ import annotations

import argparse
import glob
import json
import os
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")
ORDER = ["full", "no_coupling", "shuffle_phase", "no_migration", "no_evolution"]

PRIMARY = [
    ("H1a", "harmonicity_excess", "full", "no_coupling", ">"),
    ("H1b", "harmonicity_excess", "full", "shuffle_phase", ">"),
    ("H2a", "lock_coherence", "full", "no_coupling", ">"),
    ("H2b", "lock_coherence", "full", "shuffle_phase", ">"),
    ("H3", "harmonicity_excess", "full", "no_migration", ">"),
    ("H4", "harmonicity_excess", "full", "no_evolution", ">"),
]
SECONDARY = [
    "harmonicity_raw", "triad_closure_excess", "lock_magnitude", "n", "energy",
    "centroid_hz", "spectral_entropy_bits", "body_alignment", "openness_mean",
    "speed_abs_mean", "lineages_alive", "n_triads", "gen_mean", "gen_max", "genome_dist_mean",
]


def load(tag):
    runs = defaultdict(list)
    for f in sorted(glob.glob(os.path.join(RESULTS, f"{tag}__*.json"))):
        r = json.load(open(f))
        runs[r["condition"]].append(r)
    return runs


def tail(run, key, frac=0.25):
    s = [x[key] for x in run["series"] if key in x and x["n"] > 0 and x[key] is not None and np.isfinite(x[key])]
    if not s:
        return np.nan
    k = max(1, int(len(s) * frac))
    return float(np.mean(s[-k:]))


def compare(a, b, direction):
    a, b = np.asarray(a, float), np.asarray(b, float)
    a, b = a[np.isfinite(a)], b[np.isfinite(b)]
    if a.size < 3 or b.size < 3:
        return "insufficient", np.nan
    pooled = np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
    d = (a.mean() - b.mean()) / pooled if pooled > 0 else np.sign(a.mean() - b.mean()) * np.inf
    sep_up = a.min() > b.max()
    sep_down = a.max() < b.min()
    if direction == ">" and sep_up and d > 2:
        return "SUPPORTED", d
    if direction == ">" and sep_down and d < -2:
        return "REVERSED", d
    return "not supported", d


def fmt(v):
    v = np.asarray(v, float)
    v = v[np.isfinite(v)]
    if not v.size:
        return "–"
    return f"{v.mean():.3f} ± {v.std(ddof=1) if v.size > 1 else 0:.3f}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="main")
    args = ap.parse_args()
    runs = load(args.tag)
    conds = [c for c in ORDER if c in runs]
    L = [f"# Partial ecology, phase 1 (open): results for tag `{args.tag}`", ""]
    L.append("Runs: " + ", ".join(f"{c} {len(runs[c])}" for c in conds))
    ext = {c: sum(1 for r in runs[c] if r["series"][-1]["n"] == 0) for c in conds}
    capped = {c: sum(1 for r in runs[c] if max(x["n"] for x in r["series"]) >= r["params"]["n_max"]) for c in conds}
    L.append("Extinct at end: " + ", ".join(f"{c} {ext[c]}" for c in conds))
    L.append("Runs that ever hit the population cap: " + ", ".join(f"{c} {capped[c]}" for c in conds))
    L.append("")
    L.append("## Pre-registered hypotheses")
    L.append("")
    L.append("| id | metric | full | baseline | baseline value | d | verdict |")
    L.append("|---|---|---|---|---|---|---|")
    for hid, key, ca, cb, dirn in PRIMARY:
        if ca not in runs or cb not in runs:
            continue
        va = [tail(r, key) for r in runs[ca]]
        vb = [tail(r, key) for r in runs[cb]]
        verdict, d = compare(va, vb, dirn)
        L.append(f"| {hid} | {key} | {fmt(va)} | {cb} | {fmt(vb)} | {d:+.2f} | **{verdict}** |")
    L.append("")
    L.append("## All metrics, tail means (mean ± sd over seeds)")
    L.append("")
    L.append("| metric | " + " | ".join(conds) + " |")
    L.append("|---|" + "---|" * len(conds))
    for key in ["harmonicity_excess", "lock_coherence"] + SECONDARY:
        L.append(f"| {key} | " + " | ".join(fmt([tail(r, key) for r in runs[c]]) for c in conds) + " |")
    L.append("")
    L.append("## Per-seed harmonicity excess and lock coherence (tail)")
    L.append("")
    for c in conds:
        he = ", ".join(f"{tail(r, 'harmonicity_excess'):+.3f}" for r in sorted(runs[c], key=lambda r: r["seed"]))
        lc = ", ".join(f"{tail(r, 'lock_coherence'):+.3f}" for r in sorted(runs[c], key=lambda r: r["seed"]))
        L.append(f"- **{c}**: H+ [{he}]; lock [{lc}]")
    L.append("")
    L.append("## Time course of harmonicity excess (seed mean)")
    L.append("")
    T = min(len(r["series"]) for c in conds for r in runs[c])
    idx = sorted(set(list(range(0, T, max(1, T // 12))) + [T - 1]))
    L.append("| t (s) | " + " | ".join(conds) + " |")
    L.append("|---|" + "---|" * len(conds))
    for i in idx:
        t = runs[conds[0]][0]["series"][i]["t_s"]
        row = []
        for c in conds:
            vals = [r["series"][i].get("harmonicity_excess", np.nan) for r in runs[c]]
            vals = [v for v in vals if v is not None and np.isfinite(v)]
            row.append(f"{np.mean(vals):+.3f}" if vals else "–")
        L.append(f"| {t:.1f} | " + " | ".join(row) + " |")
    L.append("")
    L.append("## Final spectra, seed 0 (strongest 12 partials, Hz : amplitude)")
    L.append("")
    for c in conds:
        r0 = sorted(runs[c], key=lambda r: r["seed"])[0]
        sp = sorted(r0["final_spectrum"], key=lambda p: -p[1])[:12]
        sp = sorted(sp)
        L.append(f"- **{c}** (n={r0['series'][-1]['n']}): " + ", ".join(f"{f:.1f}:{a:.3f}" for f, a in sp))
    text = "\n".join(L)
    with open(os.path.join(RESULTS, f"summary_{args.tag}.md"), "w") as fh:
        fh.write(text)
    print(text)


if __name__ == "__main__":
    main()
