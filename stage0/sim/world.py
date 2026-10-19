"""
Open artificial-life substrate.

Design constraints (see ../PRINCIPLES.md):
- No macro behaviour is specified. There is no fitness function, no reward,
  no flocking rule, no communication protocol. Agents have a tiny randomly
  initialised controller, local senses, one scalar signal channel, an energy
  budget, and reproduction with mutation. Everything else is left to the
  dynamics.
- No code is generated or executed. Genomes are weight vectors only.
- The only file I/O happens in run_experiment.py, into results/.

Agent controller: 14 inputs -> 8 tanh hidden -> 3 outputs (turn, speed, signal).

Inputs
  0-3   neighbour density in four body-relative sectors (FL, FR, BL, BR), squashed
  4-7   mean neighbour signal in the same four sectors (0 if empty)
  8     resource at own cell
  9     resource gradient ahead (forward cell minus own cell)
  10    resource gradient to the left
  11    own energy, squashed
  12    own signal from the previous step
  13    bias (1.0)

Conditions
  social=False        inputs 0-7 are forced to zero: agents cannot perceive
                      each other at all. Indirect interaction through shared
                      resources remains (this is the no-social-interaction baseline).
  shuffle_signal=True signals are permuted across agents before neighbours read
                      them: same statistics, no information.
  evolve=False        offspring are exact copies: no mutation, no adaptation.
"""
from __future__ import annotations

import numpy as np

N_IN, N_HID, N_OUT = 14, 8, 3
GENOME_LEN = N_IN * N_HID + N_HID + N_HID * N_OUT + N_OUT

DEFAULTS = dict(
    L=64.0,            # world side length (torus)
    grid=64,           # resource grid resolution
    n_init=150,
    n_max=400,         # hard cap: reproduction blocked at cap (documented design intrusion)
    sense_radius=4.0,
    max_turn=0.6,
    max_speed=0.8,
    e_init=4.0,
    e_repro=8.0,
    e_child_frac=0.5,
    max_age=1500,
    cost_base=0.02,
    cost_speed=0.03,
    cost_signal=0.01,
    eat_rate=0.25,
    eat_eff=1.0,
    regrow=0.02,
    cap_mean=1.0,
    patchiness=0.6,    # 0 = uniform resource capacity, 1 = maximally patchy
    patch_scale=8.0,   # spatial scale of patches in grid cells
    mut_sigma=0.08,
    mut_big_p=0.02,
    mut_big_sigma=0.5,
    social=True,
    shuffle_signal=False,
    evolve=True,
)


def _sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def make_capacity_map(rng, grid, patchiness, patch_scale, cap_mean):
    """Smooth random field in [cap_mean*(1-p), cap_mean*(1+p)] with mean cap_mean."""
    noise = rng.standard_normal((grid, grid))
    fx = np.fft.fftfreq(grid)[:, None]
    fy = np.fft.fftfreq(grid)[None, :]
    k2 = fx ** 2 + fy ** 2
    kernel = np.exp(-0.5 * k2 * (2 * np.pi * patch_scale) ** 2)
    field = np.real(np.fft.ifft2(np.fft.fft2(noise) * kernel))
    field = (field - field.min()) / (field.max() - field.min() + 1e-12)  # [0,1]
    field = field - field.mean() + 0.5
    cap = cap_mean * (1.0 + patchiness * (2.0 * field - 1.0))
    return np.clip(cap, 0.0, None)


class World:
    def __init__(self, seed: int, **overrides):
        self.p = dict(DEFAULTS)
        self.p.update(overrides)
        p = self.p
        self.rng = np.random.default_rng(seed)
        self.t = 0
        self.L = float(p["L"])
        self.grid = int(p["grid"])
        self.cap = make_capacity_map(self.rng, self.grid, p["patchiness"], p["patch_scale"], p["cap_mean"])
        self.R = self.cap.copy() * 0.5

        n = int(p["n_init"])
        self.x = self.rng.uniform(0, self.L, n)
        self.y = self.rng.uniform(0, self.L, n)
        self.th = self.rng.uniform(-np.pi, np.pi, n)
        self.e = np.full(n, float(p["e_init"]))
        self.age = np.zeros(n, dtype=np.int64)
        self.sig = np.zeros(n)
        self.lineage = np.arange(n, dtype=np.int64)
        self.genome = self.rng.standard_normal((n, GENOME_LEN)) * 0.5
        self.next_id = n
        # per-step bookkeeping for metrics
        self.births = 0
        self.deaths = 0
        self.last_inputs = None
        self.last_outputs = None
        self.last_nbr = None  # boolean neighbour matrix from the last step

    # ------------------------------------------------------------------ helpers
    @property
    def n(self):
        return self.x.shape[0]

    def _unpack(self):
        g = self.genome
        i = 0
        W1 = g[:, i:i + N_IN * N_HID].reshape(-1, N_HID, N_IN); i += N_IN * N_HID
        b1 = g[:, i:i + N_HID]; i += N_HID
        W2 = g[:, i:i + N_HID * N_OUT].reshape(-1, N_OUT, N_HID); i += N_HID * N_OUT
        b2 = g[:, i:i + N_OUT]
        return W1, b1, W2, b2

    def _cell(self, x, y):
        s = self.grid / self.L
        ix = np.floor(x * s).astype(np.int64) % self.grid
        iy = np.floor(y * s).astype(np.int64) % self.grid
        return ix, iy

    def _wrap_delta(self, d):
        return (d + self.L / 2.0) % self.L - self.L / 2.0

    # ------------------------------------------------------------------ sensing
    def sense(self):
        p = self.p
        n = self.n
        inp = np.zeros((n, N_IN))
        if n == 0:
            self.last_nbr = np.zeros((0, 0), dtype=bool)
            return inp

        # neighbour geometry
        dx = self._wrap_delta(self.x[None, :] - self.x[:, None])
        dy = self._wrap_delta(self.y[None, :] - self.y[:, None])
        d2 = dx * dx + dy * dy
        nbr = d2 < p["sense_radius"] ** 2
        np.fill_diagonal(nbr, False)
        self.last_nbr = nbr

        if p["social"]:
            phi = np.arctan2(dy, dx) - self.th[:, None]
            phi = (phi + np.pi) % (2 * np.pi) - np.pi
            front = np.abs(phi) < np.pi / 2
            left = phi > 0
            sectors = [nbr & front & left, nbr & front & ~left, nbr & ~front & left, nbr & ~front & ~left]
            sig_seen = self.sig
            if p["shuffle_signal"]:
                sig_seen = self.rng.permutation(self.sig)
            for k, m in enumerate(sectors):
                cnt = m.sum(axis=1)
                inp[:, k] = np.tanh(cnt / 3.0)
                ssum = m @ sig_seen
                inp[:, 4 + k] = np.where(cnt > 0, ssum / np.maximum(cnt, 1), 0.0)

        # resources
        ix, iy = self._cell(self.x, self.y)
        r0 = self.R[ix, iy]
        cell = self.L / self.grid
        fx, fy = self._cell(self.x + cell * np.cos(self.th), self.y + cell * np.sin(self.th))
        lx, ly = self._cell(self.x + cell * np.cos(self.th + np.pi / 2), self.y + cell * np.sin(self.th + np.pi / 2))
        inp[:, 8] = r0
        inp[:, 9] = self.R[fx, fy] - r0
        inp[:, 10] = self.R[lx, ly] - r0
        inp[:, 11] = np.tanh(self.e / p["e_repro"])
        inp[:, 12] = self.sig
        inp[:, 13] = 1.0
        return inp

    # ------------------------------------------------------------------ control
    def act(self, inp):
        W1, b1, W2, b2 = self._unpack()
        h = np.tanh(np.einsum("nhi,ni->nh", W1, inp) + b1)
        out = np.einsum("noh,nh->no", W2, h) + b2
        turn = self.p["max_turn"] * np.tanh(out[:, 0])
        speed = self.p["max_speed"] * _sigmoid(out[:, 1])
        sig = _sigmoid(out[:, 2])
        return turn, speed, sig

    # ------------------------------------------------------------------ step
    def step(self):
        p = self.p
        self.births = 0
        self.deaths = 0
        if self.n == 0:
            self.R += p["regrow"] * (self.cap - self.R)
            self.t += 1
            return

        inp = self.sense()
        turn, speed, sig = self.act(inp)
        self.last_inputs = inp
        self.last_outputs = np.stack([turn, speed, sig], axis=1)

        # move
        self.th = (self.th + turn + np.pi) % (2 * np.pi) - np.pi
        self.x = (self.x + speed * np.cos(self.th)) % self.L
        self.y = (self.y + speed * np.sin(self.th)) % self.L
        self.sig = sig

        # metabolism
        self.e -= p["cost_base"] + p["cost_speed"] * speed ** 2 + p["cost_signal"] * sig

        # eating with local competition: a cell's resource is shared by its occupants
        ix, iy = self._cell(self.x, self.y)
        flat = ix * self.grid + iy
        occ = np.bincount(flat, minlength=self.grid * self.grid)
        avail = self.R.reshape(-1)[flat] / occ[flat]
        take = np.minimum(p["eat_rate"], avail)
        taken = np.bincount(flat, weights=take, minlength=self.grid * self.grid)
        self.R = np.clip(self.R.reshape(-1) - taken, 0.0, None).reshape(self.grid, self.grid)
        self.e += take * p["eat_eff"]

        # ageing and death
        self.age += 1
        dead = (self.e <= 0) | (self.age > p["max_age"])
        self.deaths = int(dead.sum())
        if self.deaths:
            self._keep(~dead)

        # reproduction
        if self.n > 0:
            can = self.e > p["e_repro"]
            room = int(p["n_max"]) - self.n
            idx = np.flatnonzero(can)
            if idx.size > room:
                idx = self.rng.choice(idx, size=max(room, 0), replace=False)
            if idx.size:
                self._reproduce(idx)

        # regrowth
        self.R += p["regrow"] * (self.cap - self.R)
        self.t += 1

    def _keep(self, mask):
        self.x, self.y, self.th = self.x[mask], self.y[mask], self.th[mask]
        self.e, self.age, self.sig = self.e[mask], self.age[mask], self.sig[mask]
        self.lineage, self.genome = self.lineage[mask], self.genome[mask]
        if self.last_inputs is not None:
            self.last_inputs = self.last_inputs[mask]
            self.last_outputs = self.last_outputs[mask]
        if self.last_nbr is not None and self.last_nbr.shape[0] == mask.shape[0]:
            self.last_nbr = self.last_nbr[mask][:, mask]

    def _reproduce(self, idx):
        p = self.p
        k = idx.size
        frac = p["e_child_frac"]
        child_e = self.e[idx] * frac
        self.e[idx] *= (1.0 - frac)
        g = self.genome[idx].copy()
        if p["evolve"]:
            g += self.rng.standard_normal(g.shape) * p["mut_sigma"]
            big = self.rng.random(g.shape) < p["mut_big_p"]
            g += big * self.rng.standard_normal(g.shape) * p["mut_big_sigma"]
        jitter = self.rng.standard_normal((2, k)) * 0.5
        self.x = np.concatenate([self.x, (self.x[idx] + jitter[0]) % self.L])
        self.y = np.concatenate([self.y, (self.y[idx] + jitter[1]) % self.L])
        self.th = np.concatenate([self.th, self.rng.uniform(-np.pi, np.pi, k)])
        self.e = np.concatenate([self.e, child_e])
        self.age = np.concatenate([self.age, np.zeros(k, dtype=np.int64)])
        self.sig = np.concatenate([self.sig, np.zeros(k)])
        self.lineage = np.concatenate([self.lineage, self.lineage[idx]])
        self.genome = np.concatenate([self.genome, g])
        self.births = int(k)
        # metrics arrays from this step refer to pre-birth agents; pad them
        if self.last_inputs is not None:
            self.last_inputs = np.concatenate([self.last_inputs, np.zeros((k, N_IN))])
            self.last_outputs = np.concatenate([self.last_outputs, np.zeros((k, N_OUT))])
        if self.last_nbr is not None:
            n_old = self.last_nbr.shape[0]
            nb = np.zeros((n_old + k, n_old + k), dtype=bool)
            nb[:n_old, :n_old] = self.last_nbr
            self.last_nbr = nb
