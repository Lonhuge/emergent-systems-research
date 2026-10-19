"""
Fast notes: run many 4-second notes for one condition in one process.
Writes one JSON line per note into results/notes_<tag>__<condition>__<first>-<last>.jsonl
and WAV files for seeds below --audio-below. Writes nothing outside results/.

Usage: python3 -I run_notes.py --condition full --seeds 0:50 --tag main [--audio-below 10]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sim.ecology import Ecology  # noqa: E402
from sim.fast import fast_params  # noqa: E402
from sim.metrics import snapshot, spectrum  # noqa: E402
from run import write_wav, RESULTS, _safe  # noqa: E402

CONDITIONS = {
    "full": {},
    "no_coupling": {"coupling": False},
    "shuffle_phase": {"shuffle_phase": True},
    "no_migration": {"migrate": False},
}
NOTE_S = 4.0
LOG_EVERY_S = 0.05


def run_note(cond, seed, audio):
    p = fast_params()
    p.update(CONDITIONS[cond])
    eco = Ecology(seed=seed, **p)
    mrng = np.random.default_rng(10_000 + seed)
    steps = int(round(NOTE_S / eco.dt))
    log_every = int(round(LOG_EVERY_S / eco.dt))
    series, buf = [], []
    births = deaths = 0
    for st in range(steps):
        y = eco.step(render=audio)
        births += eco.births
        deaths += eco.deaths
        if audio:
            buf.append(y)
        if (st + 1) % log_every == 0:
            series.append(snapshot(eco, mrng))
    rec = {"condition": cond, "seed": seed, "births": births, "deaths": deaths,
           "n_max_seen": max(s["n"] for s in series), "series": series,
           "final_spectrum": spectrum(eco)}
    return rec, (np.concatenate(buf) if audio else None), eco.p["sr"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--condition", required=True, choices=sorted(CONDITIONS))
    ap.add_argument("--seeds", required=True, help="a:b, half-open")
    ap.add_argument("--tag", default="main")
    ap.add_argument("--audio-below", type=int, default=10)
    args = ap.parse_args()
    a, b = (int(v) for v in args.seeds.split(":"))
    os.makedirs(RESULTS, exist_ok=True)
    out = _safe(os.path.join(RESULTS, f"notes_{args.tag}__{args.condition}__{a}-{b - 1}.jsonl"))
    t0 = time.time()
    n_ext = 0
    with open(out, "w") as fh:
        for seed in range(a, b):
            audio = seed < args.audio_below
            rec, y, sr = run_note(args.condition, seed, audio)
            n_ext += rec["series"][-1]["n"] == 0
            if audio:
                fn = f"notes_{args.tag}__{args.condition}__seed{seed}.wav"
                write_wav(os.path.join(RESULTS, fn), y, sr)
                rec["audio"] = fn
            fh.write(json.dumps(rec) + "\n")
    # viability only
    print(f"{args.condition:14s} seeds {a}-{b - 1}: {b - a} notes, extinct {n_ext}, {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
