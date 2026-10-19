# Proven practical applications of emergent systems and simulations

This chapter answers one question: where has emergent behaviour (many simple agents, local rules, indirect feedback) been put to work *for real*, and what did it deliver? The bar is deliberately high. A paper demo does not count as "proven"; a deployment or a validation against real outcomes does.

**Evidence grades used throughout**

| Grade | Meaning |
|---|---|
| **A** | Deployed in production (industry or government) with reported, attributable results |
| **B** | Validated against real-world data, or run as a field trial / pilot with measured outcomes |
| **C** | Strong research result only (simulation, lab, benchmark) |

Two framing notes before the survey:

1. **"Emergent" is a property of the mechanism, not of the marketing.** Several famous "swarm" deployments turn out to be centrally planned systems with a swarm vocabulary. The chapter calls these out, because for an engineer the distinction decides what you can copy.
2. **Simulation of emergence and control by emergence are different products.** An agent-based model (ABM) that predicts how a crowd or an epidemic will behave is "proven" when its predictions match reality. A self-organising controller (traffic lights, gossip protocols) is "proven" when the live system performs. Both appear here, graded on their own terms.

---

## 1. Swarm intelligence in optimisation

### 1.1 Ant Colony Optimisation (ACO) in telecom routing

**Mechanism.** Mobile agents ("ants") traverse the network, deposit a virtual pheromone on the routing tables of nodes they pass, and later ants probabilistically prefer high-pheromone next hops; pheromone evaporates. Good routes emerge from reinforcement without any node knowing the global topology.

**What is documented.** Schoonderwoerd, Holland, Bruten and Rothkrantz, *Ant-based load balancing in telecommunications networks* (Adaptive Behavior 5, 1996/97), simulated a circuit-switched network with a topology modelled on British Telecom's and reported fewer call failures than fixed shortest-path routing and an agent-based alternative ([Springer record](https://link.springer.com/doi/10.1007/bfb0053944); [course copy of the paper](https://www.rose-hulman.edu/class/cs/csse453/schedule/day4/LoadBalancing.pdf)). Di Caro and Dorigo's **AntNet** (JAIR 1998) extended the idea to packet-switched networks and, in simulation, outperformed OSPF, SPF, distributed Bellman-Ford and Q-routing on throughput and delay ([JAIR paper](https://staff.washington.edu/paymana/swarm/dicaro98-jair.pdf); [arXiv copy](https://arxiv.org/pdf/1105.5449)).

**What is folklore.** Both studies were simulations. The chapter found no evidence that BT or any operator put ant routing into a live network, and the often-repeated "HP Labs" affiliation for the Schoonderwoerd work could not be confirmed from the sources retrieved **(unverified)**. Ant routing's lasting influence is on the research lineage (MANET routing, later AI network-management work), not on deployed Internet routing, which remained OSPF/BGP.

**Grade: C.**

### 1.2 ACO in logistics: IDSIA / AntOptima

**Mechanism.** Ant Colony System for vehicle routing with time windows, pickup-and-delivery and dynamic order arrival: artificial ants build candidate routes guided by pheromone laid on good arcs; the colony converges to high-quality schedules in minutes.

**What is documented.** Gambardella's group at IDSIA (Lugano) published industrial applications: a VRP with time windows for "a major Swiss supermarket chain", a pickup-and-delivery problem for an Italian distributor, time-dependent freight routing in Padua, and on-line routing in Lugano where orders arrive during delivery (Montemanni et al., *J. Combinatorial Optimization* 2005; Rizzoli et al. review 2007) ([Gambardella STRC 2002](https://www.strc.ch/2002/gambardella.pdf); [Montemanni et al. 2005](https://ideas.repec.org/a/spr/jcomop/v10y2005i4d10.1007_s10878-005-4922-6.html); [USI record of the 2007 review](https://search.usi.ch/it/pubblicazioni/2709/ant-colony-optimization-for-real-world-vehicle-routing-problems)). The spin-off **AntOptima** sold this as *AntRoute*, described in trade press as processing thousands of daily orders in minutes under fleet, time-window and load constraints ([LogForum 2006](https://www.logforum.net/vol2/issue3/no4/2_3_4_06.html)).

**What is folklore.** The named clients commonly cited for AntOptima — **Migros, Barilla** — are not confirmed in any primary source retrieved; the Swiss supermarket chain is plausibly Migros but is unnamed in the papers **(unverified)**. **Air Liquide** is reported by a 2002 secondary account to have used ant-style agent simulation so that "one analyst in two hours" replaced "a team for half a day" on delivery scheduling, but the chapter could not reach a primary source ([interconnected.org 2002](https://interconnected.org/home/2002/11/20/the_french_company)) **(unverified)**.

**Grade: B** for the IDSIA industrial cases (real data, real companies, published results); **A (unverified)** for the commercial AntRoute installations.

### 1.3 The Southwest Airlines cargo story: verify before you quote

The canonical anecdote (ants → Southwest cargo routing → millions saved) traces to Bonabeau & Meyer, *Swarm Intelligence: A Whole New Way to Think About Business*, Harvard Business Review, May 2001 ([summary](https://maaw.info/ArticleSummaries/ArtSumBonabeauMeyer2001.htm)). The concrete numbers in circulation come from a 2003 Bonabeau slide deck: "71% improvement, at least $10m/yr" ([Bonabeau ETCON 2003 slides](https://staff.washington.edu/paymana/swarm/bonabeau03-etcon.pdf)); a contemporaneous conference note records "$10 million per month" instead ([ETCON notes](https://interconnected.org/notes/2003/04/etcon/swarm.txt)). The two figures disagree by 12×, and neither is from Southwest. A **separate** Southwest project, analyst Doug Lawson's ant-inspired boarding simulation, is often conflated with the cargo work ([The Smart Swarm excerpt](https://missiontolearn.com/book-excerpts/smart-swarm/); [Gadling 2008](https://gadling.com/?p=11028)).

**Verdict:** a real consulting engagement, popularised by its consultant, with no independent reporting of outcomes. **Grade: C (unverified A).**

### 1.4 Particle Swarm Optimisation and bee algorithms

PSO is ubiquitous in engineering optimisation papers, but deployed, outcome-reported industrial uses are rarer than its citation count suggests. Documented cases found: an embedded PSO solver inside a commercial digital inspection microscope that removes the need to return units to the factory for calibration (Applied Sciences 2022, [DOAJ record](https://doaj.org/article/03190b32eb5f42ba83666376e1dc035d)); PSO for exact optimal experimental designs shown to match coordinate-exchange at low cost ([Walsh & Borkowski 2022](https://arxiv.org/pdf/2206.06940)); and simulation studies in refinery energy allocation and manufacturing cell formation ([UJ record](https://pure.uj.ac.za/en/publications/particle-swarm-optimisation-algorithm-based-renewable-energy-sour/); [IJSOMA 2012](https://ideas.repec.org/a/ids/ijsoma/v13y2012i4p441-456.html)). **Grade: B** for the embedded product, otherwise **C**.

For bee-inspired methods, the best-documented case is Nakrani & Tovey's honeybee server-allocation algorithm (2004): servers are recruited to websites by "waggle-dance" advertisements proportional to revenue; on real traffic traces it beat greedy allocation by 4–25% under volatile load but lost under uniform load ([Georgia Tech](https://hg.gatech.edu/node/59987); [Cornell / Golden Goose 2016](https://news.cornell.edu/node/286521)). Production use is claimed ("at least one major company") but unnamed **(unverified)**. **Grade: C/B.**

### 1.5 Summary: well-documented vs folklore

| Claim | Status |
|---|---|
| Ant routing beats shortest-path in simulation (BT topology, AntNet) | Well documented (C) |
| Ant routing deployed in a live carrier network | No evidence found |
| ACO vehicle routing applied to real Swiss/Italian distributors (IDSIA) | Well documented (B) |
| AntOptima clients Migros / Barilla | Unverified |
| Air Liquide ant-based scheduling | Secondary source only, unverified |
| Southwest cargo "$10M saved" | Consultant slide, figures inconsistent, unverified |
| Honeybee server allocation beats greedy on real traces | Documented (C), production use unverified |

---

## 2. Swarm robotics and logistics

### 2.1 Amazon / Kiva: what is actually emergent

Amazon reports more than 750,000 robots across its network (2023, repeated 2025) ([Amazon 2023](https://aboutamazon.com/news/operations/amazon-introduces-new-robotics-solutions); [Distribution Strategy 2025](https://distributionstrategy.com/2025/06/amazon-reaches-750000-robots-in-fulfillment-operations/)). This is the largest mobile-robot fleet in existence, and it is frequently described as a "swarm". Precision matters here.

The founding paper, Wurman, D'Andrea & Mountz, *Coordinating Hundreds of Cooperative, Autonomous Vehicles in Warehouses* (AI Magazine 2008), frames the system as a multi-agent resource-allocation and path-planning problem with installations of 500+ vehicles ([AI Magazine](https://ojs.aaai.org/index.php/aimagazine/article/view/2082)). D'Andrea's later description is of a **hierarchical** control layer "similar to that used in air traffic control", with drive units sharing local sensing ([D'Andrea chapter](https://IEEECSS.org/sites/ieeecss/files/2019-06/IoCT2-SS-DAndrea-1.pdf)); the subsequent academic literature treats Kiva-style warehouses as a *centralised* target-assignment-and-path-finding (TAPF/MAPF) problem solved by planners such as Conflict-Based Search ([Ma & Koenig 2016](https://arxiv.org/pdf/1612.05693)).

**Verdict.** Task allocation, path reservation and pod placement are centrally computed; individual robots execute reserved paths with local obstacle handling. What is emergent is the *inventory layout*: pods drift towards stations in proportion to demand because frequently requested pods are returned to nearby free slots, producing a self-organising "hot zone" without an explicit layout optimiser (described qualitatively in the 2008 paper; detailed internals could not be fetched in this pass **(partly unverified)**). Engineers should copy the architecture (central planner + dumb, cheap, redundant agents), not imagine ant-like autonomy. **Grade: A** (deployed), with the emergent component being a side effect, not the control principle.

### 2.2 Kilobots: 1,024 robots self-assembling

Rubenstein, Cornejo & Nagpal, *Programmable self-assembly in a thousand-robot swarm* (Science 345, 2014): 1,024 three-centimetre, ~$14 robots using only three primitives — edge-following, gradient formation and trilateration-based localisation — formed a star, a wrench and the letter K from four seed robots, with no central controller and an algorithm designed to tolerate per-robot error. Assembly took up to ~12 hours; robots did not physically attach ([IEEE Spectrum 2014](https://spectrum.ieee.org/a-thousand-kilobots-self-assemble); [Robohub 2014](https://robohub.org/?p=36075); [National Geographic 2014](https://www.nationalgeographic.com/science/article/a-swarm-of-a-thousand-cooperative-self-organising-robots)). It is the clearest physical demonstration that simple local rules scale to four-digit populations, and its lesson — design for error, not for perfection — recurs in every successful case below. **Grade: C** (lab).

### 2.3 Drone light shows and defence swarms

**Light shows.** Intel's Shooting Star shows escalated from 100 drones (2015) to 500 (2016), 1,218 at PyeongChang (2018) and 2,018 for Intel's anniversary; Ehang flew 1,374 in Xi'an ([Guinness 2016](https://www.guinnessworldrecords.com/news/2016/11/intel-launches-500-drones-into-sky-and-breaks-world-record-in-spectacular-style-449886); [TelecomTV 2018](https://www.telecomtv.com/content/devices/intel-plans-to-break-drone-light-show-record-with-over-1-500-drones-flown-at-50th-anniversary-celebrations-30716); [The Drone Girl 2018](https://www.thedronegirl.com/2018/07/19/intel-drone-swarm-records/)). These are commercially deployed (A) but are generally understood to fly pre-computed GPS trajectories from a ground station rather than emergent flocking; this pass could not retrieve a primary technical description **(unverified)**. Treat them as evidence of cheap, reliable mass-drone operation, not of swarm intelligence.

**DARPA OFFSET (2017–2021).** The OFFensive Swarm-Enabled Tactics programme targeted swarms of up to 250 air and ground robots supporting infantry in urban terrain, with Northrop Grumman and Raytheon BBN as swarm-system integrators. The third field experiment at Camp Shelby used ~250 vehicles; the sixth and final experiment (Fort Campbell, Nov–Dec 2021) ran "over 100" platforms, with program manager Timothy Chung stating swarm capabilities were "rapidly nearing availability" ([Overt Defense 2021](https://overtdefense.com/2021/12/darpa-runs-final-test-for-offset-program-drone-swarm); [ExecutiveGov 2021](https://www.executivegov.com/articles/darpa-concludes-final-drone-swarm-control-tech-experiment); [UST 2020](https://www.unmannedsystemstechnology.com/2020/01/darpa-offset-drone-swarm-program-demonstrates-urban-raid/)). A companion human-factors study found operators overloaded only ~3% of the time while commanding the swarm ([IEEE Spectrum](https://spectrum.ieee.org/amp/darpa-robot-2670858617)). **Grade: B** (large field experiments, no operational deployment reported).

### 2.4 Agricultural swarms

SwarmFarm Robotics (Queensland) sells small autonomous "SwarmBots" that operate as fleets of lightweight units instead of one large tractor. Company and investor figures: ~145–200 robots deployed, first commercial units around 2019, first US unit delivered, and cumulative coverage reported between ~2 million and 7 million hectares depending on source and date ([QIC](https://www.qic.com/News-and-Insights/SwarmFarm-builds-future-of-farming-from-new-Darling-Downs-manufacturing-hub); [GlobalAgInvesting](https://globalaginvesting.com/australias-green-bank-cefc-backs-swarmfarm-robotics-with-a7m-series-b-investment/); [GRDC GroundCover](https://groundcover.grdc.com.au/innovation/precision-agriculture-and-machinery/bots-on-the-ground-farmings-new-army); [Future Farming](https://www.futurefarming.com/tech-in-focus/swarmfarm-robotics-delivers-first-commercial-unit-in-the-us/)). The emergence here is modest (fleet-level coverage from independent units, each with simple local coverage logic) and figures are self-reported and inconsistent. **Grade: A** (commercial), with the caveat that the "swarm" is operational rather than algorithmic.

---

## 3. Traffic and crowds

### 3.1 Hajj / Jamarat Bridge (Helbing, 2006–2007)

**Mechanism.** Helbing's social-force model treats pedestrians as particles with desired velocities and repulsive interactions; crowd phenomena (lanes, stop-and-go waves, "crowd turbulence") emerge from these local forces.

**Validation and deployment.** After the January 2006 Mina crush (>300 dead), Helbing, Johansson and Al-Abideen analysed video footage and identified two phase transitions — laminar flow to stop-and-go, then to turbulent flow in which people are pushed over — published as *Dynamics of Crowd Disasters: An Empirical Study* (Physical Review E 75, 046109, 2007) ([arXiv physics/0701203](https://arxiv.org/pdf/physics/0701203); [ETH record](https://www.research-collection.ethz.ch:443/handle/20.500.11850/7000?show=full)). Their recommendations — one-way flow in the street network and on the plaza to eliminate counterflows, removal of bottlenecks, fixed routes and time schedules to spread pilgrims in space and time, plus automated crowd monitoring — were implemented in the redevelopment of the Jamarat Bridge; Physics World reported no major incidents at the bridge in the following Hajj, and the paper itself describes "comfortable and continuous flow" and a safe Hajj ([Physics World 2007](https://physicsworld.com/a/crowd-turbulence-has-deadly-consequences/); [Nature News 2007](https://www.nature.com/news/2007/070115/full/news070115-13.html); [Boing Boing 2007](https://boingboing.net/2007/01/23/crowd-control-in-mec.html)). Later Hajj planning extended the scheduling approach ([Operations Research 2019](https://pubsonline.informs.org/doi/pdf/10.1287/opre.2018.1798)). **Grade: A.** This is the single strongest "emergence-informed design saved lives" case in the literature, with the caveat that attribution of later safety to the model alone cannot be isolated from the other measures.

### 3.2 Commercial crowd simulators: Legion, MassMotion, Pathfinder

- **Legion** (now Bentley) descends from a 2000 Warwick PhD describing the crowd "as an emergent phenomenon" from individual agents ([Warwick thesis](https://wrap.warwick.ac.uk/36364)). AECOM used it to model Canning Town station for the London 2012 Olympic Delivery Authority, building and validating a 2008 base-year model before testing spectator scenarios ([AECOM](https://aecom.com/tw/?p=15243)). Vendor claims validation against empirical measurements ([Bentley](https://www.bentley.com/software/legion/)). **Grade: A/B.**
- **MassMotion** (Arup/Oasys): an Arup study validated egress predictions against observed evacuation drills, with total evacuation times within 1–10% of observed ([Rivers et al. 2011](https://files.thunderheadeng.com/femtc/2011_d2-11-rivers-paper.pdf)); a Toronto Bloor-Yonge subway study won a TRB award ([Arup](https://www.arup.com/news-and-events/massmotion-technology-at-the-heart-of-winning-paper)); an independent Lund thesis tested its sub-behaviours ([Lund 2016](https://lup.lub.lu.se/student-papers/record/8875378)). **Grade: B.**
- **Pathfinder** (Thunderhead): vendor publishes its own verification/validation tests against research data ([Oasys/Thunderhead](https://www.oasys-software.com/wp-content/uploads/2018/09/MassMotion-–-A-Step-In-The-Right-Direction-Interflam-2013.pdf)); no independent validation located in this pass **(unverified)**. **Grade: B (vendor-reported).**

These tools are routinely used in station, stadium and building design codes work; the "proof" is adoption plus drill-level validation, not published counterfactuals.

### 3.3 City-scale agent-based traffic: SUMO and MATSim

- **SUMO** (DLR, since 2001; now Eclipse). Provided traffic forecasts to the City of Cologne during the Pope's visit / World Youth Day 2005 and the 2006 World Cup ([DLR elib](https://elib.dlr.de/46740); [SUMO about](https://sumo.dlr.de/about/)); real-world scenarios exist for Bologna (iTETRIS) and Monaco (MoST) ([SUMO scenarios](https://sumo.dlr.de/wiki/Data/Scenarios)). It is the de-facto standard for V2X and traffic-light research. **Grade: B** (event-based municipal use; research otherwise).
- **MATSim** (ETH Zurich / TU Berlin). Agents with daily plans iteratively replan; congestion and mode share emerge. A Berlin model was built for transit operator BVG with PTV, including the full transit schedule and a 2015 forecast; Zurich grew to national scale; Singapore's model was built within the ETH Future Cities Laboratory with Land Transport Authority data, explicitly labelled research ([MATSim Berlin](https://matsim.org/gallery/berlin/); [MATSim Zurich](https://matsim.org/gallery/zurich/); [MATSim Singapore](https://www.matsim.org/gallery/singapore/)). **Grade: B.**

### 3.4 Self-organising traffic lights

**Mechanism (Lämmer & Helbing).** Each intersection locally optimises service of its arriving platoons, with a stabilisation rule bounding waiting time; coordination between intersections emerges from the platoons themselves instead of a fixed "green wave" plan ([Lämmer & Helbing 2008, arXiv 0802.0403](https://arxiv.org/pdf/0802.0403)). Simulations of a 13-intersection Dresden network gave 10–30% delay reduction ([Planetizen 2010](https://planetizen.com/node/46073)). An ETH licensing notice reports an "extensive pilot study in Dresden" with 56% less delay for trams/buses, 36% for pedestrians and cyclists and 9% for cars versus state-of-the-art green-wave control ([ETH / Science|Business](https://sciencebusiness.net/news/75656/ETH-Zurich%3A-Licensing-or-collaboration-opportunity-for-new-traffic-control-technology)), and a 2016 *Straßenverkehrstechnik* article, *Selbst-gesteuerte Lichtsignalanlagen im Praxistest*, reports shorter waits for all modes versus the traffic-responsive VS-PLUS system ([TRID](https://trid.trb.org/View/1407224)). The primary pilot report could not be retrieved **(figures partly unverified)**. **Grade: B.**

**Gershenson's rules** (2004–2012) are simpler — count waiting cars, switch when a threshold is reached, with a few anti-gridlock constraints — and outperform green waves across densities in simulation ([Gershenson 2004](https://arxiv.org/pdf/nlin/0411066); [Gershenson & Rosenblueth 2012](https://turing.iimas.unam.mx/sos/?q=node/37)). Press coverage credits a 2016 Mexico City *metro* implementation of his ideas, not traffic lights ([ACM / Quanta](https://cacmb4.acm.org/careers/247717-complexity-scientist-beats-traffic-jams-through-adaptation)). **Grade: C.**

### 3.5 Ride-hailing dispatch

Dispatch is where "emergent market" meets production ML. DiDi's KDD 2022 paper *Reinforcement Learning in the Wild* describes an RL dispatch policy A/B-tested in multiple cities and then launched as the primary dispatch mode in one major international market, with >1.3% driver-income gain in A/B and ~5.3% on major metrics after full launch (causal-inference estimate) ([arXiv 2202.05118](https://ar5iv.labs.arxiv.org/html/2202.05118)). Earlier DiDi work used mean-field multi-agent RL in which each driver-agent acts on local state and the fleet-level supply/demand balance emerges ([Li et al. 2019](https://arxiv.org/pdf/1901.11454); [Zhou et al. 2019](https://arxiv.org/pdf/1910.02591.pdf)), but the deployed system is a centrally trained, batched matcher. **Grade: A** for the deployment; the fully decentralised multi-agent variants remain **C**.

---

## 4. Epidemiology

### 4.1 Pre-COVID: MIDAS and government pandemic planning

The NIH Models of Infectious Disease Agent Study (MIDAS) network, funded from 2004, built the individual-based models that shaped US and UK pandemic plans ([MIDAS history, PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC2583792); [NIH RFA 2005](https://grants.nih.gov/grants/guide/rfa-files/RFA-GM-05-011.html)). Key outputs: Longini et al., *Containing pandemic influenza at the source* (Science 309, 2005) and Ferguson et al., *Strategies for containing an emerging influenza pandemic in Southeast Asia* (Nature 437, 2005), which established targeted antiviral prophylaxis as a containment strategy; Germann et al. (PNAS 2006) simulated all 281 million US residents with Census and DOT mobility data ([PMC Germann 2006](https://pmc.ncbi.nlm.nih.gov/articles/PMC1458676); [HKU record of Ferguson 2005](https://hub.hku.hk/handle/10722/54275)). Epstein's smallpox ABM (Brookings) informed post-2001 bioterror planning ([Epstein, Brookings](https://www.brookings.edu/wp-content/uploads/2016/07/0402_agent_based_epstein.pdf)). Epstein notes the group "worked closely with the Government" on pandemic flu containment, and MIDAS received an HHS Secretary's award in 2006. **Grade: A/B** (used by government; prospective validation impossible by design).

### 4.2 Imperial College Report 9 (March 2020)

Report 9 (16 March 2020) used the Ferguson group's individual-based CovidSim to project ~510,000 UK and ~2.2 million US deaths without interventions, and is widely credited with precipitating the UK's switch from mitigation to lockdown ([Science Media Centre 2023](https://www.sciencemediacentre.org/expert-reaction-to-reanalysis-of-model-used-for-imperial-report-9-and-impact-of-school-closures/); [LBC](https://www.lbc.co.uk/article/projections-which-led-to-stringent-lockdown-backed-by-new-study-DWyjXP_2/)). Its influence is itself contested: Dominic Cummings's inquiry evidence claims the report had "almost no influence" on the decision ([Science Media Centre](https://www.sciencemediacentre.org/?p=41375)).

**Criticism and validation.** The released code (~15,000 lines, decades of accretion, originally one very long file) drew heavy software-engineering criticism, including a widely shared pseudonymous review ([CACM 2020](https://cacm.acm.org/blogs/blog-cacm/246511-the-software-that-led-to-the-lockdown/fulltext); [Daily Friend 2020](https://dailyfriend.co.za/2020/05/08/why-the-secrecy-sa-lockdown-and-uks-buggy-covid-19-model/)). An independent **Codecheck** led by Stephen Eglen (Cambridge) reproduced the Report 9 results to within ~5%, confirming computational reproducibility but not epidemiological correctness ([Imperial / Codecheck 2020](https://www.imperial.ac.uk/news/197875/codecheck-confirms-reproducibility-covid-19-model-results)). A 2020 BMJ reanalysis (Rice et al., Edinburgh) reproduced the main results and showed the model already implied school closures could worsen later waves ([Edinburgh commentary](https://webhomes.maths.ed.ac.uk/~swood34/blog/DC-evidence.html)). The CACM retrospective's conclusion is the fair one: practices were lax, but the code "was not fundamentally flawed". **Grade: A** (policy use), **B** (reproducibility), with outcome validation inherently confounded by the interventions it triggered.

### 4.3 Covasim (IDM)

Covasim (Kerr et al., PLoS Computational Biology 2021) is an open-source ABM with age structure, layered household/school/work/community networks and within-host viral load, simulating testing, tracing, distancing and vaccination ([PLoS Comp Bio 2021](https://www.doi.org/10.1371/JOURNAL.PCBI.1009149); [GitHub](https://github.com/starsimhub/covasim)). Its paper documents policy use in the US, Vietnam, UK and Australia, including a Seattle application where scenario results informed a rapid decision and were subsequently validated against real data. The best-known external application, Panovska-Griffiths et al. (Lancet Child & Adolescent Health 2020), modelled UK school reopening and found that with 68% of contacts traced, 75% of symptomatic cases would need testing to avoid a second wave ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC8341708/)). **Grade: A/B.**

### 4.4 GLEAM

GLEAM is a metapopulation model (subpopulations around airports coupled by commuting and airline data; within-population stochastic compartmental dynamics). Its 2009 H1N1 forecasts of peak timing were validated retrospectively against surveillance from 48 countries (Tizzoni et al., BMC Medicine 2012) ([BMC Medicine](https://link.springer.com/article/10.1186/1741-7015-10-165); [Northeastern 2013](https://news.northeastern.edu/2013/01/07/validation-for-flu-prediction)). Chinazzi et al. (Science 368, 2020) used it to show the Wuhan quarantine delayed mainland spread by only 3–5 days but cut international importations by ~80% until mid-February, and that travel bans alone were ineffective without ≥50% community transmission reduction ([Inside Precision Medicine 2020](https://www.insideprecisionmedicine.com/news-and-features/study-details-effects-of-travel-restrictions-on-spread-of-covid-19)). **Grade: B** (validated against real data; strictly a hybrid metapopulation rather than individual-agent model).

### 4.5 FRED and others

FRED (Pittsburgh, BMC Public Health 2013) is an open-source ABM with synthetic populations for every US county, commercialised by Epistemix ([BMC Public Health](https://bmcpublichealth.biomedcentral.com/track/pdf/10.1186/1471-2458-13-940); [FRED](https://fred.publichealth.pitt.edu/)). **Grade: B/C.** EpiSim (TU Berlin, built on MATSim mobility traces) reportedly delivered weekly reports to the German federal government in 2020; this could not be verified within this pass **(unverified)**.

**What the pandemic taught about ABMs.** Reproducibility and code quality are now a precondition for political legitimacy; calibration to early, noisy data dominates model structure; and the counterfactual problem (a model that triggers interventions cannot be validated against its own no-intervention projection) is permanent. The 2003 ABMs were used; the 2020 ABMs were *audited*.

---

## 5. Economics, finance and policy

### 5.1 The Santa Fe lineage

The Santa Fe Institute Artificial Stock Market (Arthur, Holland, LeBaron, Palmer, Tayler, 1997; precursor Palmer et al. Physica D 1994) was built to settle a bet: would learning agents converge to the rational-expectations equilibrium? With slow learning they did; with fast learning the market produced bubbles, crashes, persistent volume and the statistical signatures of real markets ([LeBaron, *Building the SFI-ASM*](https://trevcan.duckdns.org/files/trevor/papers/emintham-Papers/LeBaron-%20Building%20the%20Santa%20Fe%20Artificial%20Stock%20Market.pdf); [Palmer et al. 1994](https://deepblue.lib.umich.edu/items/18b0197f-305e-40c5-b9bf-98ca56549ca5/full); [Sornette 2014 review](https://arxiv.org/pdf/1404.0243)). Later work found defects (unrealistically fast strategy turnover) and corrected versions exist ([Ehrentreich](https://trevcan.duckdns.org/files/trevor/papers/emintham-Papers/Ehrentreich-%20A%20Corrected%20Version%20of%20the%20Santa%20Fe%20Institute%20Artificial%20Stock%20Market%20Model.pdf)). **Grade: C**, but foundational for everything below.

### 5.2 EURACE

EURACE (EU FP6, 2006–2009; Bielefeld, Genoa, Ancona and others, with Stiglitz) attempted a full agent-based model of the European economy on the FLAME parallel framework, intended for policy design ([EURACE paper](https://catalog.comses.net/publications/1653); [Bielefeld deliverables](https://uni-bielefeld.de/fakultaeten/wirtschaftswissenschaften/lehrbereiche/etace/eurace@unibi/eurace-deliverables/EURACE_VisionDocument.pdf)). No evidence of Commission policy use was found. **Grade: C.**

### 5.3 Bank of England

- **UK housing market ABM.** Baptista, Farmer, Hinterschweiger, Low, Tang & Uluc, Staff Working Paper 619 (Oct 2016): first-time buyers, owners, buy-to-let investors and renters calibrated to micro-data; used to test loan-to-income limits and the role of the buy-to-let sector in booms and busts ([BoE WP 619](https://www.bankofengland.co.uk/working-paper/2016/macroprudential-policy-in-an-agent-based-model-of-the-uk-housing-market); [INET Oxford](https://www.inet.ox.ac.uk/news/bank-of-england-wp)). **Grade: B** (calibrated to real data; informs macroprudential analysis).
- **Market-based finance stress simulation.** Baranova, Douglas & Silvestri (SWP 803, 2019) simulate UK corporate-bond fire sales among open-ended funds, dealers and insurers; Aikman et al. (SWP 809, 2019) extend this system-wide, and a Bank of Italy/ECB/BoE variant was applied to the euro-area COVID shock ([BoE SWP 803](https://www.bankofengland.co.uk/working-paper/2019/simulating-stress-in-the-uk-corporate-bond-market-investor-behaviour-and-asset-fire-sales); [BoE SWP 809](https://www.bankofengland.co.uk/working-paper/2019/system-wide-stress-simulation); [SUERF brief](https://www.suerf.org/suerf-policy-brief/52017/a-model-of-system-wide-stress-simulation-market-based-finance-and-the-covid-19-event)). **Grade: B.**
- A 2025 BoE/INET/Banco de España survey, *Agent-based modeling at central banks: recent developments and new challenges*, concludes ABMs "have emerged as effective complementary tools" at central banks ([BoE 2025](https://www.bankofengland.co.uk/working-paper/2025/agent-based-modeling-at-central-banks-recent-developments-and-new-challenges); [INET Oxford](https://www.inet.ox.ac.uk/publications/agent-based-modeling-at-central-banks-recent-developments-and-new-challenges)).

### 5.4 Austria: an ABM that forecasts

Poledna, Miess, Hommes & Rabitsch, *Economic forecasting with an agent-based model* (European Economic Review 151, 2023): a full ESA-2010-consistent ABM of Austria populated from national accounts, input-output tables and census data, which competes with VAR and DSGE benchmarks in out-of-sample macro forecasting and provides sector-level forecasts; applied to COVID lockdown scenarios ([IIASA record](https://pure.iiasa.ac.at/18339); [IHS eprint](https://irihs.ihs.ac.at/id/eprint/6453/); [IIASA award 2021](https://iiasa.ac.at/news/may-2021/sebastian-poledna-receives-complexity-in-macroeconomics-award)). **Grade: B.** This is the paper that moved macro ABMs from "interesting" to "usable", because it accepted the forecasting benchmark the DSGE community set.

### 5.5 Bank of Canada and the ECB

Building on the Austrian model, IIASA and the Bank of Canada developed **CANVAS**, a Canadian behavioural ABM using micro and macro data for forecasting and policy analysis; IIASA states the Bank added it to its core macroeconomic model suite, calling it the first instance of a major central bank adopting an ABM to inform monetary policy, with a peer-reviewed version in the Journal of Economic Dynamics and Control (2025) ([IIASA annual report](https://iiasa.ac.at/ar/23/iiasa-works-with-bank-of-canada-to-strengthen-monetary-policy-using-agent-based-modeling); [BoC SWP 2022-51](https://www.bankofcanada.ca/wp-content/uploads/2022/12/swp2022-51.pdf)). The adoption claim is from a partner, not from the Bank's own governance documents, so **Grade: A (partner-reported) / B**. Payments Canada and the Bank have also used agent-based and RL models of the high-value payments system ([Payments Canada](https://payments.ca/insights/research/computational-model-market-microstructure-bilateral-credit-limits-payments)).

The ECB's documented role is convening (4th ABM-for-Policy workshop, June 2025) and co-authoring stress models; no ECB policy decision attributable to an ABM was found ([ECB 2025](https://www.ecb.europa.eu/press/conferences/html/20250626_abm4policy.da.html)). No Federal Reserve ABM in official use was found. **Grade: C** for both.

### 5.6 Market microstructure: ABIDES

ABIDES (Byrd, Hybinette & Balch, 2019; Georgia Tech with J.P. Morgan AI Research) is an open-source discrete-event market simulator: tens of thousands of agents trade against an exchange agent via NASDAQ ITCH/OUCH-style messages at nanosecond resolution with configurable latency; used to evaluate trading strategies and later extended to ABIDES-Economist ([ABIDES arXiv 1904.12066](https://arxiv.org/pdf/1904.12066); [Balch et al. 2019](https://arxiv.org/pdf/1906.12010); [ABIDES-Economist 2024](https://arxiv.org/pdf/2402.09563)). Use inside JPMorgan research is documented; use by exchanges or regulators was not confirmed in this pass **(unverified)**. **Grade: B/C.**

---

## 6. Ecology, urban planning and energy

### 6.1 Fisheries: POSEIDON

POSEIDON (Bailey, Carrella et al., Sustainability Science 2019) couples an adaptive agent-based fishing fleet with a simplified ocean model; boats are not scripted but learn where to fish, and Bayesian optimisation over runs searches for policies meeting management goals. A follow-up fitted to US West Coast groundfish found observed vessel behaviour best predicted by simple explore/exploit heuristics. It is used by Ocean Conservancy and The Nature Conservancy (Indonesia; FAD management in tuna purse-seine fisheries) ([Oxford record](https://intelligent-earth.ox.ac.uk/node/4030731); [Ocean Conservancy](https://oceanconservancy.org/sustainable-fisheries/poseidon/)). No formal NOAA/ICES adoption was found. **Grade: B.**

### 6.2 Land-use change

The LUDAS framework (central Vietnam watershed) is the best example of an empirically verified, household-level land-use ABM used to compare policy bundles ([UCLouvain](https://dial.uclouvain.be/pr/boreal/object/boreal%3A271226/datastream/PDF_01/view)); MP-MAS and ABSOLUG are research models ([Göttingen](https://www.uni-goettingen.de/en/sp+12%3a+agent-based+assessment+of+land+management+strategies/211054.html); [JASSS 2023](https://www.jasss.org/26/1/5.html)). No ministry-level adoption found. **Grade: C/B.**

### 6.3 Transactive energy: decentralised demand response

**Olympic Peninsula GridWise demonstration (PNNL/DOE, 2006–07).** Water heaters, thermostats, commercial HVAC, municipal pumps and distributed generators bid into a five-minute retail double auction; feeder congestion was managed by price alone, and peak load on the constrained feeder was reduced, with residential customers as active market participants. Chassin and Kiesling argue it showed decentralised coordination matched or beat centralised utility control ([PNNL report 2008](https://www.pnnl.gov/publications/pacific-northwest-gridwisetm-testbed-demonstration-projects-part-i-olympic-peninsula); [DOE fast facts](https://www.smartgrid.gov/files/documents/GridWise_Demonstration_Project_Fast_Facts_200708.pdf); [Chassin & Kiesling](https://siliconflatirons.org/documents/initiatives/IRLEdaythree/Chassin_Decentralized.pdf)). **Grade: B.**

**PowerMatching City, Hoogkerk (2009–2015).** 25 homes with micro-CHP, hybrid heat pumps, PV and EVs coordinated by the PowerMatcher agent-based market; the project reported achieving end-user optimisation, grid-load reduction and imbalance reduction simultaneously, though no headline peak-reduction percentage was located in this pass ([CORDIS](https://cordis.europa.eu/article/id/120867-smart-grid-proves-feasible/en); [TNO/ECN paper](https://publications.tno.nl/publication/34631302/P026hH/m11002.pdf); [DNV](https://www.dnv.com/cases/powermatching-city-lighthouse-project-79544/)). **Grade: B.**

### 6.4 Volkswagen's Lisbon "quantum traffic" pilot (2019): adjacent, not emergent

During Web Summit 2019, VW routed nine Carris buses with a D-Wave annealer, each bus receiving an individual route to spread load; the authors call it the first commercial use of a quantum processor for a live task ([VW Group Italia](https://www.volkswagengroup.it/en/lab/quantum-computers-for-traffic-optimisation-a-pilot-project-in-lisbon); [arXiv 2006.14162](https://arxiv.org/pdf/2006.14162)). It is centralised QUBO optimisation, often mislabelled "swarm". Include it as a cautionary label check. **Grade: B** (pilot), not emergent.

---

## 7. Software and networks

### 7.1 Self-Organising Networks (SON) in LTE/5G

SON functions standardised by 3GPP — Automatic Neighbour Relations (Rel-8), mobility load balancing, handover robustness and RACH optimisation (Rel-9), energy saving (Rel-10/11) — let each cell adjust its own parameters from local measurements, with network-wide coverage/capacity balance emerging ([Survey, arXiv 1707.09300](https://arxiv.org/pdf/1707.09300)). Deployment is broad: Nokia states more than 100 operators run its SON software (EE/BT contract) ([Total Telecom](https://totaltele.com/nokia-self-organizing-networks-software-to-enhance-network-reliability-for-bt/)). Quantified public results are scarce; a Sofrecom deployment account from Tunisia and France reports ~20% higher user bandwidth and ~50% fewer handover-area drops ([Sofrecom 2015](https://www.sofrecom.com/publications/self-optimization-son-is-the-future-of-cellular-networks)), and NEC's 25-site Yokohama trial confirmed handover optimisation and time-of-day sleep energy savings without quality loss ([Converge Digest](https://convergedigest.com/?p=53944)). **Grade: A** (deployed at scale), with most KPIs vendor-reported.

### 7.2 Gossip protocols

Epidemic/gossip dissemination is the most successful emergent mechanism in production software: each node periodically exchanges state with random peers; cluster-wide convergence and failure detection emerge with O(log N) latency and no coordinator. Amazon's Dynamo (SOSP 2007) used gossip for membership ([Dynamo paper](https://www.cs.purdue.edu/homes/bb/cs590/papers/amazon-dynamo-sosp2007.pdf); [Vogels 2007](https://www.allthingsdistributed.com/2007/10/amazons_dynamo.html)); Cassandra and Riak followed. HashiCorp's Serf/Consul/Nomad use SWIM-derived gossip for LAN and WAN membership and failure detection ([Consul docs](https://developer.hashicorp.com/consul/docs/v1.10.x/architecture/gossip)); its **Lifeguard** extensions cut false-positive failure detections by up to 50× in production ([HashiCorp 2017](https://hashicorp.com/blog/making-gossip-more-robust-with-lifeguard)). **Grade: A.** The design lesson: eventual consistency is accepted, and the failure detector is explicitly allowed to be wrong, with suspicion timeouts as the damping term.

### 7.3 Ant- and bee-based load balancing

Beyond the honeybee server-allocation result (§1.4), no production deployment of ant-based load balancing was found; the field remains **Grade: C**. Where "swarm" ideas survive in production load balancing it is as randomised local choice (power-of-two-choices, gossip-shared load hints) rather than pheromone models.

### 7.4 Emergence as a risk: documented incidents

The same feedback that makes emergent systems adaptive makes them capable of self-amplifying failure. Three well-investigated cases:

| Incident | Mechanism | Scale | Source |
|---|---|---|---|
| **Flash Crash, 6 May 2010** | A single 75,000-contract E-Mini sell algorithm pegged to 9% of trailing volume; HFTs absorbed then dumped inventory, passing contracts among themselves ("hot potato"), which inflated volume and made the algorithm sell faster — a positive feedback loop that dropped the E-Mini 3% in four minutes and cascaded into equities | ~$1 trillion temporary market-cap swing; 20+ minute dislocation | [SEC/CFTC staff report, 30 Sep 2010](https://SEC.GOV/files/marketevents-report.pdf); [Kirilenko et al. (CFTC)](https://www.cftc.gov/idc/groups/public/@economicanalysis/documents/file/oce_flashcrash0314.pdf) |
| **Northeast blackout, 14 Aug 2003** | Untrimmed trees + a failed alarm system at FirstEnergy let three 345 kV line trips go unnoticed; load redistribution tripped further lines in a cascade across eight states and Ontario; the Task Force judged it preventable and found causes "strikingly similar" to earlier outages | 50 million people, 61,800 MW, up to 4 days | [US-Canada Task Force Final Report, Apr 2004](https://www.energy.gov/sites/prod/files/oeprod/DocumentsandMedia/BlackoutFinal-Web.pdf) |
| **AWS US-East EBS outage, 21 Apr 2011** | A mis-executed network change isolated EBS nodes from replicas; on reconnection every node simultaneously searched for re-mirroring space, exhausting cluster capacity ("re-mirroring storm"); insufficient back-off and a race condition kept 13% of volumes stuck for days | ~4 days; 0.07% volumes unrecoverable | [AWS post-mortem](https://aws.amazon.com/message/65648/); [InfoQ 2011](https://www.infoq.com/news/2011/04/Amazon-EC2-Outage-Explained/) |

The distributed-systems community has since named the general pattern **metastable failure**: a trigger pushes a system into overload, and a sustaining effect (retries, re-replication, cache misses) keeps it there after the trigger is gone; recovery needs an external push such as load shedding or restart. Bronson et al. (HotOS 2021) defined it, and Huang et al. (OSDI 2022) found at least 4 of 15 major AWS outages in a decade were metastable ([Bronson et al.](https://warez.kernelpanic.cafe/errata/linkdump/Element%20-%20Chat%20Export%20-%209-11-2022%20at%206-07-59%20PM/files/hotos21-s11-bronson-10-5-2021%20at%2012-42-24%20AM.pdf); [Huang et al. OSDI 2022](https://www.usenix.net/system/files/osdi22-huang-lexiang.pdf)). Market "circuit breakers", grid relay coordination standards and exponential back-off with jitter are all the same remedy: insert damping where the loop gain exceeds one.

---

## 8. Comparison table

| Domain | Application | Emergent mechanism | Grade | Key source (year) |
|---|---|---|---|---|
| Optimisation | Ant routing (BT topology, AntNet) | Stigmergic pheromone reinforcement | C | Schoonderwoerd 1996; Di Caro & Dorigo 1998 |
| Optimisation | IDSIA/AntOptima vehicle routing | Ant Colony System | B (A unverified) | Montemanni 2005; Rizzoli 2007 |
| Optimisation | Southwest cargo routing | Simple local rules (consultant-reported) | C / unverified | Bonabeau 2001, 2003 |
| Optimisation | Honeybee server allocation | Recruitment by advertisement | C | Nakrani & Tovey 2004 |
| Robotics | Amazon/Kiva warehouses | Central planner; emergent inventory layout | A | Wurman et al. 2008; Amazon 2023 |
| Robotics | Kilobots 1,024-robot self-assembly | Edge-following + gradients + local localisation | C | Rubenstein et al. 2014 |
| Robotics | DARPA OFFSET | Heterogeneous swarm tactics, human-on-the-loop | B | DARPA 2021 |
| Robotics | SwarmFarm agricultural fleets | Fleet of small independent units | A (operational swarm) | QIC / GRDC 2024 |
| Crowds | Jamarat Bridge redesign | Social-force model; crowd turbulence | A | Helbing et al. PRE 2007 |
| Crowds | Legion / MassMotion / Pathfinder | Agent-based pedestrian simulation | A/B | AECOM 2012; Rivers 2011 |
| Traffic | SUMO (Cologne 2005/06), MATSim (Berlin BVG) | Microscopic / activity-based agents | B | DLR 2005; MATSim gallery |
| Traffic | Self-organising traffic lights, Dresden | Local platoon-serving + stabilisation | B | Lämmer & Helbing 2008; ETH pilot; TRID 2016 |
| Traffic | DiDi RL dispatch | Learned matching; market equilibrium emergent | A | KDD 2022 |
| Epidemiology | MIDAS flu/smallpox ABMs | Individual-based transmission | A/B | Longini 2005; Ferguson 2005; Germann 2006 |
| Epidemiology | Imperial Report 9 / CovidSim | Individual-based transmission | A (use), B (reproducibility) | Ferguson 2020; Codecheck 2020 |
| Epidemiology | Covasim | Layered-network ABM | A/B | Kerr 2021 |
| Epidemiology | GLEAM | Metapopulation + mobility | B | Tizzoni 2012; Chinazzi 2020 |
| Finance | SFI artificial stock market | Co-evolving trader strategies | C | Arthur et al. 1997 |
| Finance/policy | BoE housing ABM | Heterogeneous households, credit | B | Baptista et al. 2016 |
| Finance/policy | BoE / ECB stress simulation | Fire-sale feedback among funds, dealers | B | Baranova 2019; Aikman 2019 |
| Macro | Austria forecasting ABM | Full-economy heterogeneous agents | B | Poledna et al. 2023 |
| Macro | Bank of Canada CANVAS | Behavioural macro ABM | A (partner-reported) | IIASA 2023; JEDC 2025 |
| Markets | ABIDES (JPMorgan) | Agent-based exchange simulation | B/C | Byrd et al. 2019 |
| Ecology | POSEIDON fisheries | Adaptive fleet agents | B | Bailey et al. 2019 |
| Energy | Olympic Peninsula GridWise; PowerMatching City | Agent double-auction / market agents | B | PNNL 2008; TNO 2011 |
| Networks | 3GPP SON | Per-cell self-configuration/optimisation | A | 3GPP Rel-8–11; Nokia |
| Software | Gossip (Dynamo, Cassandra, Consul) | Epidemic dissemination, SWIM | A | DeCandia 2007; HashiCorp 2017 |
| Risk | Flash Crash; 2003 blackout; AWS 2011 | Positive feedback, cascade, metastability | A (negative) | SEC/CFTC 2010; Task Force 2004; AWS 2011 |

---

## 9. Patterns that transferred to practice

Looking only at the A- and B-grade rows, the successful cases share properties that the C-grade folklore lacks.

1. **Simple, local, stateless-ish rules on cheap agents.** Kilobots ($14, three primitives), gossip nodes (random peer, periodic exchange), SON cells (local KPIs), transactive water heaters (one bid). Complexity lives in the aggregate, not the agent. Where the agent needed to be clever (ant routers in real IP networks), deployment never happened.
2. **Explicit damping and bounded loops.** Every production success has an evaporation, timeout, suspicion period, stabilisation rule or market-clearing interval that keeps loop gain below one: pheromone evaporation, SWIM suspicion timers, Lämmer's waiting-time bound, five-minute auctions. Every documented disaster lacked one until it was added afterwards (circuit breakers, back-off with jitter, relay coordination).
3. **Redundancy and tolerance of individual error as a design input.** Kilobots' algorithm assumed robots would fail; gossip assumes detectors lie; Kiva assumes robots stall. Systems that required every agent to behave stayed in the lab.
4. **A central layer where it is cheap and a decentralised layer where it is not.** Kiva, DiDi and drone shows are *hybrids*: global assignment is centralised because it is computationally affordable and auditable; local execution is decentralised because latency and scale demand it. Purist decentralisation is rare in production.
5. **Validation against the benchmark the incumbent sets.** Poledna et al. won acceptance by beating VARs on out-of-sample forecasts; MassMotion by matching drill times; GLEAM by matching 48 countries' peak timing; Codecheck by reproducing Report 9. ABMs that offered only "insight" (EURACE, SFI-ASM) stayed academic.
6. **Interventions that reshape the environment rather than the agents.** The Jamarat redesign did not change pilgrims' rules; it changed geometry and timing so that the same local rules produced laminar flow. For an engineer this is the cheapest lever: change the topology, the incentives or the rate limits, and let emergence do the rest.
7. **Honest provenance.** The weakest claims in this chapter (Southwest, Air Liquide, Migros/Barilla) all share a pattern: a vendor or consultant is the only source. Treat any swarm-intelligence case with a single commercial narrator as grade C until a customer or regulator reports the number.

---

## Sources

Swarm optimisation
- https://link.springer.com/doi/10.1007/bfb0053944 (Schoonderwoerd et al., 1996/97)
- https://www.rose-hulman.edu/class/cs/csse453/schedule/day4/LoadBalancing.pdf
- https://staff.washington.edu/paymana/swarm/dicaro98-jair.pdf (Di Caro & Dorigo, JAIR 1998)
- https://arxiv.org/pdf/1105.5449
- https://www.strc.ch/2002/gambardella.pdf (2002)
- https://ideas.repec.org/a/spr/jcomop/v10y2005i4d10.1007_s10878-005-4922-6.html (Montemanni et al., 2005)
- https://search.usi.ch/it/pubblicazioni/2709/ant-colony-optimization-for-real-world-vehicle-routing-problems (Rizzoli et al., 2007)
- https://www.logforum.net/vol2/issue3/no4/2_3_4_06.html (2006)
- https://interconnected.org/home/2002/11/20/the_french_company (2002)
- https://maaw.info/ArticleSummaries/ArtSumBonabeauMeyer2001.htm (Bonabeau & Meyer, HBR 2001)
- https://staff.washington.edu/paymana/swarm/bonabeau03-etcon.pdf (2003)
- https://interconnected.org/notes/2003/04/etcon/swarm.txt (2003)
- https://missiontolearn.com/book-excerpts/smart-swarm/ (2010)
- https://gadling.com/?p=11028 (2008)
- https://doaj.org/article/03190b32eb5f42ba83666376e1dc035d (Applied Sciences 2022)
- https://arxiv.org/pdf/2206.06940 (Walsh & Borkowski 2022)
- https://pure.uj.ac.za/en/publications/particle-swarm-optimisation-algorithm-based-renewable-energy-sour/
- https://ideas.repec.org/a/ids/ijsoma/v13y2012i4p441-456.html (2012)
- https://hg.gatech.edu/node/59987 (Nakrani & Tovey)
- https://news.cornell.edu/node/286521 (2016)

Swarm robotics
- https://ojs.aaai.org/index.php/aimagazine/article/view/2082 (Wurman, D'Andrea & Mountz, 2008)
- https://IEEECSS.org/sites/ieeecss/files/2019-06/IoCT2-SS-DAndrea-1.pdf
- https://arxiv.org/pdf/1612.05693 (Ma & Koenig 2016)
- https://aboutamazon.com/news/operations/amazon-introduces-new-robotics-solutions (2023)
- https://distributionstrategy.com/2025/06/amazon-reaches-750000-robots-in-fulfillment-operations/ (2025)
- https://spectrum.ieee.org/a-thousand-kilobots-self-assemble (2014)
- https://robohub.org/?p=36075 (2014)
- https://www.nationalgeographic.com/science/article/a-swarm-of-a-thousand-cooperative-self-organising-robots (2014)
- https://www.guinnessworldrecords.com/news/2016/11/intel-launches-500-drones-into-sky-and-breaks-world-record-in-spectacular-style-449886 (2016)
- https://www.telecomtv.com/content/devices/intel-plans-to-break-drone-light-show-record-with-over-1-500-drones-flown-at-50th-anniversary-celebrations-30716 (2018)
- https://www.thedronegirl.com/2018/07/19/intel-drone-swarm-records/ (2018)
- https://overtdefense.com/2021/12/darpa-runs-final-test-for-offset-program-drone-swarm (2021)
- https://www.executivegov.com/articles/darpa-concludes-final-drone-swarm-control-tech-experiment (2021)
- https://www.unmannedsystemstechnology.com/2020/01/darpa-offset-drone-swarm-program-demonstrates-urban-raid/ (2020)
- https://spectrum.ieee.org/amp/darpa-robot-2670858617
- https://www.qic.com/News-and-Insights/SwarmFarm-builds-future-of-farming-from-new-Darling-Downs-manufacturing-hub
- https://globalaginvesting.com/australias-green-bank-cefc-backs-swarmfarm-robotics-with-a7m-series-b-investment/
- https://groundcover.grdc.com.au/innovation/precision-agriculture-and-machinery/bots-on-the-ground-farmings-new-army (2024)
- https://www.futurefarming.com/tech-in-focus/swarmfarm-robotics-delivers-first-commercial-unit-in-the-us/

Traffic and crowds
- https://arxiv.org/pdf/physics/0701203 (Helbing, Johansson & Al-Abideen, PRE 2007)
- https://www.research-collection.ethz.ch:443/handle/20.500.11850/7000?show=full
- https://physicsworld.com/a/crowd-turbulence-has-deadly-consequences/ (2007)
- https://www.nature.com/news/2007/070115/full/news070115-13.html (2007)
- https://boingboing.net/2007/01/23/crowd-control-in-mec.html (2007)
- https://pubsonline.informs.org/doi/pdf/10.1287/opre.2018.1798 (2019)
- https://wrap.warwick.ac.uk/36364 (2000)
- https://aecom.com/tw/?p=15243 (London 2012)
- https://www.bentley.com/software/legion/
- https://files.thunderheadeng.com/femtc/2011_d2-11-rivers-paper.pdf (2011)
- https://www.arup.com/news-and-events/massmotion-technology-at-the-heart-of-winning-paper
- https://lup.lub.lu.se/student-papers/record/8875378 (2016)
- https://www.oasys-software.com/wp-content/uploads/2018/09/MassMotion-–-A-Step-In-The-Right-Direction-Interflam-2013.pdf (2013)
- https://elib.dlr.de/46740 (2005)
- https://sumo.dlr.de/about/
- https://sumo.dlr.de/wiki/Data/Scenarios
- https://matsim.org/gallery/berlin/
- https://matsim.org/gallery/zurich/
- https://www.matsim.org/gallery/singapore/
- https://arxiv.org/pdf/0802.0403 (Lämmer & Helbing 2008)
- https://planetizen.com/node/46073 (2010)
- https://sciencebusiness.net/news/75656/ETH-Zurich%3A-Licensing-or-collaboration-opportunity-for-new-traffic-control-technology
- https://trid.trb.org/View/1407224 (2016)
- https://arxiv.org/pdf/nlin/0411066 (Gershenson 2004)
- https://turing.iimas.unam.mx/sos/?q=node/37 (2012)
- https://cacmb4.acm.org/careers/247717-complexity-scientist-beats-traffic-jams-through-adaptation
- https://ar5iv.labs.arxiv.org/html/2202.05118 (DiDi, KDD 2022)
- https://arxiv.org/pdf/1901.11454 (2019)
- https://arxiv.org/pdf/1910.02591.pdf (2019)

Epidemiology
- https://pmc.ncbi.nlm.nih.gov/articles/PMC2583792 (MIDAS history)
- https://grants.nih.gov/grants/guide/rfa-files/RFA-GM-05-011.html (2005)
- https://pmc.ncbi.nlm.nih.gov/articles/PMC1458676 (Germann et al., PNAS 2006)
- https://hub.hku.hk/handle/10722/54275 (Ferguson et al., Nature 2005)
- https://www.brookings.edu/wp-content/uploads/2016/07/0402_agent_based_epstein.pdf
- https://www.sciencemediacentre.org/expert-reaction-to-reanalysis-of-model-used-for-imperial-report-9-and-impact-of-school-closures/ (2023)
- https://www.sciencemediacentre.org/?p=41375
- https://www.lbc.co.uk/article/projections-which-led-to-stringent-lockdown-backed-by-new-study-DWyjXP_2/
- https://cacm.acm.org/blogs/blog-cacm/246511-the-software-that-led-to-the-lockdown/fulltext (2020)
- https://dailyfriend.co.za/2020/05/08/why-the-secrecy-sa-lockdown-and-uks-buggy-covid-19-model/ (2020)
- https://www.imperial.ac.uk/news/197875/codecheck-confirms-reproducibility-covid-19-model-results (2020)
- https://webhomes.maths.ed.ac.uk/~swood34/blog/DC-evidence.html
- https://www.doi.org/10.1371/JOURNAL.PCBI.1009149 (Kerr et al., 2021)
- https://github.com/starsimhub/covasim
- https://pmc.ncbi.nlm.nih.gov/articles/PMC8341708/
- https://link.springer.com/article/10.1186/1741-7015-10-165 (Tizzoni et al., 2012)
- https://news.northeastern.edu/2013/01/07/validation-for-flu-prediction (2013)
- https://www.insideprecisionmedicine.com/news-and-features/study-details-effects-of-travel-restrictions-on-spread-of-covid-19 (Chinazzi et al., 2020)
- https://bmcpublichealth.biomedcentral.com/track/pdf/10.1186/1471-2458-13-940 (FRED, 2013)
- https://fred.publichealth.pitt.edu/

Economics, finance, policy
- https://trevcan.duckdns.org/files/trevor/papers/emintham-Papers/LeBaron-%20Building%20the%20Santa%20Fe%20Artificial%20Stock%20Market.pdf
- https://deepblue.lib.umich.edu/items/18b0197f-305e-40c5-b9bf-98ca56549ca5/full (Palmer et al., 1994)
- https://arxiv.org/pdf/1404.0243 (2014)
- https://trevcan.duckdns.org/files/trevor/papers/emintham-Papers/Ehrentreich-%20A%20Corrected%20Version%20of%20the%20Santa%20Fe%20Institute%20Artificial%20Stock%20Market%20Model.pdf
- https://catalog.comses.net/publications/1653 (EURACE)
- https://uni-bielefeld.de/fakultaeten/wirtschaftswissenschaften/lehrbereiche/etace/eurace@unibi/eurace-deliverables/EURACE_VisionDocument.pdf
- https://www.bankofengland.co.uk/working-paper/2016/macroprudential-policy-in-an-agent-based-model-of-the-uk-housing-market (Baptista et al., 2016)
- https://www.inet.ox.ac.uk/news/bank-of-england-wp
- https://www.bankofengland.co.uk/working-paper/2019/simulating-stress-in-the-uk-corporate-bond-market-investor-behaviour-and-asset-fire-sales (2019)
- https://www.bankofengland.co.uk/working-paper/2019/system-wide-stress-simulation (2019)
- https://www.suerf.org/suerf-policy-brief/52017/a-model-of-system-wide-stress-simulation-market-based-finance-and-the-covid-19-event
- https://www.bankofengland.co.uk/working-paper/2025/agent-based-modeling-at-central-banks-recent-developments-and-new-challenges (2025)
- https://www.inet.ox.ac.uk/publications/agent-based-modeling-at-central-banks-recent-developments-and-new-challenges
- https://pure.iiasa.ac.at/18339 (Poledna et al., EER 2023)
- https://irihs.ihs.ac.at/id/eprint/6453/
- https://iiasa.ac.at/news/may-2021/sebastian-poledna-receives-complexity-in-macroeconomics-award (2021)
- https://iiasa.ac.at/ar/23/iiasa-works-with-bank-of-canada-to-strengthen-monetary-policy-using-agent-based-modeling (2023)
- https://www.bankofcanada.ca/wp-content/uploads/2022/12/swp2022-51.pdf (2022)
- https://payments.ca/insights/research/computational-model-market-microstructure-bilateral-credit-limits-payments
- https://www.ecb.europa.eu/press/conferences/html/20250626_abm4policy.da.html (2025)
- https://arxiv.org/pdf/1904.12066 (ABIDES, 2019)
- https://arxiv.org/pdf/1906.12010 (2019)
- https://arxiv.org/pdf/2402.09563 (2024)

Ecology, urban, energy
- https://intelligent-earth.ox.ac.uk/node/4030731 (POSEIDON, 2019)
- https://oceanconservancy.org/sustainable-fisheries/poseidon/
- https://dial.uclouvain.be/pr/boreal/object/boreal%3A271226/datastream/PDF_01/view (LUDAS)
- https://www.uni-goettingen.de/en/sp+12%3a+agent-based+assessment+of+land+management+strategies/211054.html
- https://www.jasss.org/26/1/5.html (2023)
- https://www.pnnl.gov/publications/pacific-northwest-gridwisetm-testbed-demonstration-projects-part-i-olympic-peninsula (2008)
- https://www.smartgrid.gov/files/documents/GridWise_Demonstration_Project_Fast_Facts_200708.pdf (2007)
- https://siliconflatirons.org/documents/initiatives/IRLEdaythree/Chassin_Decentralized.pdf
- https://cordis.europa.eu/article/id/120867-smart-grid-proves-feasible/en
- https://publications.tno.nl/publication/34631302/P026hH/m11002.pdf (2011)
- https://www.dnv.com/cases/powermatching-city-lighthouse-project-79544/
- https://www.volkswagengroup.it/en/lab/quantum-computers-for-traffic-optimisation-a-pilot-project-in-lisbon (2019)
- https://arxiv.org/pdf/2006.14162 (2020)

Software, networks, risk
- https://arxiv.org/pdf/1707.09300 (SON survey, 2017)
- https://totaltele.com/nokia-self-organizing-networks-software-to-enhance-network-reliability-for-bt/
- https://www.sofrecom.com/publications/self-optimization-son-is-the-future-of-cellular-networks (2015)
- https://convergedigest.com/?p=53944
- https://www.cs.purdue.edu/homes/bb/cs590/papers/amazon-dynamo-sosp2007.pdf (DeCandia et al., 2007)
- https://www.allthingsdistributed.com/2007/10/amazons_dynamo.html (2007)
- https://developer.hashicorp.com/consul/docs/v1.10.x/architecture/gossip
- https://hashicorp.com/blog/making-gossip-more-robust-with-lifeguard (2017)
- https://SEC.GOV/files/marketevents-report.pdf (SEC/CFTC, 2010)
- https://www.cftc.gov/idc/groups/public/@economicanalysis/documents/file/oce_flashcrash0314.pdf (Kirilenko et al.)
- https://www.energy.gov/sites/prod/files/oeprod/DocumentsandMedia/BlackoutFinal-Web.pdf (2004)
- https://emp.lbl.gov/publications/final-report-august-14-2003-blackout
- https://aws.amazon.com/message/65648/ (2011)
- https://www.infoq.com/news/2011/04/Amazon-EC2-Outage-Explained/ (2011)
- https://warez.kernelpanic.cafe/errata/linkdump/Element%20-%20Chat%20Export%20-%209-11-2022%20at%206-07-59%20PM/files/hotos21-s11-bronson-10-5-2021%20at%2012-42-24%20AM.pdf (Bronson et al., HotOS 2021)
- https://www.usenix.net/system/files/osdi22-huang-lexiang.pdf (Huang et al., OSDI 2022)
