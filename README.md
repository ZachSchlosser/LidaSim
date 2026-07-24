# LidaSim

Interactive charts for the **Simulating AI Policies** project.

🔗 **Live site:** <https://zachschlosser.github.io/LidaSim/>

## Contents

| File | What it is |
|------|-----------|
| [`index.html`](index.html) | **AI Legislation × Policy Impact Areas** — interactive map of 25 current US state, federal, and EU AI laws/bills against the 19 policy-impact domains from the GPS-Bench framework. Filterable by catastrophic-only scope, impact area, jurisdiction, status, and text search. |
| [`ai_actors.html`](ai_actors.html) | **Actors in AI 2027 & AI 2040 Scenarios** — unified inventory of 174 entities with agency across both AI Futures Project scenario documents. Original source: [`ZachSchlosser/ai-actors`](https://github.com/ZachSchlosser/ai-actors). |
| [`ai_actors.csv`](ai_actors.csv) | Source data for `ai_actors.html`. |

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
- **Catastrophic-relevant:** bills in chart categories 7 (Existential / Frontier AI) and 10 (Power Concentration & Race Dynamics) — 12 of 25.
- **Impact definitions:** GPS-Bench repo and paper first; OECD AI Principles and NIST AI RMF fill gaps where GPS-Bench has only template slots (most of the 19). Source lineage is shown per impact in the chart's taxonomy grid and in the definition text.
- **Bill data current as of:** 2026-07-24.

## Provenance

The 19-impact taxonomy and evidence-grading discipline originate from the GPS-Bench paper (Governance Pathway Simulator Benchmark), an anonymized submission for the AAAI Special Track on AI for Social Impact. See also: GPS-Bench's `policy_dossier.py`, which implements a 10-level master causal graph and 44-section report template that this chart's taxonomy is derived from.

## License

MIT — see [`LICENSE`](LICENSE) (or infer from the source repos).
