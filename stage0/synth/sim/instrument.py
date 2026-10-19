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

FULL_LEN = GENOME_LEN + N_BODY
NOTE_S = 4.0


def random_genome(rng):
    return np.concatenate([rng.standard_normal(GENOME_LEN) * 0.5, rng.standard_normal(N_BODY)])


def instrument_params(genome, pitch_hz, interaction=True, wander=0.0):
    """wander: migration speed limit in octaves per second; 0 = partials stay where they are born."""
    g = np.asarray(genome, float)
    p = fast_params()
    p.update(dict(pitch_hz=float(pitch_hz), n_init=6, a_init=0.04, init_spread=0.02,
                  genome=g[:GENOME_LEN], body_genes=g[GENOME_LEN:], births=True,
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
