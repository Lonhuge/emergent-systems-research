"""
Run one condition x seed and write metrics to results/.

Usage: python3 -I run_experiment.py --condition full --seed 0 --steps 20000 [--patchiness 0.6] [--tag name]

Conditions
  full            all interaction on, evolution on
  no_social       agents cannot perceive each other (no-social-interaction baseline)
  shuffle_signal  neighbours read permuted signals (no information in the channel)
  no_evolution    offspring are exact copies (no adaptation)

Sandbox: this script imports only numpy and the standard library, writes only
inside results/ next to itself, and refuses any other output path.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim.world import World  # noqa: E402
from sim.metrics import snapshot, density_map  # noqa: E402

CONDITIONS = {
    "full": dict(),
    "no_social": dict(social=False),
    "shuffle_signal": dict(shuffle_signal=True),
    "no_evolution": dict(evolve=False),
}

RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--condition", required=True, choices=sorted(CONDITIONS))
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--steps", type=int, default=20000)
    ap.add_argument("--log-every", type=int, default=100)
    ap.add_argument("--patchiness", type=float, default=None)
    ap.add_argument("--n-max", type=int, default=None)
    ap.add_argument("--tag", default="main")
    args = ap.parse_args()

    overrides = dict(CONDITIONS[args.condition])
    if args.patchiness is not None:
        overrides["patchiness"] = args.patchiness
    if args.n_max is not None:
        overrides["n_max"] = args.n_max

    os.makedirs(RESULTS_DIR, exist_ok=True)
    out = os.path.join(RESULTS_DIR, f"{args.tag}__{args.condition}__seed{args.seed}.json")
    if os.path.commonpath([os.path.abspath(out), RESULTS_DIR]) != RESULTS_DIR:
        raise SystemExit("refusing to write outside results/")

    w = World(seed=args.seed, **overrides)
    series = []
    t0 = time.time()
    extinct_at = None
    for t in range(args.steps):
        w.step()
        if (t + 1) % args.log_every == 0 or t == 0:
            series.append(snapshot(w))
        if w.n == 0:
            extinct_at = w.t
            series.append(snapshot(w))
            break
    elapsed = time.time() - t0

    final = {
        "x": np.round(w.x, 2).tolist(), "y": np.round(w.y, 2).tolist(),
        "th": np.round(w.th, 3).tolist(), "sig": np.round(w.sig, 3).tolist(),
        "lineage": w.lineage.tolist(),
        "density_map": density_map(w).astype(int).tolist() if w.n else None,
        "capacity_map_coarse": w.cap.reshape(32, 2, 32, 2).mean(axis=(1, 3)).round(3).tolist(),
    }
    record = {
        "tag": args.tag, "condition": args.condition, "seed": args.seed,
        "steps_requested": args.steps, "steps_run": w.t, "extinct_at": extinct_at,
        "params": {k: (v if not isinstance(v, (np.floating, np.integer)) else float(v)) for k, v in w.p.items()},
        "elapsed_s": round(elapsed, 1), "series": series, "final": final,
    }
    with open(out, "w") as f:
        json.dump(record, f)
    last = series[-1]
    print(f"{args.condition} seed={args.seed} steps={w.t} n={last['n']} "
          f"elapsed={elapsed:.0f}s -> {os.path.relpath(out, RESULTS_DIR)}")


if __name__ == "__main__":
    main()
