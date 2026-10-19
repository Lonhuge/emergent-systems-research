"""
Order parameters and emergence proxies (see docs/01 §4.2).

Everything here is computed from a World snapshot. Nothing feeds back into
the simulation. The emergence verdict itself is made in analyze.py by comparing
conditions, never inside a single run.
"""
from __future__ import annotations

import numpy as np


def _mi_bits(a, b, bins=4):
    """Mutual information in bits between two 1-D arrays, fixed-width bins on [0,1]."""
    if a.size < 10:
        return 0.0
    ea = np.clip(np.floor(np.clip(a, 0, 1) * bins).astype(int), 0, bins - 1)
    eb = np.clip(np.floor(np.clip(b, 0, 1) * bins).astype(int), 0, bins - 1)
    joint = np.zeros((bins, bins))
    np.add.at(joint, (ea, eb), 1.0)
    joint /= joint.sum()
    pa = joint.sum(axis=1, keepdims=True)
    pb = joint.sum(axis=0, keepdims=True)
    nz = joint > 0
    return float((joint[nz] * np.log2(joint[nz] / (pa @ pb)[nz])).sum())


def _entropy_bits(x, bins=8):
    if x.size == 0:
        return 0.0
    h, _ = np.histogram(np.clip(x, 0, 1), bins=bins, range=(0, 1))
    p = h / h.sum()
    p = p[p > 0]
    return float(-(p * np.log2(p)).sum())


def snapshot(w) -> dict:
    n = w.n
    m = {"t": int(w.t), "n": int(n), "births": int(w.births), "deaths": int(w.deaths)}
    if n == 0:
        return m
    p = w.p
    L = w.L
    m["energy_mean"] = float(w.e.mean())
    m["age_mean"] = float(w.age.mean())
    m["resource_mean"] = float(w.R.mean())

    # --- behaviour
    if w.last_outputs is not None and w.last_outputs.shape[0] == n:
        turn, speed, sig = w.last_outputs.T
        m["speed_mean"] = float(speed.mean())
        m["speed_std"] = float(speed.std())
        m["turn_abs_mean"] = float(np.abs(turn).mean())
    m["signal_mean"] = float(w.sig.mean())
    m["signal_std"] = float(w.sig.std())
    m["signal_entropy_bits"] = _entropy_bits(w.sig)

    # --- spatial order
    # global polarisation of headings
    m["polarisation_global"] = float(np.abs(np.exp(1j * w.th).mean()))
    nbr = w.last_nbr
    if nbr is not None and nbr.shape[0] == n and n > 1:
        deg = nbr.sum(axis=1)
        has = deg > 0
        m["neighbours_mean"] = float(deg.mean())
        m["isolated_frac"] = float((~has).mean())
        if has.any():
            z = np.exp(1j * w.th)
            local = np.abs((nbr[has] @ z) / deg[has])
            m["polarisation_local"] = float(local.mean())
            # Moran's I of the signal over the neighbour graph
            s = w.sig - w.sig.mean()
            denom = float((s * s).sum())
            W = float(nbr.sum())
            if denom > 1e-12 and W > 0:
                m["signal_morans_I"] = float((n / W) * (s @ (nbr @ s)) / denom)
            # MI between own signal and mean neighbour signal
            nb_mean = np.where(has, (nbr @ w.sig) / np.maximum(deg, 1), np.nan)
            ok = ~np.isnan(nb_mean)
            m["mi_signal_neighbour_signal_bits"] = _mi_bits(w.sig[ok], nb_mean[ok])
        else:
            m["polarisation_local"] = 0.0
    # Clark-Evans aggregation index: <1 clustered, 1 random, >1 dispersed
    if n > 2:
        dx = (w.x[None, :] - w.x[:, None] + L / 2) % L - L / 2
        dy = (w.y[None, :] - w.y[:, None] + L / 2) % L - L / 2
        d = np.sqrt(dx * dx + dy * dy)
        np.fill_diagonal(d, np.inf)
        nn = d.min(axis=1)
        expected = 0.5 / np.sqrt(n / (L * L))
        m["clark_evans"] = float(nn.mean() / expected)

    # --- agents vs resources
    ix, iy = w._cell(w.x, w.y)
    occ = np.zeros(w.grid * w.grid)
    np.add.at(occ, ix * w.grid + iy, 1.0)
    R = w.R.reshape(-1)
    cap = w.cap.reshape(-1)
    if occ.std() > 0 and R.std() > 0:
        m["corr_density_resource"] = float(np.corrcoef(occ, R)[0, 1])
    if occ.std() > 0 and cap.std() > 0:
        m["corr_density_capacity"] = float(np.corrcoef(occ, cap)[0, 1])
    m["mi_signal_resource_bits"] = _mi_bits(w.sig, np.clip(w.R[ix, iy] / max(p["cap_mean"] * 2, 1e-9), 0, 1))
    m["mi_signal_energy_bits"] = _mi_bits(w.sig, np.clip(w.e / (2 * p["e_repro"]), 0, 1))

    # --- genetic structure
    lin, counts = np.unique(w.lineage, return_counts=True)
    pl = counts / counts.sum()
    m["lineages_alive"] = int(lin.size)
    m["lineages_effective"] = float(np.exp(-(pl * np.log(pl)).sum()))
    k = min(n, 80)
    idx = w.rng.choice(n, size=k, replace=False) if n > k else np.arange(n)
    g = w.genome[idx]
    dd = np.sqrt(((g[:, None, :] - g[None, :, :]) ** 2).sum(-1))
    m["genome_dist_mean"] = float(dd[np.triu_indices(k, 1)].mean()) if k > 1 else 0.0
    return m


def density_map(w, size=32):
    """Coarse agent-count map for ASCII rendering."""
    s = size / w.L
    ix = np.floor(w.x * s).astype(int) % size
    iy = np.floor(w.y * s).astype(int) % size
    occ = np.zeros((size, size))
    np.add.at(occ, (ix, iy), 1.0)
    return occ
