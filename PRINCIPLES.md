# Principles for this research

Binding rules for all work in this directory. Set by the repository owner on 2026-10-19.

## 1. Real emergence only

- The goal is **genuine, hard emergence**: macro behaviour that nobody specified, that arises from local rules and interaction, and that survives the tests below.
- Do **not** drift into building proven things whose outcome is known in advance. Re-implementing Boids, Game of Life or Schelling as a demo is not research; the answer is already known.
- Designed coordination (orchestrator–worker, hand-written rules that produce a known pattern) is not emergence and must never be labelled as such.
- A result counts as emergent only if, per chapter 1 §4 of the research:
  1. it is a macro property (order parameter, convention, structure) not present in any single agent,
  2. it is absent in a **no-interaction baseline** with otherwise identical parameters,
  3. it is robust across seeds and to ablation of individual agents,
  4. it was not encoded in the rules, the reward or the prompt.
- Negative results are reported as negative. Never tune until "something appears" and then call it emergence.

## 2. Sandboxing grows with the stage

| Stage | What runs | Minimum sandbox |
|---|---|---|
| 0 | numpy simulation, no generated code | own process, `timeout`, `ulimit` on memory and CPU, no network libraries, writes only to `results/`, no `eval`/`exec`/untrusted `pickle` |
| 1 | LLM agent populations, text only | no tools for agents, hard token and cost budgets per run, kill switch, agent messages are untrusted data and never become instructions for the operator or for tools |
| 2–3 | self-play and evolutionary program search, generated code is executed | every candidate in its own container: no network, no credentials, read-only filesystem, time and memory limits; verifier runs separately from the candidate; archives and logs append-only |
| any | — | nothing from a simulation touches this session, git, or credentials; the cloud container's isolation is a backstop, not the sandbox |

## 3. Honesty of measurement

- Report continuous metrics alongside thresholds.
- Always run the no-interaction baseline and at least one ablation before claiming anything.
- Report transient length; run longer than feels necessary.
- State the order parameters and baselines before running, not after.
