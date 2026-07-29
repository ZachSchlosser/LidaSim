# LidaSim

Interactive charts for the **Simulating AI Policies** project.

🔗 **Live site:** <https://zachschlosser.github.io/LidaSim/>

## About

**LidaSim** is the data and visualization layer for **Wargaming AI Policies to Decrease Catastrophic Risk** — a global-scale simulation framework developed at [Lida Safety Research](https://www.lidasafety.org/research) in which actors (states, companies, and influential individuals) make strategic decisions as catastrophic AI scenarios unfold. Human participants can assume any role; other entities are played by LLM-based agents.

The simulation has a three-part mission: (1) a public **educational tool** for interactive exploration of catastrophic AI risk (going beyond passive resources like AI 2027), (2) a **research platform** for investigating policy questions and releasing open datasets of action/state sequences, and (3) a **policy forecasting tool** so politicians can estimate the impact of proposed AI regulations before enacting them. Each run follows a five-step loop — research question → actors and world state → mixed human/LLM simulation → accelerated LLM-only runs for statistics → expert retrospective.

Recognition: 🥇 First place at the Apart Research AI Governance Hackathon; *"LidaSim: Testing AI Policies With Persona-Based Simulations"* at the AIMII workshop (IASEAI, Paris, Feb 2026); earlier version at the AI & Societal Robustness Conference (Cambridge UK, Dec 2025).

This repository holds project source data: the 174-actor inventory (drawn from the AI 2027 and AI 2040 scenario documents), the AI-legislation × policy-impact map, and the persona-methodology comparison for the top 30 actors.

## Contents

| File | What it is |
|------|-----------|
| [`index.html`](index.html) | Landing page with links to the two charts below. |
| [`ai_legislation_impacts.html`](ai_legislation_impacts.html) | **AI Legislation × Policy Impact Areas** — interactive map of 26 current US state, federal, and EU AI laws/bills against the 19 policy-impact domains from the GPS-Bench framework. Filterable by catastrophic-only scope, impact area, jurisdiction, status, and text search. |
| [`ai_actors.html`](ai_actors.html) | **Actors in AI 2027 & AI 2040 Scenarios** — unified inventory of 174 entities with agency across both AI Futures Project scenario documents. |
| [`ai_actors.csv`](ai_actors.csv) | Source data for `ai_actors.html`. |
| [`build_deliverables.py`](build_deliverables.py) | Python generator for `ai_actors.html` and `ai_actors.csv` from a canonical `ACTORS` list and `DATASETS` catalog. Writes outputs to `~/Downloads/` — copy into the repo after re-running. |
| [`persona-comparison/`](persona-comparison/) | **Option 1 vs Option 2 Persona Profiles** — side-by-side comparison of two persona methodologies for the top 30 AI actors: CastBench baseline (12 fields) vs CastBench + HumanLM-style behavioral-trend paragraph + Rivera-style pairwise relationship matrix. Self-contained page, live at <https://zachschlosser.github.io/LidaSim/persona-comparison/>. |

## Taxonomy: 19 policy impact areas

Drawn from the GPS-Bench paper §12 (Layer 1), cross-referenced with Stage-3 benchmark trajectories (Layer 3) and Stage-3 pilot dimensions (Layer 4):

1. Employment & Labor `[L1, L3, L4]`
2. Prices & Cost of Living `[L1, L3, L4]`
3. Economic Growth & Productivity `[L1]`
4. Innovation & R&D `[L1, L3]`
5. Small Business & Competition `[L1]`
6. Government Fiscal Position `[L1]`
7. National Security `[L1]`
8. Public Safety & Catastrophic Risk `[L1, L3, L4]`
9. Healthcare `[L1]`
10. Education & Skills `[L1]`
11. Privacy & Civil Liberties `[L1, L4]`
12. Elections & Democracy `[L1]`
13. Crime & Cybersecurity `[L1]`
14. Inequality & Vulnerable Groups `[L1]`
15. Energy & Environment `[L1]`
16. Trade & Supply Chains `[L1, L3]`
17. International Cooperation `[L1]`
18. Developing-Country Equity `[L1]`
19. Public Trust & Epistemic Integrity `[L1]`

Layer tags: **L1** = GPS-Bench paper matrix (19 domains). **L3** = Stage-3 benchmark trajectory (5 trajectories). **L4** = Stage-3 pilot dimension (5 dims).

## Methodology

- **Bill tagging rule:** direct + likely second-order effects. Conservative bias. Per GPS-Bench `policy_dossier.py` no-jump rule, second-order effects are included only where the bill's mechanism plausibly activates them.
- **Catastrophic-relevant:** bills in chart categories 7 (Existential / Frontier AI) and 10 (Power Concentration & Race Dynamics) — 13 of 26.
- **Impact definitions:** GPS-Bench repo and paper first; OECD AI Principles and NIST AI RMF fill gaps where GPS-Bench has only template slots (most of the 19). Source lineage is shown per impact in the chart's taxonomy grid and in the definition text.
- **Bill data current as of:** 2026-07-24.

## Provenance

The 19-impact taxonomy and evidence-grading discipline originate from the GPS-Bench paper (Governance Pathway Simulator Benchmark), an anonymized submission for the AAAI Special Track on AI for Social Impact. See also: GPS-Bench's `policy_dossier.py`, which implements a 10-level master causal graph and 44-section report template that this chart's taxonomy is derived from.

## License

MIT — see [`LICENSE`](LICENSE) (or infer from the source repos).
