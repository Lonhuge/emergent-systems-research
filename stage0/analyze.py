"""
Compare conditions and apply the emergence criteria from ../PRINCIPLES.md.

For every metric: mean over the last 25% of each run, then mean +/- sd across
seeds per condition. A difference between `full` and a baseline is called
ROBUST only if (a) the seed distributions do not overlap at all (rank-based,
equivalent to exact Mann-Whitney p = 2/C(n1+n2, n1), i.e. p = 0.008 for 5 vs 5)
and (b) |difference| exceeds 2 pooled standard deviations.

Usage: python3 -I analyze.py [--tag main] [--out results/summary_main.md]
"""
from __future__ import annotations

import argparse
import glob
import json
import os
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(HERE, "results")

METRICS = [
    ("n", "population"),
    ("lineages_effective", "effective lineages"),
    ("genome_dist_mean", "genome diversity"),
    ("speed_mean", "mean speed"),
    ("turn_abs_mean", "mean |turn|"),
    ("clark_evans", "Clark-Evans (1=random, <1 clustered)"),
    ("corr_density_capacity", "corr(density, capacity)"),
    ("corr_density_resource", "corr(density, resource)"),
    ("polarisation_local", "local polarisation"),
    ("polarisation_global", "global polarisation"),
    ("neighbours_mean", "mean neighbours"),
    ("signal_mean", "signal mean"),
    ("signal_std", "signal std"),
    ("signal_entropy_bits", "signal entropy (bits)"),
    ("signal_morans_I", "signal Moran's I"),
    ("mi_signal_neighbour_signal_bits", "MI(signal, neighbour signal)"),
    ("mi_signal_resource_bits", "MI(signal, resource)"),
    ("mi_signal_energy_bits", "MI(signal, energy)"),
]


def load(tag):
    runs = []
    for f in sorted(glob.glob(os.path.join(RESULTS_DIR, f"{tag}__*.json"))):
        with open(f) as fh:
            runs.append(json.load(fh))
    return runs


def tail_mean(run, key):
    s = [r[key] for r in run["series"] if key in r and r["n"] > 0]
    if not s:
        return np.nan
    k = max(1, len(s) // 4)
    return float(np.mean(s[-k:]))


def separated(a, b):
    a, b = np.asarray(a), np.asarray(b)
    a, b = a[~np.isnan(a)], b[~np.isnan(b)]
    if a.size < 2 or b.size < 2:
        return False, np.nan
    sep = a.min() > b.max() or b.min() > a.max()
    pooled = np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
    d = (a.mean() - b.mean()) / pooled if pooled > 0 else np.inf
    return bool(sep and abs(d) > 2), float(d)


def ascii_map(grid, chars=" .:-=+*#%@"):
    g = np.asarray(grid, dtype=float)
    if g.max() <= 0:
        return "(empty)"
    q = np.clip((g / g.max()) * (len(chars) - 1), 0, len(chars) - 1).astype(int)
    return "\n".join("".join(chars[v] for v in row) for row in q)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="main")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    runs = load(args.tag)
    if not runs:
        raise SystemExit("no results for tag " + args.tag)
    by = defaultdict(list)
    for r in runs:
        by[r["condition"]].append(r)
    conds = [c for c in ["full", "no_social", "shuffle_signal", "no_evolution"] if c in by]

    lines = [f"# Stage 0 results: tag `{args.tag}`", ""]
    lines.append("Runs per condition: " + ", ".join(f"{c}={len(by[c])}" for c in conds))
    steps = sorted({r['steps_requested'] for r in runs})
    lines.append(f"Steps requested: {steps}. Extinctions: " +
                 ", ".join(f"{c}: {sum(1 for r in by[c] if r['extinct_at'])}/{len(by[c])}" for c in conds))
    lines.append("")

    # table of tail means
    lines.append("## Tail means (last 25% of each run), mean ± sd across seeds")
    lines.append("")
    lines.append("| metric | " + " | ".join(conds) + " |")
    lines.append("|---|" + "---|" * len(conds))
    tails = {}
    for key, label in METRICS:
        row = [label]
        for c in conds:
            vals = np.array([tail_mean(r, key) for r in by[c]])
            tails[(key, c)] = vals
            v = vals[~np.isnan(vals)]
            row.append(f"{v.mean():.3f} ± {v.std(ddof=1) if v.size>1 else 0:.3f}" if v.size else "–")
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")

    # emergence tests
    lines.append("## Emergence tests: `full` vs each baseline")
    lines.append("")
    lines.append("ROBUST = seed distributions fully separated and |d| > 2 (see header of analyze.py). "
                 "Anything else is NOT a finding, whatever the means look like.")
    lines.append("")
    for base in [c for c in conds if c != "full"]:
        lines.append(f"### full vs {base}")
        lines.append("")
        lines.append("| metric | full | " + base + " | d | verdict |")
        lines.append("|---|---|---|---|---|")
        for key, label in METRICS:
            a, b = tails[(key, "full")], tails[(key, base)]
            ok, d = separated(a, b)
            fa, fb = a[~np.isnan(a)], b[~np.isnan(b)]
            lines.append(f"| {label} | {fa.mean():.3f} | {fb.mean():.3f} | {d:+.2f} | "
                         f"{'**ROBUST**' if ok else 'not robust'} |")
        lines.append("")

    # time course of a few key metrics for full
    lines.append("## Time course (`full`, seed-averaged)")
    lines.append("")
    keys = ["n", "signal_mean", "signal_std", "polarisation_local", "clark_evans", "mi_signal_resource_bits", "lineages_effective"]
    T = min(len(r["series"]) for r in by["full"])
    lines.append("| t | " + " | ".join(keys) + " |")
    lines.append("|---|" + "---|" * len(keys))
    picks = sorted(set([0, 1, 2, 4, 8] + list(range(0, T, max(1, T // 10))) + [T - 1]))
    for i in picks:
        if i >= T:
            continue
        row = [str(by["full"][0]["series"][i]["t"])]
        for k in keys:
            vals = [r["series"][i].get(k, np.nan) for r in by["full"]]
            row.append(f"{np.nanmean(vals):.3f}")
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")

    # final density maps
    lines.append("## Final agent density (seed 0 of each condition; capacity map for reference)")
    lines.append("")
    cap = by["full"][0]["final"]["capacity_map_coarse"]
    lines.append("capacity map (resource richness):")
    lines.append("```\n" + ascii_map(cap) + "\n```")
    for c in conds:
        dm = by[c][0]["final"]["density_map"]
        lines.append(f"{c}, seed {by[c][0]['seed']}, n={by[c][0]['series'][-1]['n']}:")
        lines.append("```\n" + (ascii_map(dm) if dm else "(extinct)") + "\n```")
    text = "\n".join(lines)
    out = args.out or os.path.join(RESULTS_DIR, f"summary_{args.tag}.md")
    with open(out, "w") as f:
        f.write(text)
    print(text)


if __name__ == "__main__":
    main()
