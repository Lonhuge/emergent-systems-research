# Teiltongarten (breeding instrument)

Published page: https://claude.ai/artifact/TzNC12wiRrisuquCGyNEqZ (private to the owner).

- `engine.js` is a port of `sim/ecology.py` with the v2 instrument options in
  `sim/instrument.py`: fast notes, a low-loss body resonance at the chosen
  pitch, combination-tone births (f1 + f2, |f1 - f2|), capped phase pull, one
  shared controller per note. Genome = 75 controller weights + 12 body genes.
- `template.html` + `engine.js` -> `build.py` -> `teiltongarten.html`.
- Validation against Python (16 shared genomes, different random streams):
  survival agreed 16/16; harmonic levels 2-5 differ by a median of 1.3 dB,
  within the Python reference's own seed-to-seed spread.
- Tagged notes are stored in the page database, collection `notes`
  (genome, seed, pitch, wander, tags, parents, generation, metrics).
  Python can re-render any stored note with `sim.instrument.play`.

This tool is not a hypothesis test. Breeding by ear is selection by a person;
claims about emergence still need the baselines (interaction off) and the
generalisation test (unseen pitches), both built into each card.
