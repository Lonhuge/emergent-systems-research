# Session handoff (2026-10-20)

Read this first when continuing in a new session. Then `PRINCIPLES.md`.

## Owner's rules
- Real, hard emergence only. Do not drift into building proven things whose outcome is known.
- Sandbox everything (see PRINCIPLES.md §2). No GitHub pushes unless the owner asks.
- Measure emergence with baselines and pre-registration; report negative results as negative.

## Where things are
| Path | What |
|---|---|
| `docs/01..05` | Research knowledge base (foundations, proven applications, emergence in AI, multi-agent LLM systems, playbook) |
| `stage0/` | Generic artificial-life substrate (built, not run) |
| `stage0/synth/sim/ecology.py` | Partial ecology: sine partials as agents (migrate, split, die, triad coupling). Python reference |
| `stage0/synth/PRE_REGISTRATION.md`, `RESULTS_phase1_main.md` | Phase 1 (60 s runs): harmonic self-assembly not supported; agent behaviour eroded order |
| `stage0/synth/PRE_REGISTRATION_notes.md`, `RESULTS_notes.md` | Phase 1b (4 s notes, 500 paired seeds): pre-registered harmonicity metric was inflated by clustering; with a cluster-robust metric, coupling organises stationary partials into a few sum-closed clusters (f1 + f2 = f3), p 3e-18. Migration kills 77% of notes |
| `stage0/synth/sim/instrument.py`, `ui/engine.js` | Breeding instrument: Python reference and browser port (validated distributionally) |
| `stage0/synth/ui/teiltongarten.html` | Published breeding page: https://claude.ai/artifact/TzNC12wiRrisuquCGyNEqZ (private). Tagged notes are in its database, collection `notes` |

## Instrument history (what the owner heard and what changed)
1. v2: pitch via body resonance, combination-tone births, no migration. Owner: "everything sounds like oboe or bassoon". Cause: fixed held reed-like physics; controller only moved spectral tilt.
2. v3: 14 physics genes (drive from strike to held, rise, damping, up to 3 extra resonances, coupling/birth/noise strength, tremolo). Owner: "mostly winds, sometimes like telephone compression".
3. v4: frequency range 3.5 kHz -> 17 kHz (the old ceiling was the telephone sound), 4 more genes (strike noise, frequency-dependent damping, purity, exciter brightness). Genome = 75 controller + 12 body + 18 physics = 105 numbers.

## Open decision for the owner
Overtones arise from the fundamental via combination tones, so they enter one after another (brass/wind attack). String/piano-like simultaneous onset would need a resonator with harmonic modes, which hands the harmonic series to the system instead of letting it emerge. Not built in; the owner has not decided yet.

## Useful commands
```
cd stage0/synth/ui && python3 build.py            # rebuild the page from template.html + engine.js
node -e 'const E=require("./engine.js"); ...'     # run the browser engine headless
cd stage0/synth && python3 -I analyze_notes.py --tag main   # needs results/, which are not in git
```
Results (`stage0/synth/results/`) are git-ignored and were not carried over; they can be regenerated with the run scripts.
