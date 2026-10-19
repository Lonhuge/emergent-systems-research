# Partial ecology, phase 1 (open): results for tag `main`

Runs: full 5, no_coupling 5, shuffle_phase 5, no_migration 5, no_evolution 5
Extinct at end: full 1, no_coupling 0, shuffle_phase 0, no_migration 0, no_evolution 1
Runs that ever hit the population cap: full 0, no_coupling 0, shuffle_phase 0, no_migration 0, no_evolution 0

## Pre-registered hypotheses

| id | metric | full | baseline | baseline value | d | verdict |
|---|---|---|---|---|---|---|
| H1a | harmonicity_excess | 0.064 ± 0.056 | no_coupling | 0.005 ± 0.076 | +0.88 | **not supported** |
| H1b | harmonicity_excess | 0.064 ± 0.056 | shuffle_phase | -0.019 ± 0.094 | +1.07 | **not supported** |
| H2a | lock_coherence | 0.609 ± 0.254 | no_coupling | 0.072 ± 0.161 | +2.52 | **not supported** |
| H2b | lock_coherence | 0.609 ± 0.254 | shuffle_phase | -0.084 ± 0.183 | +3.13 | **SUPPORTED** |
| H3 | harmonicity_excess | 0.064 ± 0.056 | no_migration | 0.251 ± 0.281 | -0.92 | **not supported** |
| H4 | harmonicity_excess | 0.064 ± 0.056 | no_evolution | 0.249 ± 0.214 | -1.18 | **not supported** |

## All metrics, tail means (mean ± sd over seeds)

| metric | full | no_coupling | shuffle_phase | no_migration | no_evolution |
|---|---|---|---|---|---|
| harmonicity_excess | 0.064 ± 0.056 | 0.005 ± 0.076 | -0.019 ± 0.094 | 0.251 ± 0.281 | 0.249 ± 0.214 |
| lock_coherence | 0.609 ± 0.254 | 0.072 ± 0.161 | -0.084 ± 0.183 | 0.604 ± 0.360 | 0.554 ± 0.366 |
| harmonicity_raw | 0.376 ± 0.290 | 0.289 ± 0.266 | 0.294 ± 0.290 | 0.465 ± 0.335 | 0.575 ± 0.243 |
| triad_closure_excess | 0.007 ± 0.088 | -0.165 ± 0.182 | -0.211 ± 0.139 | -0.199 ± 0.283 | 0.198 ± 0.396 |
| lock_magnitude | 0.855 ± 0.064 | 0.237 ± 0.424 | 0.204 ± 0.382 | 0.698 ± 0.372 | 0.749 ± 0.307 |
| n | 65.757 ± 46.153 | 65.880 ± 38.587 | 74.653 ± 41.512 | 55.040 ± 34.489 | 41.443 ± 25.143 |
| energy | 0.787 ± 0.458 | 0.918 ± 0.511 | 0.890 ± 0.505 | 0.769 ± 0.393 | 0.501 ± 0.374 |
| centroid_hz | 279.760 ± 347.097 | 219.498 ± 159.372 | 138.154 ± 59.527 | 265.159 ± 164.418 | 416.633 ± 421.362 |
| spectral_entropy_bits | 2.515 ± 1.458 | 2.774 ± 1.161 | 2.776 ± 1.606 | 1.780 ± 0.771 | 1.221 ± 0.786 |
| body_alignment | 0.247 ± 0.158 | 0.356 ± 0.111 | 0.289 ± 0.068 | 0.053 ± 0.360 | 0.201 ± 0.301 |
| openness_mean | 0.573 ± 0.108 | 0.428 ± 0.180 | 0.382 ± 0.124 | 0.538 ± 0.105 | 0.449 ± 0.122 |
| speed_abs_mean | 0.128 ± 0.042 | 0.127 ± 0.021 | 0.108 ± 0.057 | 0.000 ± 0.000 | 0.154 ± 0.055 |
| lineages_alive | 2.580 ± 1.768 | 1.537 ± 0.507 | 1.687 ± 0.951 | 4.000 ± 1.871 | 2.593 ± 1.520 |
| n_triads | 13545.734 ± 11709.855 | 2631.249 ± 2169.015 | 5255.109 ± 5082.677 | 3532.893 ± 4202.822 | 3584.007 ± 4221.902 |

## Per-seed harmonicity excess and lock coherence (tail)

- **full**: H+ [+0.094, +0.019, -0.009, +0.092, +0.124]; lock [+0.793, +0.640, +0.590, +0.191, +0.830]
- **no_coupling**: H+ [-0.019, -0.013, -0.051, +0.138, -0.029]; lock [-0.011, -0.001, +0.001, +0.359, +0.012]
- **shuffle_phase**: H+ [-0.028, -0.036, -0.052, +0.138, -0.116]; lock [-0.001, -0.004, +0.000, -0.411, -0.004]
- **no_migration**: H+ [+0.051, +0.143, +0.606, +0.488, -0.035]; lock [+0.089, +0.787, +0.996, +0.395, +0.751]
- **no_evolution**: H+ [+0.570, +0.370, +0.120, +0.092, +0.092]; lock [+0.768, +0.829, +0.121, +0.191, +0.861]

## Time course of harmonicity excess (seed mean)

| t (s) | full | no_coupling | shuffle_phase | no_migration | no_evolution |
|---|---|---|---|---|---|
| 0.2 | -0.030 | -0.023 | -0.032 | -0.003 | -0.030 |
| 5.2 | -0.039 | +0.051 | -0.028 | +0.003 | -0.078 |
| 10.2 | +0.079 | -0.005 | +0.019 | +0.208 | +0.283 |
| 15.2 | +0.251 | +0.031 | -0.051 | +0.250 | +0.377 |
| 20.2 | +0.230 | -0.005 | -0.046 | +0.191 | +0.320 |
| 25.2 | +0.253 | -0.066 | +0.009 | +0.171 | +0.353 |
| 30.2 | +0.080 | +0.028 | -0.065 | +0.270 | +0.310 |
| 35.2 | +0.002 | +0.012 | -0.031 | +0.266 | +0.474 |
| 40.2 | +0.067 | -0.036 | -0.031 | +0.242 | +0.353 |
| 45.2 | -0.010 | -0.054 | -0.060 | +0.244 | +0.245 |
| 50.2 | +0.140 | -0.017 | -0.052 | +0.279 | +0.320 |
| 55.2 | +0.015 | -0.039 | -0.048 | +0.271 | +0.339 |
| 60.0 | -0.020 | -0.022 | -0.037 | +0.271 | +0.340 |

## Final spectra, seed 0 (strongest 12 partials, Hz : amplitude)

- **full** (n=56): 61.1:0.189, 62.2:0.173, 62.7:0.204, 65.4:0.161, 67.5:0.157, 108.3:0.157, 109.4:0.180, 112.1:0.167, 163.5:0.203, 166.3:0.181, 166.8:0.187, 184.7:0.154
- **no_coupling** (n=97): 87.6:0.188, 114.2:0.168, 116.3:0.151, 117.4:0.150, 117.5:0.157, 127.2:0.176, 127.3:0.193, 127.6:0.184, 127.8:0.163, 135.5:0.170, 138.7:0.173, 157.8:0.163
- **shuffle_phase** (n=80): 98.3:0.166, 107.9:0.155, 112.6:0.155, 117.1:0.172, 126.3:0.192, 127.8:0.171, 130.6:0.161, 137.0:0.179, 137.0:0.157, 143.0:0.162, 154.0:0.192, 168.2:0.178
- **no_migration** (n=91): 112.8:0.187, 113.1:0.153, 113.4:0.156, 119.8:0.173, 122.3:0.169, 126.4:0.178, 126.7:0.257, 131.6:0.166, 134.8:0.177, 136.2:0.189, 140.2:0.171, 143.5:0.225
- **no_evolution** (n=61): 104.0:0.135, 104.9:0.125, 104.9:0.154, 105.7:0.125, 105.8:0.130, 106.4:0.128, 210.5:0.184, 210.6:0.135, 211.2:0.135, 211.2:0.150, 211.2:0.130, 212.0:0.153
---

## Reading (written after the analysis, against the frozen interpretation rules)

**Primary verdict: H1 not supported.** The population does not robustly organise
itself into a harmonic lattice. Mean harmonicity excess in `full` is small
(+0.06) and overlaps the no-coupling and shuffled-phase baselines. Per the
pre-registration this is a negative result for emergent harmonicity in this
substrate.

**Phase locking is real but not the open question.** H2b is supported and H2a
narrowly misses (one no-coupling seed shows accidental locking). This confirms
the coupling physics works as built; it is the known mechanism, not the
emergent claim.

**H3 and H4 point the wrong way.** Without migration or without evolution,
harmonicity excess is higher (about +0.25), though not robustly so because the
seed variance is large. Agent behaviour does not create harmonic order here; if
anything it erodes it.

**Exploratory, no claim:** in `full`, harmonicity rises to about +0.25 between
15 and 25 s and then decays to about zero after 35 s. In `no_migration` and
`no_evolution` it stays near +0.25 to +0.35. The final spectra show dense
clusters of many partials within a few hertz (a chorus-like band structure),
for example 61–67 Hz, 108–112 Hz and 163–167 Hz in full seed 0, and an
octave pair of clusters at 104–106 Hz and 210–212 Hz in no_evolution seed 0.

**Not anticipated:** one `full` run and one `no_evolution` run went extinct
before 60 s; calibration had shown no extinctions.

**Extinction check:** both extinctions are seed 3 at 29.5 s. In that seed no
partial ever split (zero births) in `full` and `no_evolution`. Without splits
there is no mutation, so the two conditions are identical by construction.
Seed 3 has a hostile body landscape; this is not a bug. Its tail values come
from a dying single partial and carry no information about organisation.
