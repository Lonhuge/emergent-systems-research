"""
Run one condition x seed of the partial ecology. Writes JSON and WAV into results/ only.

Usage: python3 -I run.py --condition full --seed 0 --seconds 60 [--tag main]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sim.ecology import Ecology  # noqa: E402
from sim.metrics import snapshot, spectrum  # noqa: E402

RESULTS = os.path.join(HERE, "results")
CONDITIONS = {
    "full": {},
    "no_coupling": {"coupling": False},
    "shuffle_phase": {"shuffle_phase": True},
    "no_migration": {"migrate": False},
    "no_evolution": {"evolve": False},
}


def _safe(path):
    path = os.path.abspath(path)
    if os.path.commonpath([path, RESULTS]) != RESULTS:
        raise SystemExit("refusing to write outside results/")
    return path


def write_wav(path, x, sr):
    x = np.asarray(x, dtype=float)
    peak = np.max(np.abs(x)) if x.size else 0.0
    if peak > 0:
        x = 0.9 * x / peak
    fade = min(len(x) // 2, int(0.02 * sr))
    if fade:
        ramp = np.linspace(0, 1, fade)
        x[:fade] *= ramp
        x[-fade:] *= ramp[::-1]
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2")
    with wave.open(_safe(path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(pcm.tobytes())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--condition", required=True, choices=sorted(CONDITIONS))
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--seconds", type=float, default=60.0)
    ap.add_argument("--log-every", type=float, default=0.25)
    ap.add_argument("--tag", default="main")
    ap.add_argument("--audio", default="0:3,28:31,57:60", help="segments start:end in seconds, '' for none")
    ap.add_argument("--set", action="append", default=[], help="override param, e.g. --set g=1.3 (calibration only)")
    args = ap.parse_args()

    over = dict(CONDITIONS[args.condition])
    for kv in args.set:
        k, v = kv.split("=")
        over[k] = float(v)
    os.makedirs(RESULTS, exist_ok=True)
    eco = Ecology(seed=args.seed, **over)
    mrng = np.random.default_rng(10_000 + args.seed)
    steps = int(round(args.seconds / eco.dt))
    log_every = max(1, int(round(args.log_every / eco.dt)))
    segs = []
    if args.audio:
        for s in args.audio.split(","):
            a, b = s.split(":")
            segs.append((int(float(a) / eco.dt), int(float(b) / eco.dt), []))
    series, births, deaths = [], 0, 0
    t0 = time.time()
    for st in range(steps):
        render = any(a <= st < b for a, b, _ in segs)
        y = eco.step(render=render)
        births += eco.births
        deaths += eco.deaths
        if render:
            for a, b, buf in segs:
                if a <= st < b:
                    buf.append(y)
        if (st + 1) % log_every == 0:
            snap = snapshot(eco, mrng)
            snap["births_cum"], snap["deaths_cum"] = births, deaths
            series.append(snap)
            if not np.isfinite(snap.get("energy", 0.0)):
                break
    elapsed = time.time() - t0
    base = f"{args.tag}__{args.condition}__seed{args.seed}"
    audio_files = []
    for a, b, buf in segs:
        if buf:
            fn = f"{base}__{a * eco.dt:.0f}-{b * eco.dt:.0f}s.wav"
            write_wav(os.path.join(RESULTS, fn), np.concatenate(buf), eco.p["sr"])
            audio_files.append(fn)
    rec = {
        "tag": args.tag, "condition": args.condition, "seed": args.seed,
        "seconds": args.seconds, "elapsed_s": round(elapsed, 1),
        "params": {k: (bool(v) if isinstance(v, bool) else float(v)) for k, v in eco.p.items()},
        "births": births, "deaths": deaths, "series": series,
        "final_spectrum": spectrum(eco), "audio": audio_files,
        "body": {"x": eco.body_x[::20].round(3).tolist(),
                 "net_gain": eco.body_net_gain(eco.body_x[::20]).round(4).tolist()},
    }
    with open(_safe(os.path.join(RESULTS, base + ".json")), "w") as fh:
        json.dump(rec, fh)
    last = series[-1] if series else {}
    print(f"{args.condition:14s} seed={args.seed} n={last.get('n')} H+={last.get('harmonicity_excess', float('nan')):.3f} "
          f"lock={last.get('lock_coherence', float('nan')):.3f} births={births} deaths={deaths} {elapsed:.0f}s")


if __name__ == "__main__":
    main()
