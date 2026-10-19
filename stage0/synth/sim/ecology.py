"""
Partial ecology.

Each agent is one sine partial with base frequency f, amplitude a and phase Phi.
Agents live on a log-frequency axis x (octaves above f_ref). The sound is the
sum of all partials.

What is given (physics layer, the same in every condition):
- A sustained exciter (think breath or bow) that supplies linear gain with a
  spectral tilt S(x).
- A random, smooth "body" loss landscape alpha(x), different per seed.
- Cubic saturation shared by all partials (energy competition), stronger
  between partials closer than ~1/3 semitone (they share the same drive region).
- A hard exciter power budget P_max: if linear drive plus the positive part of
  the triad drive would inject more power than P_max, all drive is scaled down
  so that exactly P_max is injected (a player has only so much breath or bow).
- The exciter has a band-pass characteristic (low roll-off, high tilt).
- A generic quadratic nonlinearity of the exciter. Averaged over fast time, a
  quadratic nonlinearity couples only near-resonant triads f_j + f_k ~ f_m
  (j == k allowed: second-harmonic generation). The coupling exchanges energy
  (cos psi) and pulls phases (sin psi, Adler-type), psi = Phi_j + Phi_k - Phi_m.
- Multiplicative noise in the drive.

What is NOT given anywhere:
- no fundamental frequency, no integer ratios, no harmonic series,
- no target spectrum, no reward, no fitness function, no instrument template.

What the agents decide (tiny heritable neural controller, 8-6-3):
- drift velocity on the log-frequency axis (migration),
- coupling openness c in [0, 1] (how strongly it engages the nonlinearity),
- split propensity (threshold modifier for splitting into two partials).
Splitting conserves energy and mutates the controller. A partial dies when its
amplitude falls below a_min. That is the whole ecology.

Senses (local only)
  0 log amplitude relative to the split threshold
  1 own net growth rate in the last step
  2 local body net gain g*S(x) - alpha(x)
  3 gradient of body net gain along x
  4 crowding: other partials within +-0.05 octave
  5 triad support magnitude |z| / a
  6 triad support alignment Re(z) / |z|
  7 bias

Conditions
  coupling=False       quadratic coupling switched off (q = kappa = 0)
  shuffle_phase=True   coupling sees phases of randomly permuted partials: same
                       magnitudes, no phase information
  migrate=False        agents cannot move in frequency (only split jitter)
  evolve=False         controllers are copied exactly at a split
"""
from __future__ import annotations

import numpy as np

N_IN, N_HID, N_OUT = 8, 6, 3
GENOME_LEN = N_IN * N_HID + N_HID + N_HID * N_OUT + N_OUT
TWO_PI = 2.0 * np.pi

DEFAULTS = dict(
    dt=0.002,              # control step in seconds
    sr=32000,              # audio sample rate for rendering
    f_ref=55.0,            # x = 0 corresponds to 55 Hz
    x_min=0.0, x_max=6.0,  # 55 Hz .. 3520 Hz
    n_init=24,
    n_max=160,             # hard safety cap, never reached in calibration (max 107)
    g=1.8,                 # exciter linear gain per second
    exciter_tilt=0.35,     # S(x) = exp(-tilt * x) * (1 - exp(-x / exciter_low))
    exciter_low=0.4,       # low-frequency roll-off of the exciter, octaves
    P_max=1.0,             # exciter power budget per second (energy units a^2 / s), all drive sources together
    alpha_mean=0.8,        # body loss per second
    alpha_var=0.5,
    body_scale=0.35,       # smoothness of the body landscape in octaves
    h=1.0,                 # cubic saturation
    beta=0.15,             # global cross-saturation weight
    beta_near=2.0,         # extra competition between partials closer than ~near_width
    near_width=0.03,       # octaves (~36 cents)
    q=2.0,                 # quadratic coupling, amplitude channel
    kappa=30.0,            # quadratic coupling, phase channel
    w_hz=4.0,              # resonance window of the averaged nonlinearity
    v_max=0.5,             # octaves per second
    cost_move=0.3,         # loss per second at full speed
    cost_open=0.05,        # loss per second at full openness
    noise=0.3,             # multiplicative drive noise per sqrt(second)
    a_init=0.05,
    a_min=0.02,            # below this a partial is gone (about -25 dB under a typical partial)
    a_floor=0.02,          # floor in phase-coupling ratios
    a_split=0.35,
    split_detune=0.012,    # octaves, sd of child offset (~14 cents)
    mut_sigma=0.08,
    mut_big_p=0.02,
    mut_big_sigma=0.5,
    triad_refresh=10,
    coupling=True,
    shuffle_phase=False,
    migrate=True,
    evolve=True,
)


def _sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


def make_body(rng, n_grid, x_min, x_max, scale, alpha_mean, alpha_var):
    xs = np.linspace(x_min, x_max, n_grid)
    noise = rng.standard_normal(n_grid)
    k = np.fft.rfftfreq(n_grid, d=(x_max - x_min) / (n_grid - 1))
    kern = np.exp(-0.5 * (TWO_PI * k * scale) ** 2)
    field = np.fft.irfft(np.fft.rfft(noise) * kern, n=n_grid)
    field = (field - field.min()) / (field.max() - field.min() + 1e-12)
    alpha = alpha_mean + alpha_var * (2.0 * field - 1.0)
    return xs, np.clip(alpha, 0.05, None)


class Ecology:
    def __init__(self, seed: int, **overrides):
        p = dict(DEFAULTS)
        p.update(overrides)
        self.p = p
        self.rng = np.random.default_rng(seed)
        self.t = 0
        self.dt = float(p["dt"])
        self.body_x, self.body_alpha = make_body(
            self.rng, 1200, p["x_min"], p["x_max"], p["body_scale"], p["alpha_mean"], p["alpha_var"])
        n = int(p["n_init"])
        self.x = self.rng.uniform(1.0, 4.0, n)          # inharmonic random start, 110-880 Hz
        self.a = np.full(n, float(p["a_init"])) * self.rng.uniform(0.5, 1.5, n)
        self.Phi = self.rng.uniform(0, TWO_PI, n)
        self.genome = self.rng.standard_normal((n, GENOME_LEN)) * 0.5
        self.lineage = np.arange(n, dtype=np.int64)
        self.gen = np.zeros(n, dtype=np.int64)     # bookkeeping only, never read by the dynamics
        self.growth = np.zeros(n)
        self.f_eff = self.freq()
        self.c = np.full(n, 0.5)
        self.v = np.zeros(n)
        self._triads = None
        self._triads_dirty = True
        self.births = 0
        self.deaths = 0
        self.last_psi = np.zeros(0)
        self.last_triad_w = np.zeros(0)
        self.last_triad_prod = np.zeros(0)

    # ------------------------------------------------------------ helpers
    @property
    def n(self):
        return self.x.shape[0]

    def freq(self, x=None):
        x = self.x if x is None else x
        return self.p["f_ref"] * np.power(2.0, x)

    def exciter(self, x):
        p = self.p
        return p["g"] * np.exp(-p["exciter_tilt"] * x) * (1.0 - np.exp(-x / p["exciter_low"]))

    def body_net_gain(self, x, comp=1.0):
        alpha = np.interp(x, self.body_x, self.body_alpha)
        return comp * self.exciter(x) - alpha

    def _unpack(self):
        g = self.genome
        i = 0
        W1 = g[:, i:i + N_IN * N_HID].reshape(-1, N_HID, N_IN); i += N_IN * N_HID
        b1 = g[:, i:i + N_HID]; i += N_HID
        W2 = g[:, i:i + N_HID * N_OUT].reshape(-1, N_OUT, N_HID); i += N_HID * N_OUT
        b2 = g[:, i:i + N_OUT]
        return W1, b1, W2, b2

    # ------------------------------------------------------------ triads
    def _find_triads(self):
        """Near-resonant triads f_j + f_k ~ f_m with j <= k, any m != j,k."""
        n = self.n
        if n < 2:
            self._triads = (np.zeros(0, int),) * 3 + (np.zeros(0),)
            return
        f = self.freq()
        w = self.p["w_hz"]
        jj, kk = np.triu_indices(n, 0)
        s = f[jj] + f[kk]
        d = s[:, None] - f[None, :]                    # pairs x targets
        hit = np.abs(d) < 3.0 * w
        pi, mm = np.nonzero(hit)
        J, K, M = jj[pi], kk[pi], mm
        ok = (M != J) & (M != K)
        J, K, M = J[ok], K[ok], M[ok]
        dd = d[pi[ok], M]
        weight = np.exp(-(dd / w) ** 2)
        weight = np.where(J == K, 0.5 * weight, weight)  # degenerate triad factor
        self._triads = (J, K, M, weight)

    def _coupling(self, Phi_seen):
        """Return amplitude drive dA, phase rate dtheta, support z per agent."""
        n = self.n
        dA = np.zeros(n)
        dth = np.zeros(n)
        z = np.zeros(n, dtype=complex)
        J, K, M, W = self._triads
        if J.size == 0:
            self.last_psi = np.zeros(0)
            self.last_triad_w = np.zeros(0)
            self.last_triad_prod = np.zeros(0)
            return dA, dth, z
        a = self.a
        af = np.maximum(a, self.p["a_floor"])
        psi = Phi_seen[J] + Phi_seen[K] - Phi_seen[M]
        cps, sps = np.cos(psi), np.sin(psi)
        e = np.exp(1j * psi)
        aj, ak, am = a[J], a[K], a[M]
        # true-phase psi for metrics, regardless of condition
        psi_true = self.Phi[J] + self.Phi[K] - self.Phi[M]
        self.last_psi = psi_true
        self.last_triad_w = W
        self.last_triad_prod = aj * ak * am
        q, kap = self.p["q"], self.p["kappa"]
        if self.p["coupling"]:
            np.add.at(dA, M, q * W * aj * ak * cps)
            np.add.at(dA, J, q * W * ak * am * cps)
            np.add.at(dA, K, q * W * aj * am * cps)
            np.add.at(dth, M, kap * W * np.minimum(aj * ak / af[M], 3.0) * sps)
            np.add.at(dth, J, -kap * W * np.minimum(ak * am / af[J], 3.0) * sps)
            np.add.at(dth, K, -kap * W * np.minimum(aj * am / af[K], 3.0) * sps)
        # support is a local sense that exists in every condition
        np.add.at(z, M, W * aj * ak * e)
        np.add.at(z, J, W * ak * am * e)
        np.add.at(z, K, W * aj * am * e)
        return dA, dth, z

    # ------------------------------------------------------------ step
    def step(self, render=False):
        p = self.p
        dt = self.dt
        self.births = 0
        self.deaths = 0
        out_audio = None
        n = self.n
        if n == 0:
            self.t += 1
            if render:
                out_audio = np.zeros(int(round(dt * p["sr"])))
            return out_audio

        if self._triads_dirty or self.t % int(p["triad_refresh"]) == 0:
            self._find_triads()
            self._triads_dirty = False

        Phi_seen = self.Phi
        if p["shuffle_phase"]:
            Phi_seen = self.Phi[self.rng.permutation(n)]
        dA, dth, z = self._coupling(Phi_seen)

        # --- senses
        a = self.a
        af = np.maximum(a, p["a_floor"])
        a2 = a * a
        exc = self.exciter(self.x)
        c_prev = self.c if self.c.shape[0] == n else np.full(n, 0.5)
        power = (exc * a2).sum() + (a * c_prev * np.maximum(dA, 0.0)).sum()
        comp = min(1.0, p["P_max"] / power) if power > 0 else 1.0
        net = self.body_net_gain(self.x, comp)
        grad = (self.body_net_gain(np.clip(self.x + 0.02, p["x_min"], p["x_max"]), comp) -
                self.body_net_gain(np.clip(self.x - 0.02, p["x_min"], p["x_max"]), comp)) / 0.04
        dx = np.abs(self.x[:, None] - self.x[None, :])
        crowd = (dx < 0.05).sum(axis=1) - 1
        zabs = np.abs(z)
        inp = np.empty((n, N_IN))
        inp[:, 0] = np.clip((np.log(af) - np.log(p["a_split"])) / 2.0, -3, 3)
        inp[:, 1] = np.tanh(self.growth)
        inp[:, 2] = np.tanh(net)
        inp[:, 3] = np.tanh(0.5 * grad)
        inp[:, 4] = np.tanh(crowd / 2.0)
        inp[:, 5] = np.tanh(zabs / af)
        inp[:, 6] = np.where(zabs > 1e-12, np.real(z) / np.maximum(zabs, 1e-12), 0.0)
        inp[:, 7] = 1.0

        # --- controller
        W1, b1, W2, b2 = self._unpack()
        hdn = np.tanh(np.einsum("nhi,ni->nh", W1, inp) + b1)
        out = np.einsum("noh,nh->no", W2, hdn) + b2
        v = p["v_max"] * np.tanh(out[:, 0]) if p["migrate"] else np.zeros(n)
        c = _sigmoid(out[:, 1])
        split_mod = np.tanh(out[:, 2])
        self.v, self.c = v, c

        # --- amplitude dynamics
        near = np.exp(-(dx / p["near_width"]) ** 2)
        np.fill_diagonal(near, 0.0)
        sat = p["h"] * (a2 + p["beta"] * (a2.sum() - a2) + p["beta_near"] * (near @ a2))
        rate = net - sat - p["cost_move"] * (v / p["v_max"]) ** 2 - p["cost_open"] * c
        noise = p["noise"] * np.sqrt(dt) * self.rng.standard_normal(n)
        a_new = a + dt * (a * rate + comp * c * dA) + a * noise
        a_new = np.clip(a_new, 0.0, 4.0)

        # --- phase dynamics
        theta_rate = c * dth
        f = self.freq()
        f_eff = f + theta_rate / TWO_PI
        if render:
            ns = int(round(dt * p["sr"]))
            tt = np.arange(ns) / p["sr"]
            frac = (np.arange(ns) / ns)[None, :]
            amp = a[:, None] * (1 - frac) + a_new[:, None] * frac
            ph = self.Phi[:, None] + TWO_PI * f_eff[:, None] * tt[None, :]
            out_audio = (amp * np.cos(ph)).sum(axis=0)
        self.Phi = (self.Phi + TWO_PI * f_eff * dt) % TWO_PI
        self.f_eff = f_eff
        self.growth = (a_new - a) / (af * dt)
        self.a = a_new

        # --- migration
        if p["migrate"]:
            self.x = np.clip(self.x + v * dt, p["x_min"], p["x_max"])

        # --- death
        dead = self.a < p["a_min"]
        if dead.any():
            self.deaths = int(dead.sum())
            self._keep(~dead)

        # --- splitting
        if self.n:
            thr = p["a_split"] * np.exp(0.5 * split_mod[~dead] if dead.any() else 0.5 * split_mod)
            idx = np.flatnonzero(self.a > thr)
            room = int(p["n_max"]) - self.n
            if idx.size > room:
                idx = self.rng.choice(idx, size=max(room, 0), replace=False)
            if idx.size:
                self._split(idx)
        self.t += 1
        return out_audio

    def _keep(self, m):
        self.x, self.a, self.Phi = self.x[m], self.a[m], self.Phi[m]
        self.genome, self.lineage, self.gen = self.genome[m], self.lineage[m], self.gen[m]
        self.growth, self.f_eff = self.growth[m], self.f_eff[m]
        self.c, self.v = self.c[m], self.v[m]
        self._triads_dirty = True

    def _split(self, idx):
        p = self.p
        k = idx.size
        self.a[idx] = self.a[idx] / np.sqrt(2.0)
        child_a = self.a[idx].copy()
        child_x = np.clip(self.x[idx] + self.rng.standard_normal(k) * p["split_detune"], p["x_min"], p["x_max"])
        g = self.genome[idx].copy()
        if p["evolve"]:
            g += self.rng.standard_normal(g.shape) * p["mut_sigma"]
            big = self.rng.random(g.shape) < p["mut_big_p"]
            g += big * self.rng.standard_normal(g.shape) * p["mut_big_sigma"]
        self.x = np.concatenate([self.x, child_x])
        self.a = np.concatenate([self.a, child_a])
        self.Phi = np.concatenate([self.Phi, self.Phi[idx]])
        self.genome = np.concatenate([self.genome, g])
        self.lineage = np.concatenate([self.lineage, self.lineage[idx]])
        self.gen[idx] += 1
        self.gen = np.concatenate([self.gen, self.gen[idx]])
        self.growth = np.concatenate([self.growth, np.zeros(k)])
        self.f_eff = np.concatenate([self.f_eff, self.freq(child_x)])
        self.c = np.concatenate([self.c, self.c[idx]])
        self.v = np.concatenate([self.v, np.zeros(k)])
        self.births = int(k)
        self._triads_dirty = True
