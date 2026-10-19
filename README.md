# Emergent systems research

Research notes on emergent systems, simulations and their proven practical applications, collected with one goal: deciding how to use emergent behaviour in AI systems.

Compiled 2026-10-19. Written for an engineer, not a philosopher. Every chapter ends with a Sources list; claims that could not be verified against a primary source are marked "(unverified)" inline rather than dropped.

## Start here

If you only read one file, read [`docs/05-playbook-using-emergence-for-ai.md`](docs/05-playbook-using-emergence-for-ai.md). It contains the decision gate, the five emergence engines with a track record, the design principles, the risk table and a staged experiment roadmap.

## Structure

| # | File | What it answers | Words |
|---|---|---|---|
| 1 | [Foundations and the simulation toolbox](docs/01-foundations-and-simulations.md) | What emergence is, what the canonical simulations proved, which ABM and RL tools to use, how to measure emergence | ~5,500 |
| 2 | [Proven practical applications](docs/02-proven-practical-applications.md) | Where emergence has been deployed or validated for real: swarm optimisation, robotics, crowds and traffic, epidemiology, finance and policy, energy, networks, plus emergence as a risk | ~6,000 |
| 3 | [Emergence inside AI systems](docs/03-emergence-in-ai-systems.md) | Self-play and autocurricula, emergent communication, the LLM "emergent abilities" debate, emergent misalignment, open-endedness and quality-diversity, neural cellular automata, mechanisms and levers | ~6,000 |
| 4 | [Multi-agent LLM systems and simulated societies](docs/04-multi-agent-llm-systems-and-simulated-societies.md) | Generative-agent simulations, production multi-agent frameworks, emergent risks in LLM collectives, benchmarks, design patterns and anti-patterns | ~5,300 |
| 5 | [Playbook: using emergence for AI](docs/05-playbook-using-emergence-for-ai.md) | Synthesis: when to use emergence, which engines work, principles, measurement, risks, roadmap | ~2,100 |

## Evidence grades

Used consistently across chapters 2, 3 and 5.

| Grade | Meaning |
|---|---|
| **A** | Deployed in production with reported, attributable results |
| **B** | Validated against real data, field trial, or strong peer-reviewed research with public code |
| **C** | Research result only, or claims from a single commercial narrator |

## Headline findings

1. **Reliable emergence engines share one structure:** a cheap, hard-to-fake verifier plus a mechanism that keeps the task at the frontier of ability (opponent, curriculum, self-proposed problem). TD-Gammon (1992) and AlphaEvolve (2025) are the same loop with a different mutation operator.
2. **In production, "emergent" is usually a vocabulary, not a mechanism.** Amazon/Kiva, drone shows and every shipping multi-agent LLM framework are designed, mostly centralised coordination with local execution. The genuinely emergent production successes are in infrastructure: gossip protocols, self-organising cellular networks, self-organising traffic control, transactive energy.
3. **The properties that transferred to practice** are simple local rules on cheap agents, explicit damping of feedback loops, redundancy as a design input, hybrid central/decentral layering, and validation against the incumbent's benchmark.
4. **Genuine emergence in LLM collectives is real but narrow:** spontaneous conventions and collective bias, supracompetitive pricing, diffusion of information and roles. Populations default to commons collapse, herding and collusion unless mitigated.
5. **Emergence is symmetric.** The same generalisation pressure that yields tool use and world models yields emergent misalignment from a narrow fine-tune. Mitigations exist and have been shown to be undone by further training.
6. **The environment is the ceiling.** Task-space richness decides whether there is anything left to discover; for most teams it pays more than scaling the learner.

## Known gaps

- Several famous swarm-intelligence business cases (Southwest cargo, Air Liquide, Migros/Barilla) rest on a single vendor or consultant source and are graded accordingly.
- No confirmed out-of-sample validation was found for the largest LLM society simulations (OASIS, AgentSociety).
- Full PDFs were not fetched for every source in this session; a number of figures rest on abstracts and official summaries and are marked where that matters.

## Suggested next step

Stage 0 and Stage 1 of the roadmap in chapter 5: a small simulation and metrics package, then a replication of the LLM naming-game experiment. Both are days of work and settle whether this direction is worth a larger investment.
