"""Amendment B: cluster-robust harmonicity on final spectra (t = 4 s). See PRE_REGISTRATION_notes.md."""
from __future__ import annotations

import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from analyze_notes import load, win_vals, wilcoxon, RESULTS  # noqa: E402
from sim.metrics import cluster_harmonicity_excess  # noqa: E402

CONDS = ["full", "no_coupling", "shuffle_phase", "no_migration", "no_migration_no_coupling"]


def main():
    data = load("main")
    seeds = sorted(set.intersection(*[set(data[c]) for c in CONDS if c in data]))
    ch, ncl, viable = {}, {}, {}
    for c in CONDS:
        for s in seeds:
            r = data[c][s]
            sp = np.asarray(r["final_spectrum"], float).reshape(-1, 2)
            rng = np.random.default_rng(20_000 + s)
            if sp.shape[0] >= 3:
                e, k = cluster_harmonicity_excess(sp[:, 0], sp[:, 1] ** 2, rng)
            else:
                e, k = 0.0, int(sp.shape[0])
            ch[(c, s)], ncl[(c, s)] = e, k
            viable[(c, s)] = win_vals(r, "n")[1]
    L = ["# Amendment B: artefact check", "", f"Seeds: {len(seeds)}", ""]
    L.append("| condition | viable notes | mean clusters (viable) | partials per cluster (viable) | cluster-robust excess (viable) | pre-registered excess (viable) |")
    L.append("|---|---|---|---|---|---|")
    for c in CONDS:
        vs = [s for s in seeds if viable[(c, s)]]
        if not vs:
            continue
        npart = [len(data[c][s]["final_spectrum"]) for s in vs]
        k = [ncl[(c, s)] for s in vs]
        L.append(f"| {c} | {len(vs)} | {np.mean(k):.1f} | {np.mean(np.array(npart) / np.maximum(k, 1)):.2f} | "
                 f"{np.mean([ch[(c, s)] for s in vs]):+.3f} | {np.mean([win_vals(data[c][s], 'harmonicity_excess')[0] for s in vs]):+.3f} |")
    L.append("")
    # C1
    use = [s for s in seeds if viable[("no_migration", s)] and viable[("no_migration_no_coupling", s)]]
    d = np.array([ch[("no_migration", s)] - ch[("no_migration_no_coupling", s)] for s in use])
    p, r, nz = wilcoxon(d, ">")
    v1 = "SUPPORTED" if (np.isfinite(p) and p < 0.001 and r > 0.3) else "not supported"
    L.append(f"**C1** cluster-robust excess, no_migration > no_migration_no_coupling: pairs {len(use)} (nonzero {nz}), "
             f"median d {np.median(d):+.4f}, r {r:+.2f}, p {p:.2g} → **{v1}**")
    # C2
    vs = [s for s in seeds if viable[("no_coupling", s)]]
    x = np.array([ch[("no_coupling", s)] for s in vs])
    p2, r2, nz2 = wilcoxon(x, ">")
    v2 = "SUPPORTED (metric still biased)" if (np.isfinite(p2) and p2 < 0.001 and r2 > 0.3) else "not supported (no residual bias detected)"
    L.append(f"**C2** cluster-robust excess in viable no_coupling notes > 0: n {len(vs)} (nonzero {nz2}), "
             f"mean {x.mean():+.4f}, r {r2:+.2f}, p {p2:.2g} → **{v2}**")
    L.append("")
    # extra exploratory: full vs no_coupling on cluster-robust metric, viable pairs
    use = [s for s in seeds if viable[("full", s)] and viable[("no_coupling", s)]]
    d = np.array([ch[("full", s)] - ch[("no_coupling", s)] for s in use])
    p3, r3, nz3 = wilcoxon(d, ">")
    L.append(f"Exploratory: cluster-robust excess, full > no_coupling on jointly viable pairs: pairs {len(use)}, "
             f"median d {np.median(d):+.4f}, r {r3:+.2f}, p {p3:.2g}")
    top = sorted(seeds, key=lambda s: -ch[("no_migration", s)])[:5]
    L.append("")
    L.append("Highest cluster-robust excess in no_migration (seed: excess, clusters): " +
             ", ".join(f"{s}: {ch[('no_migration', s)]:+.2f}, {ncl[('no_migration', s)]}" for s in top))
    text = "\n".join(L)
    open(os.path.join(RESULTS, "summary_artefact.md"), "w").write(text)
    print(text)


if __name__ == "__main__":
    main()
