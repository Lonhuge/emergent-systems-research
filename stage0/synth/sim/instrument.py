"""
v2 instrument parameters for the breeding tool: fast notes (sim/fast.py) plus
pitch, combination-tone births, genome-defined body and capped phase pull.

A genome is one flat vector: controller weights (GENOME_LEN) followed by
N_BODY body genes. This module is the Python reference for the browser port.
"""
from __future__ import annotations

import numpy as np

from .ecology import GENOME_LEN, N_BODY, Ecology
from .fast import fast_params

V2_LEN = GENOME_LEN + N_BODY          # 87: fixed reed-like physics
N_PHYS = 18                           # 14 in the first v3 genomes (101 genes); later genes neutral when missing
N_PHYS_V3 = 14
FULL_LEN = V2_LEN + N_PHYS            # 105: genome carries instrument physics
NOTE_S = 4.0


def physics(genome):
    """Physics genes -> instrument physics (mirror of physics() in ui/engine.js)."""
    g = np.asarray(genome, float)
    if g.size < V2_LEN + N_PHYS_V3:
        return None
    u = list(1.0 / (1.0 + np.exp(-g[V2_LEN:FULL_LEN])))
    u += [None] * (N_PHYS - len(u))
    res = []
    for r in range(3):
        depth = max(0.0, 2 * u[3 + r] - 1)
        if depth > 0:
            res.append({"pos": 3 * u[6 + r], "depth": depth})
    return {"sustain": 0.01 * 400 ** u[0], "ramp": 0.001 * 300 ** u[1], "damp": 0.03 * (1 / 0.03) ** u[2],
            "res": res, "qs": 2 ** (4 * u[9] - 2), "bs": 2 ** (4 * u[10] - 2), "ns": 2 ** (4 * u[11] - 2),
            "tremD": max(0.0, 2 * u[12] - 1) * 0.6, "tremR": 2 + 8 * u[13],
            "strike": 0 if u[14] is None else int(round(24 * max(0.0, 2 * u[14] - 1))),
            "dtilt": 0.0 if u[15] is None else -0.5 + 2 * u[15],
            "detune": 0.012 if u[16] is None else 0.012 * 2 ** (2 - 4 * u[16]),
            "near": 2.0 if u[16] is None else 2.0 * 2 ** (2 * u[16] - 1),
            "tilt": 0.35 if u[17] is None else 0.35 * 2 ** (1.5 - 3 * u[17])}


def random_genome(rng, v3=True):
    parts = [rng.standard_normal(GENOME_LEN) * 0.5, rng.standard_normal(N_BODY)]
    if v3:
        parts.append(rng.standard_normal(N_PHYS) * 1.5)
    return np.concatenate(parts)


def instrument_params(genome, pitch_hz, interaction=True, wander=0.0):
    """wander: migration speed limit in octaves per second; 0 = partials stay where they are born."""
    g = np.asarray(genome, float)
    p = fast_params()
    p.update(dict(pitch_hz=float(pitch_hz), n_init=6, a_init=0.04, init_spread=0.02, x_max=8.3, sr=44100,
                  genome=g[:GENOME_LEN], body_genes=g[GENOME_LEN:V2_LEN], births=True, phys=physics(g),
                  pull_clip_hz=4.0, shared_genome=True, evolve=False,
                  migrate=wander > 0, v_max=max(float(wander), 1e-9)))
    if not interaction:
        p.update(coupling=False, births=False)
    return p


def play(genome, pitch_hz, seed, interaction=True, render=True, trace_every=10, wander=0.0):
    eco = Ecology(seed=seed, **instrument_params(genome, pitch_hz, interaction, wander))
    steps = int(round(NOTE_S / eco.dt))
    audio, trace = [], []
    for st in range(steps):
        y = eco.step(render=render)
        if render:
            audio.append(y)
        if st % trace_every == 0:
            trace.append((st * eco.dt, eco.f_eff.copy(), eco.a.copy()))
    return eco, (np.concatenate(audio) if render else None), trace
