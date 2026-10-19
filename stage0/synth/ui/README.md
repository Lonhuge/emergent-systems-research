# Teiltongarten (breeding instrument)

Published page: https://claude.ai/artifact/TzNC12wiRrisuquCGyNEqZ (private to the owner).

- `engine.js` is a port of `sim/ecology.py` with the v2 instrument options in
  `sim/instrument.py`: fast notes, a low-loss body resonance at the chosen
  pitch, combination-tone births (f1 + f2, |f1 - f2|), capped phase pull, one
  shared controller per note. Genome = 75 controller weights + 12 body genes
  + 18 physics genes: drive duration from strike to held tone, rise time,
  damping, up to three extra body resonances at any ratio, coupling, birth and
  noise strength, tremolo (v3, 14 genes), plus strike noise, frequency-dependent
  damping, purity (split spread and crowding penalty) and exciter brightness
  (v4). Shorter genomes get neutral values for missing genes; 87-gene genomes
  keep the fixed v2 physics.
- v4 also widens the frequency range from 55-3520 Hz to 55-17300 Hz at 44.1 kHz.
  The old ceiling was the "telephone" sound: no partial ever exceeded 3.47 kHz.
  Triad search now uses sorting and binary search (instrument runs only; frozen
  phase-1 runs keep the original code path and reproduce bit for bit).
- Known limit: overtones are created from the fundamental by combination tones,
  so they enter one after another (median onset 20/70/90/100 ms for harmonics
  1-4), which is the brass/wind attack. Simultaneous harmonic onset, as in
  plucked strings, would need a resonator with harmonic modes, which would hand
  the harmonic series to the system instead of letting it emerge. Not built in.
- Why v3: with fixed physics (held nonlinear drive on one resonance) every rule
  set sounded like an oboe or a bassoon. Across 30 random rule sets the
  controller mainly moved spectral tilt; attack, steadiness and harmonicity
  barely varied. Instrument families differ mostly in exciter and body.
- v3 cross-check: notes with several resonances are strongly seed-dependent in
  both engines (the strongest component changes between seeds of the same
  genome), so agreement is distributional, not per note.
- Fixed in v3: the pitch resonance could push body loss below zero, so the
  fundamental rang forever after the drive stopped; body loss is now floored.
  Descriptors use the loudest moment; inharmonicity below the pitch is measured
  against subharmonics.
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
