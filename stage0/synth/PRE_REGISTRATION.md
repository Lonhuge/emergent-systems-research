# Pre-registration: partial ecology, phase 1 (open, no target)

**Status: DRAFT.** Parameters are still being calibrated for viability.
The document is frozen by a commit whose message starts with "Freeze
pre-registration". After that, any change must be a new, dated section below,
never an edit, and no main run may start before the freeze.

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
