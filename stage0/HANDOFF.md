# Stage 0: handoff

Status as of 2026-10-19. Read ../PRINCIPLES.md first: real, hard emergence only; no proven demos; sandbox everything.

## What exists

| File | Purpose |
|---|---|
| sim/world.py | Open artificial-life substrate. Agents have a random 14-8-3 neural controller, local senses (neighbours in 4 sectors, neighbour signals, resource gradients, own energy), one scalar signal channel, energy, death, reproduction with mutation. No fitness function, no reward, no specified macro behaviour. |
| sim/metrics.py | Order parameters: polarisation, Clark-Evans clustering, density–resource correlation, signal entropy, Moran's I, mutual information between signal and neighbours/resource/energy, lineage diversity. |
| run_experiment.py | One condition × seed, writes JSON into results/ only. |
| run_sandboxed.sh | Sandbox wrapper: empty env (no proxy, no credentials), python -I, 4 GB memory, 2 h CPU and wall clock, single-threaded. |
| analyze.py | Compares `full` against baselines. A difference counts only if seed distributions fully separate and abs(d) > 2. |

Baselines: `no_social` (agents cannot perceive each other), `shuffle_signal` (signal channel carries no information), `no_evolution` (no mutation).

## Verified

A smoke test with 300 steps per condition runs cleanly in the sandbox, at about 3 s per 300 steps with the population at cap.

## Open issue before the main runs

The population hits the hard cap of 400 within 300 steps. That means the cap, not ecology, is doing the selection. This is a design intrusion. Before the main runs, tune energy balance (e.g. lower eat_eff or regrow, raise cost_base) so the population is resource-limited well below n_max. Record the chosen values here and do not tune them afterwards against the emergence metrics.

## Next steps

1. Fix the energy balance as above and fix the parameters.
2. Pre-register the order parameters in this file before running.
3. Main run: 4 conditions × 5 seeds × 20,000 steps, e.g.
   `for c in full no_social shuffle_signal no_evolution; do for s in 0 1 2 3 4; do ./run_sandboxed.sh --condition $c --seed $s --steps 20000; done; done`
   (roughly 3–4 h on 4 cores if run in parallel).
4. `python3 -I analyze.py --tag main` and report honestly, including a negative result.
5. Sweep patchiness (0, 0.3, 0.6, 0.9) only after step 4, to look for transitions.
