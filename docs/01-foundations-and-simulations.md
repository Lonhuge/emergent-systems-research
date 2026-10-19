# Foundations of Emergence and the Simulation Toolbox

This chapter gives a software engineer a working vocabulary for emergence, a tour of the canonical simulations that established the field and what each actually demonstrated, a map of today's agent-based modelling (ABM) and multi-agent RL toolbox, and an honest look at how emergence can be measured. Every major claim links to a source; items not verifiable against a primary source are marked "(unverified)". Direct page fetches were blocked during research, so verification relied on search snippets of primary papers, official docs and reputable secondary sources.

## 1. What emergence is

### 1.1 Working definitions

**Emergence.** A system exhibits emergence when coherent macro-level features ("emergents") arise dynamically from interactions among micro-level parts and are novel relative to the parts individually. This is De Wolf and Holvoet's (2005) operational definition, standard in multi-agent systems work; the same paper argues emergence and self-organisation are distinct and can occur separately ([via arXiv survey](https://arxiv.org/pdf/1506.09032)).

**Weak emergence.** A macrostate is weakly emergent when it can be derived from the micro-dynamics and boundary conditions "but only by simulation" (Bedau 1997, restated 2003) ([quoted in JASSS 13(1)9, 2010](https://www.jasss.org/13/1/9.html)). The Game of Life is the canonical example: rules fully known, outcome knowable only by running it. Chalmers (2006) draws the same line: weak emergence is deducible in principle from low-level truths even if surprising; strong emergence is not deducible even in principle ([Chalmers, "Varieties of Emergence"](https://consc.net/papers/granada.html)).

**Strong emergence.** High-level properties not deducible even in principle from low-level laws, typically said to exert downward causation (Chalmers 2006). Consciousness is the only serious candidate; nothing built in software is strongly emergent, since a program is by construction derivable from its code.

**Anderson's "More is Different" (1972).** Reducing everything to fundamental laws does not let you reconstruct the universe from them: "at each level of complexity entirely new properties appear", and each level of the scientific hierarchy needs new laws and concepts. His mechanism was broken symmetry, where a many-body system settles into a state less symmetric than its equations ([Anderson, Science 177:393–396, 1972](https://www.mit.edu/~kardar/research/seminars/EPB/PWA-Science72.pdf)). It became the founding text of anti-reductionist complexity science.

**Complex adaptive systems (CAS).** John Holland's term for systems of many interacting adaptive agents whose aggregate behaviour is hard to predict from the parts. *Hidden Order* (1995) lists mechanisms common to all CAS: aggregation, tagging, nonlinearity, flows, diversity, internal models and building blocks ([Leonardo review](https://www.leonardo.info/reviews_archive/pre2000/malinahidden.html); [reason.com review, 1996](https://reason.com/1996/12/01/learning-curve)). Holland was an external professor at the Santa Fe Institute, where the CAS framing was developed, until his death in 2015 ([University of Michigan obituary](https://record.umich.edu/?p=37703)).

**Self-organisation.** A system acquires and maintains structure without external control. Shalizi's thesis makes this precise as a self-generated increase in statistical complexity (Section 4) ([Shalizi thesis](https://www.bactra.org/thesis)).

**Stigmergy.** Coined by Grassé in 1959 for termite nest building: a trace left in the environment by one action stimulates a later action by the same or another agent, so coordination runs through the environment rather than direct communication ([Theraulaz & Bonabeau 1999](https://apice.unibo.it/xwiki/bin/view/Publication/StigmergyhistoryArtificiallife5); [Holland & Melhuish 1999](https://cse-robotics.engr.tamu.edu/dshell/cs689/papers/holland99stigmergy.pdf)). For an engineer: any shared mutable state that agents read and write (blackboard, vector store, ticket queue) is a stigmergic channel.

**Criticality and the edge of chaos.** Langton (1990) defined λ, the fraction of rule-table entries mapping to a non-quiescent state, and showed cellular automata pass from ordered to chaotic as λ rises, with the longest transients and richest behaviour near a critical λc, where he conjectured computation-capable rules (roughly Wolfram's Class 4) live ([arXiv review of dynamical criticality, 2015](https://arxiv.org/pdf/1512.05259); [Wikipedia: Christopher Langton](https://en.wikipedia.org/wiki/Christopher_Langton)). Self-organised criticality (Bak, Tang and Wiesenfeld 1987) is the related claim that some driven systems tune themselves to a critical state with power-law event sizes, the sandpile being the toy model ([BTW, PRL 59:381, 1987](https://courses.physics.ucsd.edu/2016/Spring/physics235/BTW-PRL.pdf)). Caveat: Mitchell, Crutchfield and Hraber (1993) failed to replicate Packard's evidence that evolution drives CA rules toward λc and attributed the clustering to artefacts of the genetic algorithm used ([Mitchell et al. 1993](https://arxiv.org/pdf/adap-org/9306003)). The "critical brain hypothesis" remains contested on similar grounds ([Frontiers review, 2021](https://www.frontiersin.org/journals/systems-neuroscience/articles/10.3389/fnsys.2021.709677/pdf); [critical assessment, arXiv 2026](https://arxiv.org/pdf/2604.21071)).

**Downward causation and the exclusion debate.** Strong emergentists claim wholes causally constrain their parts. Kim's causal exclusion argument (1993–1999) replies that if every physical event has a sufficient physical cause and there is no systematic overdetermination, a macro property adds no causal work: identify it with its micro base or accept it is epiphenomenal ([NDPR review](https://ndpr.nd.edu/news/philosophical-and-scientific-perspectives-on-downward-causation/); [Kairos paper](https://kairos.campus.ciencias.ulisboa.pt/wp-content/uploads/sites/17/2023/04/The-Downward-Causation-Argument-against-Emergentism.pdf)). Critics say the premises beg the question. The engineering-relevant version is Hoel's (Section 4): a macro description can be a better *model* without anything metaphysically new happening.

### 1.2 Criteria people actually use to say "this is emergent"

Across the literature (Goldstein 1999; De Wolf & Holvoet 2005; Bedau 1997; Rosas et al. 2020) the recurring tests are:

| Criterion | Test you can apply |
|---|---|
| Micro-macro effect | A describable macro property (flock, cluster, price level) that no single agent has. |
| Radical novelty | Not a simple sum or average of the parts; mean agent income does not count. |
| Coherence | The pattern keeps its identity while parts churn (a traffic jam moves backwards while cars move forwards). |
| Dynamical arising | Appears over time from interactions, not encoded in the initial condition. |
| Decentralised control | No agent or central component computes it. |
| Two-way link | The macro pattern constrains future micro behaviour. |
| Robustness | Survives perturbation and loss of parts; not an artefact of one run. |
| Non-derivable except by simulation | No closed form; you have to run it (weak emergence). |
| Macro predicts better than micro | A coarse-grained model has higher effective information or predictive power (Hoel; Rosas). |

Goldstein's 1999 list (radical novelty, coherence, global level, dynamical, ostensive) is the origin of several entries ([via arXiv review, 2025](https://arxiv.org/pdf/2508.08548)). The full De Wolf–Holvoet characteristic list is cited from memory of the paper, whose PDF could not be fetched; the definition itself is verified (partly unverified).

Rule of thumb: if removing 10 percent of agents leaves the macro pattern intact, no agent's local state contains the pattern, and you had to run the system to find out, you are looking at weak emergence. That is the only kind you will engineer.

## 2. Canonical simulations and what each proved

Each entry gives the rules, the emergent phenomenon, and why it matters.

### 2.1 Conway's Game of Life (1970)

Rules: a dead cell with exactly three live neighbours is born; a live cell with two or three survives; all others die (B3/S23). Popularised by Gardner's October 1970 *Scientific American* column. Conway offered $50 for a pattern that grows without bound; Gosper's MIT group found the glider gun in November 1970, emitting a glider every 30 generations ([LifeWiki](https://conwaylife.com/wiki/Conway's_Game_of_Life)). Guns and gliders build logic gates; Rendell built an explicit Turing machine in Life, the most accessible of several universality proofs ([Rendell, UWE](https://uwe-repository.worktribe.com/output/822575); [LifeWiki: Turing Machine Universality](https://conwaylife.com/wiki/Turing_Machine_Universality_of_the_Game_of_Life)). Why it matters: the cleanest demonstration that a system's capabilities are not visible in its rules, and the standard example of weak emergence.

### 2.2 Wolfram's classes and Rule 110 (1984, 2004)

Wolfram (1984) sorted 1D CA into four classes by behaviour from random initial conditions: (1) homogeneous, (2) simple stable or periodic structures, (3) chaotic, (4) complex localised structures that propagate and interact, conjectured capable of universal computation ([Wolfram 1984 summary](https://www.ics.uci.edu/%7eeppstein/ca/wolfram.html); [arXiv](https://arxiv.org/pdf/cond-mat/9409080)). The classification is heuristic. Cook proved Rule 110 universal by emulating a cyclic tag system with gliders on a periodic background; presented in 1998, published in 2004 after a legal dispute with Wolfram Research ([Cook 2004](https://complex-systems.com/?p=2418); [Wikipedia: Rule 110](https://en.wikipedia.org/wiki/Rule_110)). Why it matters: an 8-bit lookup table suffices for universality, and Class 4 is the empirical home of "interesting" behaviour.

### 2.3 Langton's ant (1986)

Rules: one agent on a black/white grid; on white turn right, on black turn left; flip the cell; step forward. From an empty grid the path looks pseudo-random for about 9,977 steps, then locks into a 104-step repeating "highway"; whether this happens from every finite start is open. Gajardo, Moreira and Goles showed the ant can compute any Boolean circuit, hence is universal ([Wikipedia](https://en.wikipedia.org/wiki/Langton%27s_ant); [Gajardo et al. 2002](https://arxiv.org/pdf/nlin/0306022)). Attribution to Langton's 1986 Physica D paper is widely repeated but not confirmed from the text (unverified) ([Langton 1986](https://deepblue.lib.umich.edu/items/76966fa1-6b4e-498c-bbfc-2b884c2a5245)). Why it matters: a deterministic two-state rule gives a long chaotic transient and then order; short runs tell you little.

### 2.4 Reynolds' Boids (1987)

Rules: each boid reacts only to flockmates within a limited neighbourhood (distance and angle) using separation, alignment and cohesion. Presented at SIGGRAPH 1987 as "Flocks, Herds, and Schools: A Distributed Behavioral Model" ([Wikipedia: Boids](https://en.wikipedia.org/wiki/Boids); [Ohio State graphics history](https://ohiostate.pressbooks.pub/graphicshistory/?p=280)). Why it matters: lifelike collective motion needs no leader and no global plan; it became the template for swarm robotics and the benchmark model in every ABM framework.

### 2.5 The Vicsek model (1995)

Rules: particles move at constant speed and each step adopt the average heading of neighbours within radius r plus noise of amplitude η. Vicsek et al. (PRL 75:1226, 1995) found a transition from disorder to collective motion as noise falls or density rises, via spontaneous symmetry breaking; the transition's order was debated for a decade ([Vicsek et al. 1995](https://arxiv.org/pdf/cond-mat/0611743); [debate review, 2009](https://arxiv.org/pdf/0907.3434)). Why it matters: Boids became statistical physics with an order parameter, a control parameter and a phase diagram, the template for "tune one knob, cross a transition".

### 2.6 Schelling segregation (1971)

Rules: two agent types on a grid; an agent moves to an empty cell if fewer than a threshold fraction of neighbours share its type. Schelling (J. Math. Sociology 1:143–186, 1971) showed mild preferences against being a small minority produce near-complete segregation: "no simple correspondence of individual incentive to collective results" ([Schelling 1971](https://uzh.ch/cmsssl/suz/dam/jcr:00000000-68cb-72db-ffff-ffffff8071db/04.02%7B_%7Dschelling%7B_%7D71.pdf); [Grauwin et al. 2009](https://arxiv.org/pdf/0907.1777)). Pancs and Vriend (2003) found segregation even when every agent strictly prefers integration ([QMUL](https://qmul.ac.uk/sef/research/workingpapers/2003/items/487.html)). Why it matters: macro outcomes can contradict micro intentions, the failure mode to watch for in multi-agent AI.

### 2.7 Sugarscape (1996)

Rules: agents with heterogeneous vision and metabolism on a grid with two sugar peaks; "look as far as you can, move to the richest cell, eat". Epstein and Axtell then added reproduction, culture, combat, trade and disease. Skewed wealth distributions appear from vision and metabolism heterogeneity alone; migration, trade and cultural groups follow ([Brookings](https://www.brookings.edu/book/growing-artificial-societies/); [JASSS appendix](https://jasss.org/12/1/6/appendixB/EpsteinAxtell1996.html); [MIT Technology Review, 2007](https://www.technologyreview.com/2007/07/01/224767/artificial-societies-and-virtual-violence/amp/)). Why it matters: it set the "generative" standard: if you did not grow it, you did not explain it.

### 2.8 Axelrod's cooperation tournaments (1984)

Rules: submitted programs play a 200-round iterated Prisoner's Dilemma against every other entry. Rapoport's Tit-for-Tat, the simplest of fourteen entries, won both tournaments, and "nice" strategies dominated Axelrod's ecological follow-up ([Wikipedia](https://en.wikipedia.org/wiki/The_Evolution_of_Cooperation)); later work questions how far this generalises ([Rapoport, Seale & Colman 2015](https://doaj.org/article/6c213202b8324e8c98beaea09479c89e)). Why it matters: cooperation emerges among self-interested agents through repetition and reciprocity, without altruism or central enforcement.

### 2.9 Ant colony models and stigmergy (1989–1990)

Deneubourg and colleagues connected an Argentine ant nest to food by a double bridge. With equal branches, fluctuations plus pheromone reinforcement make the colony converge on one (about 50/50 across trials); with unequal branches (Goss et al. 1989) it converges on the shorter one. A minimal trail-laying/following model reproduces this, and Dorigo's Ant Colony Optimization was inspired by it ([Deneubourg et al. 1990](https://www.doi.org/10.1007/BF01417909); [Dorigo et al. 1999](https://staff.washington.edu/paymana/swarm/dorigo99-al.pdf); [ACO chapter](https://www.cs.princeton.edu/courses/archive/fall24/cos597C/bib2/Ant_colony_optimization.pdf)). Why it matters: positive feedback through a shared medium performs distributed optimisation; the canonical stigmergy result.

### 2.10 Lenia and continuous CA (2019)

Chan's Lenia generalises Life to continuous space, time and state: a smooth ring kernel computes a neighbourhood potential, a bell-shaped growth function maps it to a growth rate, and the state is incremented by a small time step. The paper reports over 400 self-sustaining "species" in 18 families, many found by interactive evolution, that are geometric, metameric, fuzzy, resilient and adaptive ([Chan 2019, arXiv](https://arxiv.org/abs/1812.05433v2); [Complex Systems 28(3)](https://www.complex-systems.com/abstracts/v28_i03_a01/)). The best-known creature, Orbium, uses a Gaussian kernel (μ=0.5, σ=0.15) and growth function (μ=0.15, σ=0.015) ([arXiv 2401.13111](https://arxiv.org/pdf/2401.13111)). Why it matters: lifelike solitons in a differentiable, parameterised rule space you can search with gradients or evolution.

### 2.11 Flow-Lenia (2023)

Plantec et al. fix two Lenia problems: creatures occupy a tiny region of parameter space, and mass is not conserved. Flow-Lenia conserves activation per channel by moving "matter" along an affinity gradient (plus diffusion) and makes rule parameters local, carried with the matter, so regions run different rules and multi-species dynamics emerge (ALIFE 2023, [arXiv 2212.07906](https://arxiv.org/abs/2212.07906)). Why it matters: a step toward open-ended evolution inside a CA, with the "genome" part of the substrate.

### 2.12 Neural cellular automata (2020)

Mordvintsev, Randazzo, Niklasson and Levin trained a CA whose update rule is a small neural network (Distill 2020, DOI 10.23915/distill.00023). Each cell holds 16 channels (RGBA plus 12 hidden); a cell is alive if any 3x3 neighbour has alpha above 0.1; updates are residual and applied stochastically; perception uses fixed gradient filters (Sobel-type, unverified from the primary page). Training from a single seed toward a target image, with a persistent sample pool and random damage, yields rules that grow, stabilise and regenerate the pattern ([ML Anthology](https://mlanthology.org/distill/2020/mordvintsev2020distill-growing); [arXiv 2607.12403](https://arxiv.org/pdf/2607.12403); [Distill thread](https://distill.pub/2020/selforg/)). Why it matters: it inverts the field. Instead of hand-picking rules and hoping, you specify the macro outcome and optimise the micro rule; robustness and regeneration arrive as side effects of the training distribution.

## 3. The ABM toolbox today

### 3.1 Agent-based modelling frameworks

| Tool | Language | Scale | Verdict: use it when |
|---|---|---|---|
| [NetLogo](https://docs.netlogo.org/whatis) 7.0.x | Logo dialect | Thousands, interactive | Prototyping, teaching, *seeing* a model in an afternoon; Models Library has most canonical models ([docs](https://docs.netlogo.org/)). |
| [Mesa](https://mesa.readthedocs.io/) 3 | Python | Up to ~10^5 | You live in the Python data stack; Solara visualisation still maturing ([JOSS 2025](https://summary.ecosyste.ms/projects/356257); [PyPI](https://pypi.org/pypi/Mesa/)). |
| [Agents.jl](https://github.com/JuliaDynamics/ABMFrameworksComparison) | Julia | Fastest of the classics in vendor-run benchmarks (Mesa 20–170x slower on flocking) | CPU speed without GPUs and you accept Julia ([Datseris et al.](https://arxiv.org/pdf/2101.10072)). |
| [MASON](https://journals.sagepub.com/doi/ref/10.1177/0037549706073695) | Java | Fast discrete-event core; last release v20 (2019) | Lean Java engine, no modern GUI needed ([comparison](https://en.wikipedia.org/wiki/Comparison_of_agent-based_modeling_software)). |
| [Repast Simphony / Repast4Py](https://pypi.org/project/repast4py) | Java / Python+MPI | Multi-node distributed | HPC-scale ABM from Python; Repast HPC (C++) for specialists ([Collier & Ozik 2022](https://informs-sim.org/wsc22papers/017.pdf)). |
| [FLAME GPU 2](https://github.com/FLAMEGPU/FLAMEGPU2) | CUDA C++ / Python | Millions per GPU | Raw throughput on homogeneous populations ([Richmond et al. 2023](https://eprints.whiterose.ac.uk/199416/)). |
| [AgentTorch](https://neurips.cc/virtual/2023/79209) | PyTorch | 8.4M-agent NYC model; 600x sim, 3000x calibration speedups claimed | Gradients through the simulation for calibration, or LLM agent archetypes at population scale ([arXiv 2507.09901](https://arxiv.org/pdf/2507.09901); [bdtechtalks 2024](https://bdtechtalks.com/2024/10/02/agenttorch-llm-agents/)). |

### 3.2 Simulation and RL environments relevant to emergence

| Environment | What it is | Verdict: use it when |
|---|---|---|
| [PettingZoo](https://proceedings.neurips.cc/paper/2021/hash/803f7c4c3ff61b71be53a0c803bfb57f-Abstract.html) (NeurIPS 2021) | Gym-style multi-agent API (AEC and parallel) | Standard interface for any multi-agent environment; plumbing, not science. |
| [Melting Pot 2.0](https://arxiv.org/pdf/2211.13746) (2023) | 50+ substrates, 256+ scenarios pairing a substrate with a fixed background population, mostly mixed-motive | Testing whether learned social behaviour generalises to unfamiliar co-players ([Leibo et al. 2021](https://proceedings.mlr.press/v139/leibo21a.html); [GitHub](https://github.com/google-deepmind/meltingpot/blob/main/README.md)). |
| [Neural MMO 2.0](https://proceedings.neurips.cc/paper_files/paper/2023/hash/9ca22870ae0ba55ee50ce3e2d269e5de-Abstract.html) (NeurIPS 2023) | Procedural maps, 128 agents standard (1–1024), task system | Emergent economies, territory and specialisation in a persistent open world. |
| [JaxMARL](https://proceedings.neurips.cc/paper_files/paper/2024/hash/5aee125f052c90e326dcf6f380df94f6-Abstract.html) (NeurIPS 2024) | MARL environments and baselines in JAX; up to 12,500x wall-clock speedup | Thousands of multi-agent runs on one GPU, e.g. sweeps over social dilemmas. |
| [Craftax](https://proceedings.mlr.press/v235/matthews24a.html) (ICML 2024) | JAX Crafter plus NetHack elements; 1B steps in under an hour on one GPU | Open-ended skill acquisition at speed; multi-agent variant in 2025 ([arXiv 2511.04904](https://arxiv.org/pdf/2511.04904)). |

### 3.3 Documenting, validating and calibrating

**ODD protocol.** Grimm et al. introduced ODD (Overview, Design concepts, Details) in 2006 to fix incomplete model descriptions, updating it in 2010 and 2020 (JASSS 23(2)7). Design concepts include basic principles, emergence, adaptation, objectives, learning, sensing, interaction, stochasticity, collectives and observation ([Grimm et al. 2020](https://www.jasss.org/23/2/7.html); [Polhill 2010](https://jasss.soc.surrey.ac.uk/13/4/9/9.pdf)). The "Emergence" concept forces you to state which outcomes are imposed by rules and which are meant to emerge.

**Pattern-oriented modelling.** Grimm et al. (Science 310:987, 2005) argue that fitting one pattern under-constrains an ABM; reproducing several observed patterns at different scales filters out wrong structures and narrows parameters ([USGS record](https://pubs.usgs.gov/publication/70161783); [Wikipedia](https://en.wikipedia.org/wiki/Pattern-oriented_modeling)).

**Sensitivity analysis.** ten Broeke, van Voorn and Ligtenberg (JASSS 19(1)5, 2016) compared extended one-factor-at-a-time (OFAT), regression-based variance decomposition and Sobol' indices and found none complete; they recommend extended OFAT first because it exposes tipping points and regime shifts that global variance methods average away ([ten Broeke et al. 2016](https://www.jasss.org/19/1/5/5.pdf)). Choose the method by model purpose ([Ligmann-Zielinska et al. 2020](https://www.jasss.org/23/1/6.html)), and use surrogate models when the ABM is too slow for Sobol' sampling ([JASSS 2021](https://www.jasss.org/24/2/3.html)).

**Checklist.** Many stochastic replicates per parameter point (emergent outcomes are distributions). Report transient length separately from steady state (Langton's ant). Sweep the control parameter across the suspected transition (Vicsek). Test robustness to agent removal and noise. Match multiple patterns, not one statistic.

## 4. Measuring emergence

Honest summary first: there is no agreed scalar "emergence meter". The theoretically motivated measures are either intractable beyond toy sizes or require full knowledge of the system's transition probabilities. The practical measures are proxies. Both are listed.

### 4.1 Information-theoretic measures

**Statistical complexity (Crutchfield and Shalizi).** Computational mechanics builds the minimal predictive model (ε-machine) of a process; the entropy of its causal states is the information needed for optimal prediction ([Shalizi & Crutchfield 2001](https://csc.ucdavis.edu/~cmg/compmech/pubs/cmppss.htm)). Shalizi et al. (2004) define self-organisation as an internally generated increase in this quantity and introduce a *local* version (predict each cell's future light cone from its past light cone) that automatically highlights particles and domain walls in CA as high-complexity regions ([Shalizi et al. 2004](https://arxiv.org/abs/nlin/0409024v1); [2026 review](https://arxiv.org/pdf/2604.00273)). Usability: good for spatially extended discrete systems with ample data; expensive but done at CA scale.

**Causal emergence (Hoel).** Hoel, Albantakis and Tononi (PNAS 2013) compare effective information (EI) of a system's causal structure at micro and coarse-grained scales; when macro rules are more deterministic and less degenerate, EI is higher at the macro level even though it supervenes on the micro ([Hoel et al. 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3856819); [Hoel 2017](https://arxiv.org/pdf/1612.09592)). Critics call this epistemic, not ontological ([Dewhurst 2020](https://philsci-archive.pitt.edu/17043)). Usability: needs the full transition matrix and a search over coarse-grainings; feasible only for small discrete models.

**Information-decomposition emergence (Rosas et al.).** Rosas, Mediano et al. (PLoS Comp. Biol. 2020) use Partial Information Decomposition to define causal emergence without choosing a coarse-graining, with quantitative definitions of downward causation and "causal decoupling" and sufficiency criteria computable from data via mutual information alone; they find particle collisions emergent in the Game of Life and apply the method to Boids and ECoG ([Rosas et al. 2020](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7833221/); [arXiv](https://arxiv.org/pdf/2004.08220)). Usability: the most practical principled measure; works on macro/micro time series, but can miss emergence (false negatives).

**Integrated information (Φ).** PyPhi (Mayner et al. 2018) runs in roughly O(n·53^n) for n binary elements; practical limit about 10–12 elements, with a seven-node chain taking 2.75 hours ([PyPhi, arXiv 1712.09644](https://arxiv.org/pdf/1712.09644); [Entropy 2019](https://www.mdpi.com/1099-4300/21/5/525/htm)). Usability: not usable at engineering scale.

**Effective complexity (Gell-Mann and Lloyd 1996).** Algorithmic information content of an object's *regularities* alone; low for both order and randomness, peaking in between ([Ay, Müller & Szkoła](https://ar5iv.arxiv.org/html/0810.5663); [Measuring complexity, arXiv 1909.13243](https://arxiv.org/pdf/1909.13243)). Usability: uncomputable and observer-dependent; a concept, not a metric.

### 4.2 Practical proxies engineers use

| Proxy | Detects | Caveat |
|---|---|---|
| Order parameter (polarisation, cluster size, Gini) | Transitions under a control-parameter sweep | You must know which macro variable to watch |
| Variance peak, critical slowing down | Proximity to a transition | Needs many replicates near the critical point |
| Power-law event sizes | Possible criticality | Many non-critical mechanisms give power laws; fit properly |
| Mutual information / transfer entropy between agents | Coordination, information flow | Pairwise; misses higher-order structure |
| Compressibility of macro vs micro trajectory | Weak emergence (non-derivable but compressible) | Compressor-dependent |
| Ablation (remove agents, add noise) | Whether the pattern is a stable attractor | Cheap; always run it |
| Predictability gain of a coarse-grained model | Causal emergence (Hoel, Rosas) | Depends on candidate coarse-grainings |
| Surprise vs a no-interaction baseline | "Not simple aggregation" | Baseline choice does the work |

The most defensible combination: an order parameter with a control-parameter sweep, an ablation, and a no-interaction baseline; add Rosas-style decomposition when you need a principled claim.

## 5. Key takeaways for AI practitioners

1. You will only ever engineer weak emergence: macro behaviour derivable from your code but only by running it. Make simulation, replicates and sweeps first-class parts of development.
2. "Emergent" is not "surprising". Use the checklist: macro property, not a simple aggregate, coherent over time, decentralised, robust to ablation, ideally better predicted by a coarse model than by the micro model.
3. Local rules plus feedback through a shared medium (stigmergy) is the most reliable recipe for collective behaviour; shared memory, queues and vector stores are stigmergic channels in AI agent systems.
4. Macro outcomes can contradict micro intent (Schelling). Evaluate multi-agent AI at the population level, not only per agent.
5. Transients can be long and deceptive (Langton's ant: ~10,000 chaotic steps before order). Run longer than feels necessary and report transient length.
6. Interesting behaviour clusters near transitions (Class 4, Vicsek's critical noise), but the "edge of chaos" as a universal design law did not survive replication. Use it as a heuristic for where to search.
7. Neural CA and differentiable ABMs show emergence can be a training objective: specify the macro target, optimise the micro rule, and get robustness as a side effect. This is the most transferable idea for AI systems.
8. Tooling: NetLogo to think, Mesa or Agents.jl to build, FLAME GPU or AgentTorch to scale, JaxMARL/Craftax for fast RL sweeps, Melting Pot for social generalisation. Document with ODD, validate against multiple patterns, run sensitivity analysis before trusting any emergent result.
9. Measurement is the weak spot. Φ and effective complexity are unusable at scale; Hoel's EI needs full transition tables; Rosas's decomposition and Shalizi's local complexity are the usable principled options. Most projects will rely on order parameters, ablations and baselines, so choose and state them explicitly.

## Sources

- Anderson, P. W. (1972). More Is Different. Science 177(4047):393–396. https://www.mit.edu/~kardar/research/seminars/EPB/PWA-Science72.pdf
- Chalmers, D. (2006). Varieties of Emergence. https://consc.net/papers/granada.html
- Bedau's weak emergence definition as quoted in JASSS 13(1)9 (2010). https://www.jasss.org/13/1/9.html
- De Wolf & Holvoet (2005) definition as cited in "Organization of Multi-Agent Systems: An Overview" (arXiv 2015). https://arxiv.org/pdf/1506.09032
- Goldstein (1999) criteria as cited in "Emergence: from physics to biology, sociology, and computer science" (arXiv 2025). https://arxiv.org/pdf/2508.08548
- Holland, *Hidden Order* (1995), Leonardo review. https://www.leonardo.info/reviews_archive/pre2000/malinahidden.html
- Holland, *Hidden Order* (1995), reason.com review (1996). https://reason.com/1996/12/01/learning-curve
- University of Michigan obituary for John Holland (2015). https://record.umich.edu/?p=37703
- Shalizi, C. R. PhD thesis (2001), Causal Architecture, Complexity and Self-Organization. https://www.bactra.org/thesis
- Theraulaz & Bonabeau (1999). A Brief History of Stigmergy. https://apice.unibo.it/xwiki/bin/view/Publication/StigmergyhistoryArtificiallife5
- Holland & Melhuish (1999). Stigmergy, self-organization, and sorting in collective robotics. https://cse-robotics.engr.tamu.edu/dshell/cs689/papers/holland99stigmergy.pdf
- Langton (1990) as summarised in "Dynamical criticality: overview and open questions" (arXiv 2015). https://arxiv.org/pdf/1512.05259
- Wikipedia: Christopher Langton. https://en.wikipedia.org/wiki/Christopher_Langton
- Bak, Tang & Wiesenfeld (1987). Self-Organized Criticality. PRL 59:381. https://courses.physics.ucsd.edu/2016/Spring/physics235/BTW-PRL.pdf
- Mitchell, Crutchfield & Hraber (1993). Dynamics, Computation, and the "Edge of Chaos": A Re-Examination. https://arxiv.org/pdf/adap-org/9306003
- Frontiers in Systems Neuroscience (2021) on brain criticality. https://www.frontiersin.org/journals/systems-neuroscience/articles/10.3389/fnsys.2021.709677/pdf
- A Critical Assessment of the Brain Criticality Hypothesis (arXiv 2026). https://arxiv.org/pdf/2604.21071
- NDPR review: Philosophical and Scientific Perspectives on Downward Causation. https://ndpr.nd.edu/news/philosophical-and-scientific-perspectives-on-downward-causation/
- The Downward Causation Argument against Emergentism (Kairos). https://kairos.campus.ciencias.ulisboa.pt/wp-content/uploads/sites/17/2023/04/The-Downward-Causation-Argument-against-Emergentism.pdf
- LifeWiki: Conway's Game of Life. https://conwaylife.com/wiki/Conway's_Game_of_Life
- LifeWiki: Turing Machine Universality of the Game of Life. https://conwaylife.com/wiki/Turing_Machine_Universality_of_the_Game_of_Life
- Rendell, P. Turing Machine Universality of the Game of Life (UWE thesis / Springer 2015). https://uwe-repository.worktribe.com/output/822575
- Wolfram (1984) classes, Eppstein summary. https://www.ics.uci.edu/%7eeppstein/ca/wolfram.html
- Universal Cellular Automata and Class 4 (arXiv 1994). https://arxiv.org/pdf/cond-mat/9409080
- Cook (2004). Universality in Elementary Cellular Automata. Complex Systems. https://complex-systems.com/?p=2418
- Wikipedia: Rule 110. https://en.wikipedia.org/wiki/Rule_110
- Wikipedia: Langton's ant. https://en.wikipedia.org/wiki/Langton%27s_ant
- Gajardo, Moreira & Goles (2002). Complexity of Langton's Ant. https://arxiv.org/pdf/nlin/0306022
- Langton (1986). Studying artificial life with cellular automata. Physica D 22. https://deepblue.lib.umich.edu/items/76966fa1-6b4e-498c-bbfc-2b884c2a5245
- Wikipedia: Boids. https://en.wikipedia.org/wiki/Boids
- Ohio State computer graphics history, Reynolds' Boids. https://ohiostate.pressbooks.pub/graphicshistory/?p=280
- Vicsek et al. (1995). Novel type of phase transition in a system of self-driven particles. https://arxiv.org/pdf/cond-mat/0611743
- Phase transitions in swarming systems: a recent debate (arXiv 2009). https://arxiv.org/pdf/0907.3434
- Schelling (1971). Dynamic Models of Segregation. https://uzh.ch/cmsssl/suz/dam/jcr:00000000-68cb-72db-ffff-ffffff8071db/04.02%7B_%7Dschelling%7B_%7D71.pdf
- Grauwin et al. (2009). Dynamic models of residential segregation: review. https://arxiv.org/pdf/0907.1777
- Pancs & Vriend (2003). Schelling's spatial proximity model revisited. https://qmul.ac.uk/sef/research/workingpapers/2003/items/487.html
- Brookings: Growing Artificial Societies (1996). https://www.brookings.edu/book/growing-artificial-societies/
- JASSS appendix: Epstein and Axtell's Sugarscape. https://jasss.org/12/1/6/appendixB/EpsteinAxtell1996.html
- MIT Technology Review (2007). Artificial Societies and Virtual Violence. https://www.technologyreview.com/2007/07/01/224767/artificial-societies-and-virtual-violence/amp/
- Wikipedia: The Evolution of Cooperation. https://en.wikipedia.org/wiki/The_Evolution_of_Cooperation
- Rapoport, Seale & Colman (2015). PLoS ONE. https://doaj.org/article/6c213202b8324e8c98beaea09479c89e
- Deneubourg, Aron, Goss & Pasteels (1990). J. Insect Behavior 3:159–168. https://www.doi.org/10.1007/BF01417909
- Dorigo, Di Caro & Gambardella (1999). Ant Algorithms for Discrete Optimization. https://staff.washington.edu/paymana/swarm/dorigo99-al.pdf
- Dorigo & Stützle, Ant Colony Optimization chapter. https://www.cs.princeton.edu/courses/archive/fall24/cos597C/bib2/Ant_colony_optimization.pdf
- Chan (2019). Lenia: Biology of Artificial Life. arXiv 1812.05433. https://arxiv.org/abs/1812.05433v2
- Chan (2019). Complex Systems 28(3). https://www.complex-systems.com/abstracts/v28_i03_a01/
- Discretization-Dependent Dissolution of Gliders (arXiv 2024), Orbium parameters. https://arxiv.org/pdf/2401.13111
- Plantec et al. (2023). Flow-Lenia. arXiv 2212.07906. https://arxiv.org/abs/2212.07906
- Mordvintsev et al. (2020). Growing Neural Cellular Automata, ML Anthology entry. https://mlanthology.org/distill/2020/mordvintsev2020distill-growing
- Distill thread: Differentiable Self-organizing Systems (2020). https://distill.pub/2020/selforg/
- Structured Fluctuations ... in Growing NCA (arXiv 2026), describing the NCA setup. https://arxiv.org/pdf/2607.12403
- NetLogo 7 documentation, What is NetLogo. https://docs.netlogo.org/whatis
- NetLogo documentation home. https://docs.netlogo.org/
- Mesa documentation. https://mesa.readthedocs.io/
- Mesa 3 JOSS paper (2025) listing. https://summary.ecosyste.ms/projects/356257
- Mesa on PyPI. https://pypi.org/pypi/Mesa/
- Datseris et al. Agents.jl (arXiv 2101.10072). https://arxiv.org/pdf/2101.10072
- JuliaDynamics ABM framework comparison. https://github.com/JuliaDynamics/ABMFrameworksComparison
- Luke et al. (2005). MASON. Simulation 81. https://journals.sagepub.com/doi/ref/10.1177/0037549706073695
- Wikipedia: Comparison of agent-based modeling software. https://en.wikipedia.org/wiki/Comparison_of_agent-based_modeling_software
- Collier & Ozik (2022). Distributed Agent-Based Simulation with Repast4Py. WSC 2022. https://informs-sim.org/wsc22papers/017.pdf
- Repast4Py on PyPI. https://pypi.org/project/repast4py
- Richmond et al. (2023). FLAME GPU 2. Software: Practice and Experience 53(8). https://eprints.whiterose.ac.uk/199416/
- FLAME GPU 2 GitHub. https://github.com/FLAMEGPU/FLAMEGPU2
- AgentTorch (NeurIPS 2023 workshop). https://neurips.cc/virtual/2023/79209
- Large Population Models (arXiv 2507.09901, 2025). https://arxiv.org/pdf/2507.09901
- bdtechtalks (2024). Simulating millions of LLM agents with AgentTorch. https://bdtechtalks.com/2024/10/02/agenttorch-llm-agents/
- Terry et al. (2021). PettingZoo. NeurIPS. https://proceedings.neurips.cc/paper/2021/hash/803f7c4c3ff61b71be53a0c803bfb57f-Abstract.html
- Leibo et al. (2021). Scalable Evaluation of MARL with Melting Pot. ICML. https://proceedings.mlr.press/v139/leibo21a.html
- Agapiou et al. (2023). Melting Pot 2.0. arXiv 2211.13746. https://arxiv.org/pdf/2211.13746
- Melting Pot GitHub README. https://github.com/google-deepmind/meltingpot/blob/main/README.md
- Suarez et al. (2023). Neural MMO 2.0. NeurIPS Datasets and Benchmarks. https://proceedings.neurips.cc/paper_files/paper/2023/hash/9ca22870ae0ba55ee50ce3e2d269e5de-Abstract.html
- Rutherford et al. (2024). JaxMARL. NeurIPS Datasets and Benchmarks. https://proceedings.neurips.cc/paper_files/paper/2024/hash/5aee125f052c90e326dcf6f380df94f6-Abstract.html
- Matthews et al. (2024). Craftax. ICML, PMLR 235. https://proceedings.mlr.press/v235/matthews24a.html
- Multi-Agent Craftax (arXiv 2511.04904, 2025). https://arxiv.org/pdf/2511.04904
- Grimm et al. (2020). The ODD Protocol: A Second Update. JASSS 23(2)7. https://www.jasss.org/23/2/7.html
- Polhill (2010). ODD updated. JASSS 13(4)9. https://jasss.soc.surrey.ac.uk/13/4/9/9.pdf
- Grimm et al. (2005). Pattern-oriented modeling of agent-based complex systems. Science 310. https://pubs.usgs.gov/publication/70161783
- Wikipedia: Pattern-oriented modeling. https://en.wikipedia.org/wiki/Pattern-oriented_modeling
- ten Broeke, van Voorn & Ligtenberg (2016). Which Sensitivity Analysis Method Should I Use for My Agent-Based Model? JASSS 19(1)5. https://www.jasss.org/19/1/5/5.pdf
- Ligmann-Zielinska et al. (2020). JASSS 23(1)6. https://www.jasss.org/23/1/6.html
- ten Broeke et al. (2021). Surrogate models for ABM sensitivity analysis. JASSS 24(2)3. https://www.jasss.org/24/2/3.html
- Shalizi & Crutchfield (2001). Computational Mechanics: Pattern and Prediction, Structure and Simplicity. https://csc.ucdavis.edu/~cmg/compmech/pubs/cmppss.htm
- Shalizi, Shalizi & Haslinger (2004). Quantifying Self-Organization with Optimal Predictors. arXiv nlin/0409024. https://arxiv.org/abs/nlin/0409024v1
- How local rules generate emergent structure in cellular automata (arXiv 2026). https://arxiv.org/pdf/2604.00273
- Hoel, Albantakis & Tononi (2013). Quantifying causal emergence shows that macro can beat micro. PNAS. https://pmc.ncbi.nlm.nih.gov/articles/PMC3856819
- Hoel (2017). When the Map Is Better Than the Territory. arXiv 1612.09592. https://arxiv.org/pdf/1612.09592
- Dewhurst (2020). Causal Emergence and Real Patterns. https://philsci-archive.pitt.edu/17043
- Rosas et al. (2020). Reconciling emergences. PLoS Comp. Biol. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7833221/
- Rosas et al. (2020) arXiv version. https://arxiv.org/pdf/2004.08220
- Mayner et al. (2018). PyPhi: A toolbox for integrated information theory. arXiv 1712.09644. https://arxiv.org/pdf/1712.09644
- Entropy 21(5):525 (2019) on IIT 3.0 practical limits. https://www.mdpi.com/1099-4300/21/5/525/htm
- Ay, Müller & Szkoła. Effective Complexity and its Relation to Logical Depth. arXiv 0810.5663. https://ar5iv.arxiv.org/html/0810.5663
- Measuring complexity (arXiv 1909.13243). https://arxiv.org/pdf/1909.13243
