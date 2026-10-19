# Pre-registration: fast notes (stage 0, phase 1b)

**Status: FROZEN on 2026-10-19** by the commit whose message starts with
"Freeze notes pre-registration". Later changes only as dated amendments.
No run on seeds 0–499 happened before the freeze.

## Why this experiment

In the 60-second runs, the most harmonic phase appeared after 15–25 s and then
decayed. A playable note must organise itself within its attack, in well under
a second. Evolution within one sustained tone is also the wrong architecture
for an instrument: rules may develop slowly offline, but a note must
self-organise fast with fixed rules.

## Design

- Physics and agent rules: the frozen phase-1 substrate, time-compressed by
  K = 50 for amplitude, migration and splitting rates (sim/fast.py). Phase
  dynamics and resonance window unchanged.
- One note = 4 s of sustained excitation, starting from 24 random inharmonic
  partials (110–880 Hz).
- One shared, random controller per note (one rule set per note, like one
  genome per organism). No mutation within a note.
- Paired design: every seed (rule set + initial partials + body) is played in
  every condition. Seeds 0–499.
- Conditions: full, no_coupling, shuffle_phase, no_migration. (no_evolution is
  dropped: there is no evolution within a note.)

## Calibration (seeds 1000–1039, viability only)

With migration enabled, about 70% of notes with a random shared controller go
extinct (full 29/40, no_coupling 28/40, shuffle_phase 28/40), against 2/40
without migration. Cause: a random shared controller often drifts all partials
in the same direction out of the viable band. This is treated as a property
of random rule sets, not tuned away. The analysis is designed around it.

## Order parameters and window

Window mean over 2.0–4.0 s of each note:
- harmonicity_excess (as in phase 1, null-model corrected)
- lock_coherence (as in phase 1)
Snapshots with fewer than 3 partials count as 0 (no structure).

## Hypotheses and samples

| id | claim | sample |
|---|---|---|
| N-H1a | harmonicity full > no_coupling | all 500 pairs (intention to treat) |
| N-H1b | harmonicity full > shuffle_phase | all 500 pairs |
| N-H2a | lock coherence full > no_coupling | all 500 pairs |
| N-H2b | lock coherence full > shuffle_phase | all 500 pairs |
| N-H3 | harmonicity full > no_migration | pairs viable in both conditions |

Intention to treat is used where survival is similar across conditions
(calibration: 28–29/40). N-H3 is restricted to jointly viable pairs because
survival differs strongly; the survival difference itself is reported.

## Decision rule

Paired differences, Wilcoxon signed-rank (zeros dropped, normal approximation
with tie correction), one-sided. SUPPORTED if p < 0.001 and matched-pairs
rank-biserial r > 0.3. REVERSED if the same holds in the opposite direction.
Otherwise not supported.

## Interpretation fixed in advance

- N-H1 supported: coupling produces harmonic order within a note. Emergent at
  the population level (no harmonic rule exists), but driven by known physics.
- N-H1 and N-H3 supported: agent movement adds to fast harmonic self-assembly.
- N-H1 not supported: fast notes from random rule sets do not self-organise
  harmonically; phase 2 (search over rule sets) becomes the next step.

## Exploratory, no claims

Survival per condition; time course of harmonicity from 0.05 s to 4 s (speed
of organisation); raw harmonicity, triad closure, number of partials, energy,
spectral centroid and entropy. Listening examples: seeds 0–9 of every
condition.
