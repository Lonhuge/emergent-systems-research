/* Partial-ecology instrument engine (browser + node).
 * Port of sim/ecology.py with the v2 instrument options of sim/instrument.py:
 * fast notes, body resonance at the pitch, combination-tone births, capped
 * phase pull, one shared controller per note. Pure computation: no network,
 * no storage, no code generation. */
(function (root) {
  "use strict";
  var N_IN = 8, N_HID = 6, N_OUT = 3;
  var GLEN = N_IN * N_HID + N_HID + N_HID * N_OUT + N_OUT; // 75
  var N_BODY = 12, FULL_LEN = GLEN + N_BODY;               // 87
  var TWO_PI = Math.PI * 2, K = 50;
  var P = {
    dt: 0.001, sr: 32000, f_ref: 55, x_min: 0, x_max: 6, n_init: 6, n_max: 160,
    g: 1.8 * K, exciter_tilt: 0.35, exciter_low: 0.4, P_max: 1.0 * K,
    alpha_mean: 0.8 * K, alpha_var: 0.5 * K, h: 1.0 * K, beta: 0.15, beta_near: 2.0,
    near_width: 0.03, q: 2.0 * K, kappa: 30, w_hz: 4, cost_move: 0.3 * K, cost_open: 0.05 * K,
    noise: 0.3 * Math.sqrt(K), a_init: 0.04, a_min: 0.02, a_floor: 0.02, a_split: 0.35,
    split_detune: 0.012, triad_refresh: 2, exciter_sigma: 0.04, resonance_depth: 0.8,
    init_spread: 0.02, birth_every: 5, birth_rate: 400, birth_top: 8, a_seed: 0.03,
    pull_clip_hz: 4, note_s: 4
  };

  function makeRng(seed) {
    var s = seed >>> 0, spare = null;
    function u() { s = (s + 0x6D2B79F5) >>> 0; var t = s; t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }
    function n() { if (spare !== null) { var r = spare; spare = null; return r; }
      var a = u() || 1e-12, b = u(); var m = Math.sqrt(-2 * Math.log(a));
      spare = m * Math.sin(TWO_PI * b); return m * Math.cos(TWO_PI * b); }
    return { u: u, n: n };
  }

  function randomGenome(rng) {
    var g = new Array(FULL_LEN);
    for (var i = 0; i < GLEN; i++) g[i] = rng.n() * 0.5;
    for (var j = GLEN; j < FULL_LEN; j++) g[j] = rng.n();
    return g;
  }

  function play(opts) {
    var genome = opts.genome, pitch = opts.pitch, seed = opts.seed >>> 0;
    var interaction = opts.interaction !== false, wander = +opts.wander || 0;
    var render = opts.render !== false;
    var rng = makeRng(seed);
    var dt = P.dt, migrate = wander > 0, vmax = migrate ? wander : 1e-9;
    var q = interaction ? P.q : 0, kap = interaction ? P.kappa : 0, births = interaction;
    var x0 = Math.log2(pitch / P.f_ref);
    var cap = P.n_max + 16;
    var x = new Float64Array(cap), a = new Float64Array(cap), Phi = new Float64Array(cap);
    var growth = new Float64Array(cap), feff = new Float64Array(cap), c = new Float64Array(cap), v = new Float64Array(cap);
    var n = P.n_init;
    for (var i = 0; i < n; i++) {
      x[i] = Math.min(P.x_max, Math.max(P.x_min, x0 + rng.n() * P.init_spread));
      a[i] = P.a_init * (0.5 + rng.u());
      Phi[i] = rng.u() * TWO_PI; c[i] = 0.5;
      feff[i] = P.f_ref * Math.pow(2, x[i]);
    }
    // controller (shared) and body
    var W1 = genome.slice(0, 48), b1 = genome.slice(48, 54), W2 = genome.slice(54, 72), b2 = genome.slice(72, 75);
    var body = genome.slice(GLEN, FULL_LEN), gstep = (P.x_max - P.x_min) / (N_BODY - 1);
    function alphaAt(xx) {
      var t = (xx - P.x_min) / gstep, i0 = Math.max(0, Math.min(N_BODY - 2, Math.floor(t))), fr = Math.min(1, Math.max(0, t - i0));
      var gv = body[i0] * (1 - fr) + body[i0 + 1] * fr;
      var al = Math.max(P.alpha_mean + P.alpha_var * Math.tanh(gv), 0.05 * P.alpha_mean);
      var d = (xx - x0) / P.exciter_sigma;
      return al - P.resonance_depth * P.alpha_mean * Math.exp(-0.5 * d * d);
    }
    function exciter(xx) { return P.g * Math.exp(-P.exciter_tilt * xx) * (1 - Math.exp(-xx / P.exciter_low)); }
    function netGain(xx, comp) { return comp * exciter(xx) - alphaAt(xx); }
    function freq(xx) { return P.f_ref * Math.pow(2, xx); }

    var steps = Math.round(P.note_s / dt), ns = Math.round(dt * P.sr);
    var audio = render ? new Float32Array(steps * ns) : null;
    var trace = [], energy = [];
    var TJ = [], TK = [], TM = [], TW = [], dirty = true;
    var dA = new Float64Array(cap), dth = new Float64Array(cap), zr = new Float64Array(cap), zi = new Float64Array(cap);
    var aNew = new Float64Array(cap), inp = new Float64Array(N_IN), hdn = new Float64Array(N_HID), smod = new Float64Array(cap);
    var nearA2 = new Float64Array(cap), crowd = new Float64Array(cap), fb = new Float64Array(cap);
    var lockNum = 0, lockDen = 0;

    function findTriads() {
      TJ.length = TK.length = TM.length = TW.length = 0;
      if (n < 2) return;
      for (var i2 = 0; i2 < n; i2++) fb[i2] = freq(x[i2]);
      var w = P.w_hz, lim = 3 * w;
      for (var j = 0; j < n; j++) for (var k = j; k < n; k++) {
        var s = fb[j] + fb[k];
        for (var m = 0; m < n; m++) {
          if (m === j || m === k) continue;
          var d = s - fb[m];
          if (d > -lim && d < lim) { var wt = Math.exp(-(d / w) * (d / w)); if (j === k) wt *= 0.5;
            TJ.push(j); TK.push(k); TM.push(m); TW.push(wt); }
        }
      }
    }
    function keep(mask) {
      var w = 0;
      for (var i3 = 0; i3 < n; i3++) if (mask[i3]) {
        x[w] = x[i3]; a[w] = a[i3]; Phi[w] = Phi[i3]; growth[w] = growth[i3]; feff[w] = feff[i3]; c[w] = c[i3]; v[w] = v[i3]; smod[w] = smod[i3]; w++;
      }
      n = w; dirty = true;
    }
    function addPartial(xx, aa, ph, cc) {
      x[n] = xx; a[n] = aa; Phi[n] = ph; growth[n] = 0; feff[n] = freq(xx); c[n] = cc; v[n] = 0; smod[n] = 0; n++; dirty = true;
    }

    for (var st = 0; st < steps; st++) {
      if (n === 0) { if (render) { /* silence */ } if (st % 10 === 0) { trace.push(st * dt, 0); energy.push(0); } continue; }
      if (dirty || st % P.triad_refresh === 0) { findTriads(); dirty = false; }
      // coupling
      for (var i4 = 0; i4 < n; i4++) { dA[i4] = 0; dth[i4] = 0; zr[i4] = 0; zi[i4] = 0; }
      lockNum = 0; lockDen = 0;
      for (var t = 0; t < TJ.length; t++) {
        var J = TJ[t], Kk = TK[t], M = TM[t], W = TW[t];
        var psi = Phi[J] + Phi[Kk] - Phi[M], cp = Math.cos(psi), sp = Math.sin(psi);
        var aj = a[J], ak = a[Kk], am = a[M];
        var afJ = Math.max(aj, P.a_floor), afK = Math.max(ak, P.a_floor), afM = Math.max(am, P.a_floor);
        if (q) {
          dA[M] += q * W * aj * ak * cp; dA[J] += q * W * ak * am * cp; dA[Kk] += q * W * aj * am * cp;
          dth[M] += kap * W * Math.min(aj * ak / afM, 3) * sp;
          dth[J] -= kap * W * Math.min(ak * am / afJ, 3) * sp;
          dth[Kk] -= kap * W * Math.min(aj * am / afK, 3) * sp;
        }
        zr[M] += W * aj * ak * cp; zi[M] += W * aj * ak * sp;
        zr[J] += W * ak * am * cp; zi[J] += W * ak * am * sp;
        zr[Kk] += W * aj * am * cp; zi[Kk] += W * aj * am * sp;
        var ww = W * aj * ak * am; lockNum += ww * cp; lockDen += ww;
      }
      // power budget
      var a2sum = 0, power = 0;
      for (var i5 = 0; i5 < n; i5++) { var a2 = a[i5] * a[i5]; a2sum += a2; power += exciter(x[i5]) * a2 + a[i5] * c[i5] * Math.max(dA[i5], 0); }
      var comp = power > 0 ? Math.min(1, P.P_max / power) : 1;
      // neighbourhood
      for (var i6 = 0; i6 < n; i6++) {
        var cr = 0, na = 0;
        for (var j6 = 0; j6 < n; j6++) { if (j6 === i6) continue; var ddx = Math.abs(x[i6] - x[j6]);
          if (ddx < 0.05) cr++; var e6 = ddx / P.near_width; na += Math.exp(-e6 * e6) * a[j6] * a[j6]; }
        crowd[i6] = cr; nearA2[i6] = na;
      }
      // controller + amplitude
      for (var i7 = 0; i7 < n; i7++) {
        var ai = a[i7], af = Math.max(ai, P.a_floor), xi = x[i7];
        var net = netGain(xi, comp);
        var gp = netGain(Math.min(P.x_max, xi + 0.02), comp), gm = netGain(Math.max(P.x_min, xi - 0.02), comp);
        var grad = (gp - gm) / 0.04, za = Math.sqrt(zr[i7] * zr[i7] + zi[i7] * zi[i7]);
        inp[0] = Math.max(-3, Math.min(3, (Math.log(af) - Math.log(P.a_split)) / 2));
        inp[1] = Math.tanh(growth[i7]); inp[2] = Math.tanh(net); inp[3] = Math.tanh(0.5 * grad);
        inp[4] = Math.tanh(crowd[i7] / 2); inp[5] = Math.tanh(za / af); inp[6] = za > 1e-12 ? zr[i7] / za : 0; inp[7] = 1;
        for (var h = 0; h < N_HID; h++) { var sum = b1[h]; for (var ii = 0; ii < N_IN; ii++) sum += W1[h * N_IN + ii] * inp[ii]; hdn[h] = Math.tanh(sum); }
        var o0 = b2[0], o1 = b2[1], o2 = b2[2];
        for (var h2 = 0; h2 < N_HID; h2++) { o0 += W2[h2] * hdn[h2]; o1 += W2[N_HID + h2] * hdn[h2]; o2 += W2[2 * N_HID + h2] * hdn[h2]; }
        v[i7] = migrate ? vmax * Math.tanh(o0) : 0;
        c[i7] = 1 / (1 + Math.exp(-o1));
        smod[i7] = Math.tanh(o2);
        var sat = P.h * (ai * ai + P.beta * (a2sum - ai * ai) + P.beta_near * nearA2[i7]);
        var rate = net - sat - P.cost_move * (v[i7] / vmax) * (v[i7] / vmax) - P.cost_open * c[i7];
        var nz = P.noise * Math.sqrt(dt) * rng.n();
        var an = ai + dt * (ai * rate + comp * c[i7] * dA[i7]) + ai * nz;
        aNew[i7] = Math.min(4, Math.max(0, an));
      }
      // phase + audio
      var lim2 = TWO_PI * P.pull_clip_hz;
      for (var i8 = 0; i8 < n; i8++) {
        var tr = c[i8] * dth[i8]; tr = Math.max(-lim2, Math.min(lim2, tr));
        feff[i8] = freq(x[i8]) + tr / TWO_PI;
      }
      if (render) {
        var base = st * ns;
        for (var i9 = 0; i9 < n; i9++) {
          var w0 = TWO_PI * feff[i9] / P.sr, a0 = a[i9], a1 = aNew[i9], ph0 = Phi[i9];
          for (var sIdx = 0; sIdx < ns; sIdx++) { var fr = sIdx / ns; audio[base + sIdx] += (a0 * (1 - fr) + a1 * fr) * Math.cos(ph0 + w0 * sIdx); }
        }
      }
      for (var i10 = 0; i10 < n; i10++) {
        Phi[i10] = (Phi[i10] + TWO_PI * feff[i10] * dt) % TWO_PI;
        growth[i10] = (aNew[i10] - a[i10]) / (Math.max(a[i10], P.a_floor) * dt);
        a[i10] = aNew[i10];
        if (migrate) x[i10] = Math.min(P.x_max, Math.max(P.x_min, x[i10] + v[i10] * dt));
      }
      // death
      var anyDead = false, mask = new Uint8Array(n);
      for (var i11 = 0; i11 < n; i11++) { mask[i11] = a[i11] >= P.a_min ? 1 : 0; if (!mask[i11]) anyDead = true; }
      if (anyDead) keep(mask);
      // split
      if (n) {
        var idx = [];
        for (var i12 = 0; i12 < n; i12++) if (a[i12] > P.a_split * Math.exp(0.5 * smod[i12])) idx.push(i12);
        var room = P.n_max - n;
        while (idx.length > Math.max(room, 0)) idx.splice(Math.floor(rng.u() * idx.length), 1);
        for (var s2 = 0; s2 < idx.length; s2++) {
          var pI = idx[s2]; a[pI] = a[pI] / Math.SQRT2;
          var cx = Math.min(P.x_max, Math.max(P.x_min, x[pI] + rng.n() * P.split_detune));
          addPartial(cx, a[pI], Phi[pI], c[pI]);
        }
      }
      // combination-tone births
      if (births && n >= 1 && st % P.birth_every === 0) {
        var order = []; for (var i13 = 0; i13 < n; i13++) order.push(i13);
        order.sort(function (p1, p2) { return a[p2] - a[p1]; });
        var kTop = Math.min(n, P.birth_top), dtb = dt * P.birth_every, fLo = freq(P.x_min), fHi = freq(P.x_max), nw = [];
        for (var u1 = 0; u1 < kTop; u1++) for (var u2 = u1; u2 < kTop; u2++) {
          var jb = order[u1], mb = order[u2], fj = freq(x[jb]), fm = freq(x[mb]);
          var prob = 1 - Math.exp(-P.birth_rate * a[jb] * a[mb] * dtb);
          var cands = [[fj + fm, Phi[jb] + Phi[mb]]];
          if (jb !== mb) { if (fj >= fm) cands.push([fj - fm, Phi[jb] - Phi[mb]]); else cands.push([fm - fj, Phi[mb] - Phi[jb]]); }
          for (var cI = 0; cI < cands.length; cI++) {
            var F = cands[cI][0]; if (!(F >= fLo && F <= fHi)) continue;
            var xF = Math.log2(F / P.f_ref), clash = false;
            for (var e1 = 0; e1 < n; e1++) if (Math.abs(x[e1] - xF) < P.near_width) { clash = true; break; }
            for (var e2 = 0; e2 < nw.length && !clash; e2++) if (Math.abs(nw[e2][0] - xF) < P.near_width) clash = true;
            if (clash) continue;
            if (rng.u() < prob) nw.push([xF, ((cands[cI][1] % TWO_PI) + TWO_PI) % TWO_PI, jb]);
          }
        }
        var lim3 = Math.max(0, Math.min(P.n_max - n, 4));
        for (var b5 = 0; b5 < Math.min(nw.length, lim3); b5++) addPartial(nw[b5][0], P.a_seed, nw[b5][1], c[nw[b5][2]]);
      }
      if (st % 10 === 0) {
        trace.push(st * dt, n);
        var en = 0;
        for (var i14 = 0; i14 < n; i14++) { trace.push(feff[i14], a[i14]); en += a[i14] * a[i14]; }
        energy.push(en);
      }
    }
    // normalise audio
    if (render) {
      var peak = 0; for (var s3 = 0; s3 < audio.length; s3++) { var av = Math.abs(audio[s3]); if (av > peak) peak = av; }
      if (peak > 0) for (var s4 = 0; s4 < audio.length; s4++) audio[s4] *= 0.9 / peak;
      var fade = Math.floor(0.02 * P.sr);
      for (var s5 = 0; s5 < fade; s5++) { var r = s5 / fade; audio[s5] *= r; audio[audio.length - 1 - s5] *= r; }
    }
    var spec = [];
    for (var i15 = 0; i15 < n; i15++) spec.push([feff[i15], a[i15]]);
    spec.sort(function (p1, p2) { return p1[0] - p2[0]; });
    return { audio: audio, sr: P.sr, trace: trace, energy: energy, spectrum: spec, n: n,
             lock: lockDen > 0 ? lockNum / lockDen : 0, metrics: describe(spec, energy, pitch, seed) };
  }

  // ---------------- descriptors (read-only) ----------------
  function harmonicScore(f, w) {
    if (f.length < 3) return NaN;
    var wmax = 0, wsum = 0; for (var i = 0; i < w.length; i++) { if (w[i] > wmax) wmax = w[i]; wsum += w[i]; }
    if (wsum <= 0) return NaN;
    var flow = Infinity; for (var j = 0; j < f.length; j++) if (w[j] >= 0.05 * wmax && f[j] < flow) flow = f[j];
    var best = 0;
    for (var div = 1; div <= 4; div++) for (var g = 0; g < 17; g++) {
      var f0 = flow / div * Math.pow(2, (-40 + 5 * g) / 1200), sc = 0;
      for (var k = 0; k < f.length; k++) {
        var hk = Math.max(1, Math.round(f[k] / f0)); if (hk > 32) continue;
        var dev = 1200 * Math.log2(f[k] / (hk * f0)); sc += Math.exp(-(dev / 15) * (dev / 15)) * w[k];
      }
      sc /= wsum; if (sc > best) best = sc;
    }
    return best;
  }
  function clusterSpectrum(spec) {
    var cl = [], last = null, lw = 0, lf = 0, sf = 0, sf2 = 0;
    for (var i = 0; i < spec.length; i++) {
      var fi = Math.max(spec[i][0], 1), wi = spec[i][1] * spec[i][1];
      if (last !== null && Math.abs(1200 * Math.log2(fi / last)) <= 30) {
        lf += wi * Math.log2(fi); lw += wi; sf += wi * fi; sf2 += wi * fi * fi; last = lw > 0 ? Math.pow(2, lf / lw) : fi;
      } else {
        if (last !== null) cl.push({ f: last, w: lw, spread: Math.sqrt(Math.max(0, sf2 / lw - (sf / lw) * (sf / lw))) });
        lf = wi * Math.log2(fi); lw = wi; sf = wi * fi; sf2 = wi * fi * fi; last = fi;
      }
    }
    if (last !== null) cl.push({ f: last, w: lw, spread: Math.sqrt(Math.max(0, sf2 / lw - (sf / lw) * (sf / lw))) });
    return cl;
  }
  function describe(spec, energy, pitch, seed) {
    var m = { partials: spec.length, clusters: 0, harmony: 0, brightness: 0, inharmonicity: 0, beating: 0, attack: null, unrest: 0 };
    if (!spec.length) return m;
    var cl = clusterSpectrum(spec); m.clusters = cl.length;
    var cf = cl.map(function (o) { return o.f; }), cw = cl.map(function (o) { return o.w; });
    if (cl.length >= 3) {
      var rng = makeRng((seed ^ 0x9e3779b9) >>> 0), obs = harmonicScore(cf, cw);
      var lo = Math.log2(Math.min.apply(null, cf)), hi = Math.log2(Math.max.apply(null, cf)), nulls = 0, cnt = 0;
      for (var r = 0; r < 24; r++) { var fr = cf.map(function () { return Math.pow(2, lo + (hi - lo) * rng.u()); });
        var vv = harmonicScore(fr, cw); if (!isNaN(vv)) { nulls += vv; cnt++; } }
      m.harmony = cnt ? obs - nulls / cnt : 0;
    }
    var ws = 0, fs = 0; for (var i = 0; i < spec.length; i++) { var w = spec[i][1] * spec[i][1]; ws += w; fs += w * spec[i][0]; }
    m.brightness = ws > 0 ? fs / ws / pitch : 0;
    var wmax = Math.max.apply(null, cw), fund = null, fw = -1;
    for (var j = 0; j < cl.length; j++) if (Math.abs(1200 * Math.log2(cf[j] / pitch)) < 100 && cw[j] > fw) { fw = cw[j]; fund = cf[j]; }
    if (fund === null) fund = cf[cw.indexOf(wmax)];
    var dsum = 0, dw = 0, bsum = 0;
    for (var k = 0; k < cl.length; k++) { if (cw[k] < 0.01 * wmax) continue;
      var hk = Math.max(1, Math.round(cf[k] / fund)); dsum += cw[k] * Math.abs(1200 * Math.log2(cf[k] / (hk * fund))); dw += cw[k];
      bsum += cw[k] * cl[k].spread; }
    m.inharmonicity = dw > 0 ? dsum / dw : 0; m.beating = dw > 0 ? bsum / dw : 0;
    // energy trace is sampled every 10 ms
    var tail = energy.slice(Math.floor(energy.length / 2)), mean = 0;
    for (var t = 0; t < tail.length; t++) mean += tail[t]; mean /= Math.max(1, tail.length);
    if (mean > 0) {
      for (var u = 0; u < energy.length; u++) if (energy[u] >= 0.5 * mean) { m.attack = u * 0.01; break; }
      var vs = 0; for (var t2 = 0; t2 < tail.length; t2++) vs += (tail[t2] - mean) * (tail[t2] - mean);
      m.unrest = Math.sqrt(vs / Math.max(1, tail.length)) / mean;
    }
    return m;
  }

  var api = { play: play, randomGenome: randomGenome, makeRng: makeRng, P: P, GLEN: GLEN, N_BODY: N_BODY, FULL_LEN: FULL_LEN,
              clusterSpectrum: clusterSpectrum, harmonicScore: harmonicScore };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.PartialEngine = api;
})(typeof self !== "undefined" ? self : this);
