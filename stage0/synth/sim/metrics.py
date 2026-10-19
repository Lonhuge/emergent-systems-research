"""
Order parameters for the partial ecology. Read-only: nothing feeds back.

Harmonicity and triad closure are always reported as EXCESS over a null model:
the same number of partials with the same amplitudes, frequencies drawn
log-uniformly over the observed frequency range. This removes the trivial
effect that low candidate fundamentals make any set look harmonic.
"""
from __future__ import annotations

import numpy as np

SIGMA_CENTS = 15.0
K_MAX = 32
N_NULL = 24


def _cents(r):
    return 1200.0 * np.log2(r)


def harmonic_score(f, w):
    """Best energy-weighted fit of f to the harmonic series of some f0.

    Candidates: the lowest strong partial divided by 1..4, each on a +-40 cent grid.
    Returns a score in [0, 1].
    """
    if f.size < 3 or w.sum() <= 0:
        return np.nan
    strong = w >= 0.05 * w.max()
    f_low = f[strong].min()
    cands = []
    for div in (1, 2, 3, 4):
        base = f_low / div
        cands.append(base * np.power(2.0, np.linspace(-40, 40, 17) / 1200.0))
    f0 = np.concatenate(cands)                                  # C
    k = np.clip(np.round(f[None, :] / f0[:, None]), 1, None)    # C x N
    dev = _cents(f[None, :] / (k * f0[:, None]))
    match = np.exp(-(dev / SIGMA_CENTS) ** 2) * (k <= K_MAX)
    scores = (match * w[None, :]).sum(axis=1) / w.sum()
    return float(scores.max())


def triad_closure(f, w):
    """Weighted fraction of pairs (j<=k) whose sum frequency hits an existing partial."""
    n = f.size
    if n < 3:
        return np.nan
    jj, kk = np.triu_indices(n, 0)
    s = f[jj] + f[kk]
    inside = s <= f.max() * 1.03
    if not inside.any():
        return np.nan
    jj, kk, s = jj[inside], kk[inside], s[inside]
    dev = np.min(np.abs(_cents(s[:, None] / f[None, :])), axis=1)
    pw = np.sqrt(w[jj] * w[kk])
    return float((pw * np.exp(-(dev / SIGMA_CENTS) ** 2)).sum() / pw.sum())


def _excess(fun, f, w, rng):
    obs = fun(f, w)
    if np.isnan(obs):
        return np.nan, np.nan
    lo, hi = np.log2(f.min()), np.log2(f.max())
    nulls = []
    for _ in range(N_NULL):
        fr = np.power(2.0, rng.uniform(lo, hi, f.size))
        v = fun(fr, w)
        if not np.isnan(v):
            nulls.append(v)
    if not nulls:
        return np.nan, np.nan
    nulls = np.asarray(nulls)
    sd = nulls.std()
    return float(obs - nulls.mean()), float((obs - nulls.mean()) / sd) if sd > 0 else np.nan


def snapshot(eco, rng) -> dict:
    m = {"t_s": round(eco.t * eco.dt, 3), "n": int(eco.n)}
    if eco.n == 0:
        return m
    a = eco.a
    w = a * a
    f = np.maximum(eco.f_eff, 1.0)
    x = np.log2(f / eco.p["f_ref"])
    m["energy"] = float(w.sum())
    m["centroid_hz"] = float((w * f).sum() / w.sum())
    m["centroid_oct"] = float((w * x).sum() / w.sum())
    hist, _ = np.histogram(x, bins=60, range=(eco.p["x_min"], eco.p["x_max"]), weights=w)
    pp = hist / hist.sum()
    pp = pp[pp > 0]
    m["spectral_entropy_bits"] = float(-(pp * np.log2(pp)).sum())
    m["lineages_alive"] = int(np.unique(eco.lineage).size)
    m["openness_mean"] = float(eco.c.mean())
    m["speed_abs_mean"] = float(np.abs(eco.v).mean())

    he, hz = _excess(harmonic_score, f, w, rng)
    m["harmonicity_excess"], m["harmonicity_z"] = he, hz
    m["harmonicity_raw"] = harmonic_score(f, w)
    te, tz = _excess(triad_closure, f, w, rng)
    m["triad_closure_excess"], m["triad_closure_z"] = te, tz

    # phase locking among near-resonant triads, weighted by resonance x amplitude
    if eco.last_psi.size and eco.last_psi.size == eco.last_triad_w.size:
        ww = eco.last_triad_w * eco.last_triad_prod
        if ww.sum() > 0:
            m["lock_coherence"] = float((ww * np.cos(eco.last_psi)).sum() / ww.sum())
            m["lock_magnitude"] = float(np.abs((ww * np.exp(1j * eco.last_psi)).sum()) / ww.sum())
        m["n_triads"] = int(eco.last_psi.size)

    # does the energy distribution follow the body landscape?
    gain = eco.body_net_gain(np.clip(x, eco.p["x_min"], eco.p["x_max"]))
    if eco.n > 3 and gain.std() > 0 and w.std() > 0:
        m["body_alignment"] = float(np.corrcoef(gain, w)[0, 1])
    return m


def spectrum(eco):
    """Compact list of (f_eff, amplitude) for the final state, sorted by frequency."""
    o = np.argsort(eco.f_eff)
    return [[round(float(eco.f_eff[i]), 3), round(float(eco.a[i]), 5)] for i in o]
