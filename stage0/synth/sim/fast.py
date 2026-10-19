"""
Fast-note parameter set: the frozen phase-1 physics, time-compressed.

All rates of the amplitude, migration and splitting dynamics are multiplied by
K. Phase dynamics (kappa) and the resonance window (w_hz) are unchanged: phase
locking already took about 45 ms. Noise scales with sqrt(K) because it is
specified per sqrt(second). One shared controller per note, no mutation within
a note.
"""
from __future__ import annotations

import math

from .ecology import DEFAULTS

K = 50.0
RATE_KEYS = ["g", "alpha_mean", "alpha_var", "h", "q", "v_max", "cost_move", "cost_open", "P_max"]


def fast_params() -> dict:
    p = {}
    for k in RATE_KEYS:
        p[k] = DEFAULTS[k] * K
    p["noise"] = DEFAULTS["noise"] * math.sqrt(K)
    p["dt"] = 0.001
    p["triad_refresh"] = 2
    p["evolve"] = False
    p["shared_genome"] = True
    return p
