# Pre-registration: partial ecology, phase 1 (open, no target)

**Status: FROZEN on 2026-10-19** by the commit whose message starts with
"Freeze pre-registration". Any later change must be a new, dated section
below, never an edit. No run on seeds 0–4 happened before the freeze.

## Question

A population of sine partials behaves as agents on a log-frequency axis. They
migrate, split with mutation, and die. A sustained exciter feeds them through a
generic quadratic nonlinearity that couples near-resonant triads f_j + f_k ~ f_m.
Nothing in the rules mentions a fundamental, integer ratios, a harmonic series,
or a target spectrum. Starting from random inharmonic partials:

**Does the population organise itself into a harmonic lattice, and is that
organisation an emergent product of the agents' interaction and behaviour?**

## Known versus open

- Known physics (Fletcher 1978): a nonlinear drive can lock slightly inharmonic,
  *fixed* resonances into harmonic relationship.
- Open here: there are no fixed resonances. Partials choose where to sit,
  multiply and die. Whether a globally consistent harmonic lattice self-assembles
  from local triad interactions, and whether agent behaviour (migration,
  heritable controllers) is necessary for it, is not known in advance.

## Conditions (5 seeds each, seeds 0–4, 60 s simulated time per run)

| condition | change |
|---|---|
| full | everything on |
| no_coupling | quadratic coupling off (q = kappa = 0); triads still sensed |
| shuffle_phase | coupling uses phases of randomly permuted partials: same magnitudes, no phase information |
| no_migration | agents cannot move in frequency; only split jitter |
| no_evolution | controllers copied exactly at splits |

Calibration used seeds 100–102 and looked only at viability (population size,
energy, births, deaths), never at harmonicity or locking.

**Disclosed deviation during calibration:** one 20-second probe on seed 100
printed harmonicity excess and lock coherence by mistake (full: H+ 0.11, lock
0.22; no_coupling: H+ 0.00, lock -0.06). The print was removed immediately.
No parameter was changed in response to these values. Seeds 0–4 were never run
before the freeze.

## Primary order parameters

- **harmonicity_excess**: best energy-weighted fit to the harmonic series of
  any f0 (candidates: lowest strong partial / 1..4, ±40 cents grid, tolerance
  15 cents, harmonics up to 32), minus the mean of a null model with the same
  amplitudes and log-uniform random frequencies over the observed range.
  0 means "no more harmonic than chance".
- **lock_coherence**: weighted mean of cos(psi) over near-resonant triads,
  measured on true phases in every condition. 0 means unlocked phases.

## Hypotheses

| id | claim |
|---|---|
| H1a/b | harmonicity_excess(full) > no_coupling and > shuffle_phase |
| H2a/b | lock_coherence(full) > no_coupling and > shuffle_phase |
| H3 | harmonicity_excess(full) > no_migration (agent movement matters) |
| H4 | harmonicity_excess(full) > no_evolution (heritable adaptation matters) |

## Decision rule

Tail mean = mean over the last 25% of each run. A hypothesis is SUPPORTED only
if the five seed values of `full` are all above all five baseline values AND
Cohen's d > 2. Everything else is "not supported", however suggestive.

## Interpretation fixed in advance

- H1 and H2 supported, H3 supported: emergent self-assembly of a harmonic
  lattice that needs agent behaviour. This is the result we are looking for.
- H1 and H2 supported, H3 not supported: harmonicity comes from the coupling
  physics acting on whatever positions exist. Still emergent at the population
  level, but the agents' behaviour does not add anything. Reported as such.
- H1 not supported: no emergent harmonicity in this substrate. Reported as a
  negative result; the substrate is changed, not the metric.
- Harmonicity above zero in no_coupling would indicate an artefact of the
  measurement or of the body landscape and must be explained before any claim.

## Secondary, exploratory (no claims)

triad closure excess, lock magnitude, number of partials, energy, spectral
centroid, spectral entropy, alignment with the body landscape, openness,
migration speed, lineages, number of triads; transient length.

## Parameters

See the DEFAULTS block in sim/ecology.py at the freezing commit.

## Calibration record (viability only, seeds 100–102, 60 s)

Changes made during calibration, each for a viability failure, none touching
the coupling form, the resonance window or the agent rules:

1. Exciter band-pass (low roll-off) instead of a pure tilt: partials piled up
   at the lower frequency bound.
2. Stronger competition between partials closer than ~36 cents: hundreds of
   partials sat at nearly the same frequency.
3. Higher exciter gain: one seed went extinct.
4. Hard exciter power budget P_max shared by all drive sources: coupled
   populations ran away in energy and filled the population cap.
5. Death threshold raised to an audible level and split threshold raised:
   inaudible partials accumulated and filled the cap.
6. Safety cap raised from 128 to 160 after the final calibration peaked at 107.

Final calibration: no extinctions, cap never reached, total energy 0.6–1.2 in
all five conditions.

---

## Amendment A (2026-10-19): long runs

Written after the 60-second main results were known (H1 not supported; H3 and
H4 pointing the other way, not robustly). This amendment does not change any
of the above; it adds a separate, pre-registered experiment.

**Why:** 60 s gives a few hundred births per run. The evolution question (H4)
and the observation that agent behaviour seems to erode harmonic order need
more time to be judged fairly.

**Design:** same five conditions, same frozen parameters, **600 s** simulated
time, **fresh seeds 10–14** (seeds 0–4 are not reused). Snapshot every 1 s.
Audio segments 0–4 s, 296–300 s, 596–600 s.

**Added bookkeeping (read-only, verified not to change trajectories):**
generation counter per partial (`gen_mean`, `gen_max`) and genome diversity
(`genome_dist_mean`).

**Hypotheses:** L-H1a/b, L-H2a/b, L-H3, L-H4 are H1a/b, H2a/b, H3, H4 above,
evaluated on the last 25% of the long runs (450–600 s) with the same decision
rule. A significant effect in the opposite direction is reported as REVERSED.

**Interpretation fixed in advance:**
- L-H4 supported: evolution needs time; the 60-s null result on H4 was too short.
- L-H4 REVERSED (no_evolution robustly more harmonic): heritable adaptation
  actively erodes harmonic order in this ecology (individual advantage versus
  collective order). That would be a substantive negative finding.
- Neither: evolution does not matter for harmonicity in this substrate; next
  step is the substrate change (costly splitting / non-local offspring).
