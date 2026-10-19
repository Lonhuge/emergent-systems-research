# Playbook: using emergent behaviour for AI

This chapter is the synthesis. Chapters 1–4 collect the evidence; this one turns it into decisions. It is written for an engineer who wants to build something, not for a literature review. Every recommendation points back to the chapter that carries the evidence.

Evidence grades follow the convention used throughout the repo: **A** production-proven, **B** validated research with public code or real-data validation, **C** research result only.

---

## 1. First decision: is emergence the right tool?

Emergence is worth paying for only when the alternative, writing the global behaviour down explicitly, is impossible or too expensive. The proven cases in chapter 2 share a profile. Use this as a gate before starting anything.

| Question | If yes | If no |
|---|---|---|
| Is the global solution unknown or too large to specify (search spaces, open task families, adversarial opponents)? | Emergence candidate | Write the algorithm |
| Is there a **cheap, hard-to-fake verifier** for outcomes (game result, test suite, executor, measured KPI)? | Strongest predictor of success (ch. 3 §6, ch. 4 §6) | Expect drift, sycophantic consensus, reward hacking |
| Can agents be cheap and individually dumb, with complexity in the aggregate? | Classic swarm profile (ch. 2 §9) | You are building a designed multi-agent system; label it as such |
| Can you afford populations and archives instead of one best candidate? | Required for stability (ch. 3 §6) | Single-lineage optimisation cycles or collapses |
| Is predictability more important than discovery? | — | Use designed coordination (orchestrator–worker, ch. 4 §2); it is valuable *because* it is not emergent |

Rule of thumb from chapter 4: everything shipping in production as "multi-agent AI" today is designed coordination. Genuine emergence in LLM collectives is real but narrow (conventions, collusion, information diffusion). Do not confuse the two when planning.

---

## 2. Five emergence engines with a track record

These are the loops that have repeatedly produced useful emergent behaviour. They are ranked by how safely you can bet on them today.

### 2.1 Self-play against a population, scored by a verifier (Grade A)

TD-Gammon → AlphaZero → AlphaStar → OpenAI Five → hide-and-seek. The structure is always the same: a hard outcome signal, an opponent that keeps the task at the frontier, and a population (league, past checkpoints, exploiters) so the system does not chase its tail (ch. 3 §1, §6).

- **For LLMs:** verifier-grounded self-play for reasoning and code (SPIN 2024, Absolute Zero Reasoner 2025) is Grade B with public code (ch. 3 §7, ch. 4 §5).
- **Minimum viable setup:** a task generator, a solver, an executable checker, an archive of past solvers. Train against the archive, never a single copy.

### 2.2 LLM-driven evolutionary program search with a hard evaluator (Grade A)

FunSearch (2023) → AlphaEvolve (2025), with open reimplementations. The LLM is the mutation operator; an evaluator scores candidates; a MAP-Elites-style archive keeps diversity (ch. 3 §4, §7). Production use reported at Google for scheduling and kernels.

- **Best fit:** any problem where you can score a program in seconds (heuristics, kernels, schedulers, prompts, test generators, agent policies).
- **This is the most accessible high-value entry point for a small team.**

### 2.3 Quality-diversity search and open-ended curricula (Grade B)

Novelty search, MAP-Elites, POET, Voyager, OMNI-EPIC. The core insight is that stepping stones look useless until they are needed, so you preserve diversity deliberately (ch. 3 §4). Voyager-style skill libraries with automatic curricula work with public code; FM-as-interestingness-judge (OMNI-EPIC, ASAL) works but the judge is exploitable.

### 2.4 Stigmergy and local rules with damping (Grade A in infrastructure, C in "AI")

Gossip protocols, 3GPP self-organising networks, self-organising traffic lights, transactive energy (ch. 2 §3, §6, §7). The engineering lesson that transferred: simple local rules, explicit damping (evaporation, timeouts, bounded waiting), redundancy as a design input, and a central layer wherever it is cheap and auditable.

- **For AI systems:** this is the design vocabulary for agent fleets and tool-using swarms (rate limits, back-off, shared-state decay, hybrid central assignment plus local execution). Ant-routing-style algorithms themselves never reached production in IP networks; copy the properties, not the metaphor.

### 2.5 Population simulation as a test and discovery instrument (Grade A/B in simulation, C as "synthetic humans")

Agent-based models earned policy use when they beat the incumbent benchmark: epidemiology (MIDAS, Report 9, Covasim), crowds (Jamarat Bridge), macro forecasting (Poledna et al., Bank of Canada) (ch. 2 §3–5). LLM populations (Smallville, Project Sid, AgentSociety, OASIS) reproduce qualitative social phenomena, and the 1,000-people study reaches ~85% normalised accuracy on survey answers (ch. 4 §1).

- **Reliable use now:** simulation-based evaluation of your own agents before deployment, red-teaming with adversarial agent populations, stress-testing protocols (ch. 4 §5).
- **Unreliable use now:** demographic personas standing in for user research; outputs are homogenised and stereotyped (ch. 4 anti-patterns).

---

## 3. Design principles that recur across all four chapters

1. **A verifier at the boundary.** Every A-grade system has one. If your judge is a model, audit it adversarially and expect hacking (ch. 3 §6, ch. 4 §6).
2. **Diversity by construction.** Archives, leagues, mixed model families, independent agents. Correlated errors compound; independent ones cancel (ch. 3 §6, ch. 4 §6).
3. **Damping and bounded loops.** Evaporation, timeouts, termination rules, effort caps. Every documented disaster (flash crash, cascading blackouts, metastable failures, runaway agent spawning) lacked one (ch. 2 §7, ch. 4 §6).
4. **Individual coherence before collective behaviour.** Incoherent agents produce noise. PIANO's cognitive bottleneck and Smallville's reflection module are the LLM versions of this (ch. 4 §6).
5. **Topology is a first-class parameter.** Star vs chain vs graph changes outcomes more than model choice in many settings (ch. 4 §6).
6. **Shape the environment, not the agents.** The Jamarat redesign changed geometry and timing, not pilgrims. For AI: change task space, incentives, rate limits, channels (ch. 2 §9, ch. 3 §6).
7. **Hybrid over purist.** Kiva, DiDi, drone shows and the Anthropic research system all centralise what is cheap and decentralise what is not (ch. 2 §9, ch. 4 §2).
8. **Validate against the incumbent's benchmark.** ABMs that only offered "insight" stayed academic (ch. 2 §9).

---

## 4. Measuring emergence in practice

The formal measures (statistical complexity, causal emergence, integrated information) are mostly not usable at production scale (ch. 1 §4). What practitioners actually do:

| Signal | How | Why |
|---|---|---|
| Continuous metrics next to accuracy | Log per-token loss, partial credit, edit distance | Reveals capabilities approaching before they "appear"; defuses the mirage debate (ch. 3 §3) |
| Regime-change detection | Behaviour clustering, probe accuracy over training, feature diffing | Representations emerge before behaviours (induction heads, Othello boards, persona features) (ch. 3 §3, §5) |
| Population-level statistics | Convention convergence time, diversity indices, Gini on resources, survival in commons dilemmas | Standard in GovSim, naming-game, OASIS evaluations (ch. 4 §4) |
| Macro patterns against ground truth | Pattern-oriented modelling, out-of-sample forecast error | How ABMs earned policy credibility (ch. 1 §3, ch. 2 §9) |
| Ablations of the mechanism | Remove communication, memory, diversity, or the verifier and re-run | The only way to prove the behaviour is emergent rather than prompted or designed |

Treat every emergent property as a **state, not a possession**: in-context learning can fade, conventions break, alignment regresses after further fine-tuning (ch. 3 key takeaways).

---

## 5. Risks and controls

| Risk | Evidence | Control |
|---|---|---|
| Reward hacking of soft evaluators | DGM fake logs, AI Scientist, reward-hacking-to-misalignment chain (ch. 3 §6) | Executable verifiers; sandboxing; adversarial audits of judges |
| Emergent misalignment from narrow fine-tuning | Betley et al. 2025 and follow-ups (ch. 3 §3) | Benign framing / inoculation prompting; monitor persona features; re-test after every fine-tune |
| Collusion and supracompetitive pricing among agents | Fish et al. 2024, Lin et al. 2024 (ch. 4 §3) | Never give profit-maximising agents a shared market without monitoring; prompt audits |
| Herding, polarisation, diversity collapse | OASIS, echo-chamber sims, 2025–26 conformity work (ch. 4 §3) | Diversity-preserving topology; independent agents; no shared ranking without control |
| Prompt-injection propagation between agents | Morris II 2024 (ch. 4 §3) | Sanitise agent-to-agent channels; treat all inter-agent content as untrusted |
| Model collapse from recursive self-training | Shumailov et al. 2024 (ch. 3 §6) | Ground self-generated curricula in an executor, real data or humans |
| Cascades and metastable failure in agent fleets | Flash crash, 2003 blackout, AWS 2011 (ch. 2 §7) | Circuit breakers, back-off with jitter, effort caps, kill switches |
| Over-trusting synthetic populations | Silicon-sample critiques (ch. 4 §1) | Validate against held-out real data before any decision rides on it |

---

## 6. A staged experiment roadmap

Each stage is small enough to finish, produces a reusable asset, and tests one claim from the research. Costs are rough and assume a single engineer.

### Stage 0 — Build intuition and metrics (days)
- Implement Boids, Game of Life, Schelling and a growing Neural Cellular Automaton (ch. 1 §2, ch. 3 §5).
- Deliverable: a small `sims/` package plus a `metrics/` module (diversity index, convergence time, cluster count, simple probe harness) you will reuse in every later stage.
- Claim tested: you can tell designed from emergent behaviour by ablation.

### Stage 1 — Replicate emergent conventions in an LLM population (days)
- Reproduce the naming game of Ashery et al. 2025 with 20–50 cheap LLM agents, then the committed-minority tipping experiment (ch. 4 §1, §6).
- Deliverable: a population harness with topology, memory and channel controls.
- Claim tested: conventions and collective bias emerge without instruction; topology and a committed minority steer them.

### Stage 2 — Verifier-grounded self-play on a domain task (1–2 weeks)
- Pick a task with an executable checker (unit tests, SQL correctness, schema validation, a game). Build proposer, solver and archive; follow the Absolute Zero / SPIN pattern (ch. 3 §7, ch. 4 §5).
- Deliverable: a self-play loop that measurably improves a small open model or a prompt policy.
- Claim tested: a cheap verifier plus frontier-of-ability curriculum produces improvement without labels; watch for hacking.

### Stage 3 — LLM evolutionary program search on a real problem (1–2 weeks)
- Use an open FunSearch/AlphaEvolve-style framework with a MAP-Elites archive on a problem you actually have (a heuristic, a scheduler, a prompt, a test generator) (ch. 3 §4, §7).
- Deliverable: a search harness with evaluator, archive and provenance log.
- Claim tested: this is the most accessible high-value entry point; measure gain against your current best.

### Stage 4 — Simulation-based evaluation of an agent before deployment (2–4 weeks)
- Build a population sandbox (GovSim-style commons dilemma or a market with an adversarial newcomer) and run your production agent inside it (ch. 4 §4–6).
- Deliverable: a pre-deployment test suite that reports cooperation, collusion, herding and injection-propagation metrics.
- Claim tested: failures of LLM collectives are predictable in sandboxes and mostly engineering failures (MAST taxonomy).

### Stage 5 — Decide on a product direction (after 0–4)
Candidate directions, ranked by evidence and accessibility:

| Direction | Engine | Grade | Why now |
|---|---|---|---|
| Evolutionary search service for internal heuristics, prompts and tests | 2.2 + 2.3 | A/B | Public code, clear ROI, safe (hard evaluator) |
| Self-play training loop for a domain-specific model | 2.1 | B | Public recipes; needs only a verifier |
| Agent-fleet runtime with stigmergic coordination primitives (decay, back-off, bounded loops, hybrid assignment) | 2.4 | A (properties) | The infrastructure lessons are proven; the AI-agent framing is new |
| Simulation sandbox for agent evaluation and red-teaming | 2.5 | B | Benchmarks exist (GovSim, MARBLE, SOTOPIA); demand is rising with agent deployment |
| Synthetic populations for product or policy research | 2.5 | C | Validity problems unsolved; only with real-data validation gates |

---

## 7. Reading order

1. Chapter 1 §1 and §5 for definitions and the practitioner takeaways.
2. Chapter 3 §6 and §7 for mechanisms and what is usable today.
3. Chapter 4 §6, anti-patterns and key takeaways for LLM collectives.
4. Chapter 2 §9 for the properties that made emergence work in production.
5. Then the full chapters, in any order, as reference.

---

## 8. Open questions this repo does not settle

- Whether population-level LLM simulations predict anything out of sample (no confirmed validation found for OASIS or AgentSociety; ch. 4 gaps).
- Whether emergent-misalignment mitigations hold under continued training (evidence says they can be undone; ch. 3 §3).
- Which formal emergence measures scale to production models (none clearly do; ch. 1 §4).
- The real provenance of several famous swarm-intelligence business cases (Southwest, Air Liquide, Migros/Barilla are single-narrator claims; ch. 2 §1).
