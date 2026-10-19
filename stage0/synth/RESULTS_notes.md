# Fast notes: results for tag `main`

Paired seeds present in all conditions: 500. Window 2.0–4.0 s.

## Survival

| condition | extinct at 4 s | viable in window | population cap reached |
|---|---|---|---|
| full | 387 (77%) | 106 (21%) | 2 |
| no_coupling | 383 (77%) | 108 (22%) | 0 |
| shuffle_phase | 386 (77%) | 108 (22%) | 0 |
| no_migration | 27 (5%) | 465 (93%) | 0 |

## Pre-registered hypotheses

| id | metric | baseline | sample | pairs used | median d | mean full | mean base | r | p (one-sided) | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| N-H1a | harmonicity_excess | no_coupling | itt | 500 (nonzero 131) | +0.0000 | +0.0183 | +0.0170 | +0.01 | 0.48 | **not supported** |
| N-H1b | harmonicity_excess | shuffle_phase | itt | 500 (nonzero 133) | +0.0000 | +0.0183 | +0.0162 | +0.11 | 0.13 | **not supported** |
| N-H2a | lock_coherence | no_coupling | itt | 500 (nonzero 73) | +0.0000 | +0.0306 | -0.0004 | +0.76 | 7.8e-09 | **SUPPORTED** |
| N-H2b | lock_coherence | shuffle_phase | itt | 500 (nonzero 71) | +0.0000 | +0.0306 | +0.0007 | +0.68 | 3.8e-07 | **SUPPORTED** |
| N-H3 | harmonicity_excess | no_migration | viable | 104 (nonzero 104) | -0.1713 | +0.0885 | +0.3379 | -0.71 | 1 | **REVERSED** |

## Exploratory: window means among notes viable in the given condition

| metric | full | no_coupling | shuffle_phase | no_migration |
|---|---|---|---|---|
| harmonicity_excess | 0.087 (n=106) | 0.079 (n=108) | 0.076 (n=108) | 0.297 (n=465) |
| lock_coherence | 0.143 (n=106) | -0.002 (n=108) | 0.004 (n=108) | 0.730 (n=465) |
| harmonicity_raw | 0.430 (n=106) | 0.429 (n=108) | 0.419 (n=108) | 0.496 (n=465) |
| triad_closure_excess | -0.051 (n=106) | -0.048 (n=108) | -0.054 (n=108) | 0.232 (n=465) |
| n | 38.877 (n=106) | 35.811 (n=108) | 35.478 (n=108) | 45.370 (n=465) |
| energy | 0.632 (n=106) | 0.602 (n=108) | 0.620 (n=108) | 0.845 (n=465) |
| centroid_hz | 183.047 (n=106) | 175.959 (n=108) | 178.515 (n=108) | 254.663 (n=465) |
| spectral_entropy_bits | 1.478 (n=106) | 1.492 (n=108) | 1.548 (n=108) | 1.802 (n=465) |

## Exploratory: time course of harmonicity excess, mean over notes viable at that time

| t (s) | full | no_coupling | shuffle_phase | no_migration |
|---|---|---|---|---|
| 0.05 | -0.008 (n=497) | +0.009 (n=495) | +0.010 (n=493) | -0.006 (n=500) |
| 0.1 | +0.048 (n=426) | +0.046 (n=430) | +0.046 (n=427) | +0.074 (n=493) |
| 0.2 | +0.068 (n=315) | +0.056 (n=313) | +0.049 (n=305) | +0.222 (n=475) |
| 0.3 | +0.067 (n=227) | +0.051 (n=234) | +0.067 (n=225) | +0.286 (n=468) |
| 0.5 | +0.069 (n=167) | +0.054 (n=163) | +0.058 (n=160) | +0.314 (n=471) |
| 0.75 | +0.053 (n=144) | +0.067 (n=144) | +0.059 (n=136) | +0.318 (n=470) |
| 1.0 | +0.086 (n=131) | +0.067 (n=133) | +0.044 (n=134) | +0.313 (n=469) |
| 1.5 | +0.099 (n=119) | +0.069 (n=126) | +0.073 (n=125) | +0.310 (n=472) |
| 2.0 | +0.087 (n=118) | +0.084 (n=119) | +0.082 (n=119) | +0.303 (n=474) |
| 3.0 | +0.061 (n=113) | +0.086 (n=115) | +0.073 (n=114) | +0.290 (n=472) |
| 4.0 | +0.086 (n=110) | +0.074 (n=113) | +0.071 (n=113) | +0.286 (n=471) |# Amendment B: artefact check

Seeds: 500

| condition | viable notes | mean clusters (viable) | partials per cluster (viable) | cluster-robust excess (viable) | pre-registered excess (viable) |
|---|---|---|---|---|---|
| full | 106 | 7.8 | 9.22 | -0.024 | +0.087 |
| no_coupling | 108 | 8.4 | 9.24 | -0.018 | +0.079 |
| shuffle_phase | 108 | 8.4 | 8.96 | -0.026 | +0.076 |
| no_migration | 465 | 7.6 | 10.18 | +0.068 | +0.297 |
| no_migration_no_coupling | 459 | 10.9 | 5.30 | -0.037 | +0.010 |

**C1** cluster-robust excess, no_migration > no_migration_no_coupling: pairs 456 (nonzero 455), median d +0.0453, r +0.47, p 3e-18 → **SUPPORTED**
**C2** cluster-robust excess in viable no_coupling notes > 0: n 108 (nonzero 70), mean -0.0181, r -0.22, p 0.94 → **not supported (no residual bias detected)**

Exploratory: cluster-robust excess, full > no_coupling on jointly viable pairs: pairs 95, median d +0.0000, r -0.07, p 0.7

Highest cluster-robust excess in no_migration (seed: excess, clusters): 212: +0.58, 5, 69: +0.58, 3, 13: +0.56, 3, 389: +0.56, 3, 413: +0.55, 3
---

## Reading

**Pre-registered verdicts:** N-H1 not supported, N-H2 supported, N-H3 REVERSED.

**Artefact (amendment B):** the pre-registered harmonicity metric is inflated
by clustering. Splitting creates clusters of about 5–10 near-identical
partials, and few clusters fit a harmonic series more easily than the null.
With the cluster-robust metric, full, no_coupling and shuffle_phase all sit
at about -0.02 (no harmonic order), and the +0.30 of no_migration shrinks to
+0.07. C2 shows no residual bias of the robust metric.

**What survives (C1, supported, p 3e-18, r 0.47):** when partials stay where
they are born, coupling organises the note. With coupling the spectrum
condenses into 3–5 clusters that satisfy sum relations f1 + f2 = f3 (seed 1:
150 + 563 = 713 Hz; seed 6: 205 + 252 = 457 Hz; seed 9: 113 + 142 = 255 Hz
and 255 x 2 = 511 Hz). Without coupling, 9–15 scattered clusters remain.
No rule mentions clusters, sums or ratios. This is the macro-level product of
local triad interaction.

**Honest scope:** sum-closed networks are what three-wave coupling favours,
so this is emergent organisation driven by known nonlinear physics, not a
new mechanism. Harmonic spectra appear only as a special case (f2 = f1, or
octave pairs). The structure resembles wind-instrument multiphonics, which
Fletcher (1978) describes as nonharmonic locked combinations.

**Migration:** with a random shared controller, migration kills 77% of notes
and destroys the organisation in the survivors.

**Sensitivity (not pre-declared):** in 7% of no_migration notes the summed
phase pull of many triads drags single partials far from their base
frequency, occasionally below 0 Hz. This is a flaw of the substrate. C1 holds
when those notes are excluded (424 pairs, r 0.47, p 2e-17).
