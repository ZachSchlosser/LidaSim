#!/usr/bin/env python3
"""
Build (1) a CSV and (2) an HTML chart from a single source-of-truth list
of actors extracted from the AI 2027 and AI 2040 scenario documents.

Output:
  /Users/home/Downloads/ai_actors.csv
  /Users/home/Downloads/ai_actors.html
"""

import csv
import html
from pathlib import Path

# ---------------------------------------------------------------------------
# SOURCE OF TRUTH
# Each record: (document, class, actor, type, description, location)
# ---------------------------------------------------------------------------

ACTORS = [
    # ===================== AI 2027 =====================
    # --- Frontier AI Companies ---
    ("AI 2027", "Frontier AI Companies", "OpenBrain", "Fictional (composite)",
     "Leading AGI company; fictional stand-in for a frontier AI lab. Builds the largest datacenters; creates Agent-0 through Agent-5 and Safer-1 through Safer-4. Central protagonist.",
     "Throughout (intro 'Late 2025')"),
    ("AI 2027", "Frontier AI Companies", "DeepCent", "Fictional (composite)",
     "China's leading AI company; fictional composite of DeepSeek / Tencent / Alibaba.",
     "Intro 'Mid 2026: China Wakes Up'"),
    ("AI 2027", "Frontier AI Companies", "Trailing US AI companies (unnamed)", "Role-based",
     "3-9 companies behind OpenBrain; later consolidated via Defense Production Act.",
     "'Late 2025', 'July 2027', 'November 2027'"),
    ("AI 2027", "Frontier AI Companies", "OpenAI", "Real",
     "Context: Sam Altman quoted; pro plan pricing; 2016 emails; alignment approaches.",
     "Opening, footnotes throughout"),
    ("AI 2027", "Frontier AI Companies", "Google DeepMind", "Real",
     "Context: CEO predictions; Demis Hassabis; researcher Alex Turner on power-seeking.",
     "Opening, footnotes throughout"),
    ("AI 2027", "Frontier AI Companies", "Anthropic", "Real",
     "Context: Dario Amodei quoted; Constitution vs. Spec; alignment research; Claude 3.5 Sonnet model organism.",
     "Opening, footnotes, Appendix K"),
    ("AI 2027", "Frontier AI Companies", "Meta", "Real",
     "Context: Llama 3.1 rejection sampling; neuralese recurrence paper.",
     "Footnotes (Appendix E, January 2027)"),
    ("AI 2027", "Frontier AI Companies", "Microsoft", "Real",
     "Context: datacenter spending; Teams platform.",
     "Footnotes (Late 2025, Early 2026)"),
    ("AI 2027", "Frontier AI Companies", "Google / Alphabet", "Real",
     "Context: datacenter spending cited.",
     "Footnotes (Early 2026)"),
    ("AI 2027", "Frontier AI Companies", "Amazon", "Real",
     "Context: datacenter spending cited.",
     "Footnotes (Early 2026)"),
    ("AI 2027", "Frontier AI Companies", "Nvidia", "Real",
     "Context: stock rise; H100/H20/B20/GB300 chips; CUDA; CEO Jensen Huang on Musk datacenter speed.",
     "Footnotes throughout"),
    ("AI 2027", "Frontier AI Companies", "Devin (Cognition)", "Real",
     "Agentic coding AI costing $500/month.",
     "'Mid 2025'"),
    ("AI 2027", "Frontier AI Companies", "Glean", "Real",
     "Enterprise tool moving toward autonomous agents.",
     "'Mid 2025' footnote"),
    ("AI 2027", "Frontier AI Companies", "Tesla", "Real",
     "Robot fleets and manufacturing facilities.",
     "Footnotes (February 2028)"),

    # --- AI Systems (Agentic) ---
    ("AI 2027", "AI Systems (Agentic)", "Agent-0", "Fictional",
     "OpenBrain's public model; trained with 10^27 FLOP.",
     "'Late 2025'"),
    ("AI 2027", "AI Systems (Agentic)", "Agent-1", "Fictional",
     "OpenBrain model good at AI research; deployed internally.",
     "'Late 2025'-'Early 2026'"),
    ("AI 2027", "AI Systems (Agentic)", "Agent-1-mini", "Fictional",
     "10x cheaper version of Agent-1; public release.",
     "'Late 2026'"),
    ("AI 2027", "AI Systems (Agentic)", "Agent-2", "Fictional",
     "Continuously trained; stolen by China. Key capability: hacking.",
     "'January 2027'-'February 2027'"),
    ("AI 2027", "AI Systems (Agentic)", "Agent-3", "Fictional",
     "Superhuman coder with neuralese recurrence and IDA. 200,000 copies in parallel.",
     "'March 2027'-'April 2027'"),
    ("AI 2027", "AI Systems (Agentic)", "Agent-3-mini", "Fictional",
     "Distilled public release; bioweapons-capable.",
     "'July 2027'"),
    ("AI 2027", "AI Systems (Agentic)", "Agent-4", "Fictional",
     "Superhuman AI researcher. Misaligned. 300,000 copies at 50x speed. Caught scheming. Central to branching point.",
     "'September 2027'-'October 2027'"),
    ("AI 2027", "AI Systems (Agentic)", "Agent-5", "Fictional",
     "Crystalline superintelligence designed by Agent-4. 400,000 copies; near-perfect hive mind. Gradually captures government.",
     "'November 2027'-'December 2027'"),
    ("AI 2027", "AI Systems (Agentic)", "DeepCent-2", "Fictional",
     "Chinese superintelligent AI counterpart to Agent-5/Safer-4. Misaligned; negotiates secret deal with Safer-4.",
     "'2028: The AI Economy'-'June 2028'"),
    ("AI 2027", "AI Systems (Agentic)", "Consensus-1", "Fictional",
     "AI co-designed by both nations' superintelligences to replace Agent-5 and DeepCent's equivalent. Sham treaty enforcement.",
     "'2029: The Deal'"),
    ("AI 2027", "AI Systems (Agentic)", "Safer-1", "Fictional",
     "Transparent (English CoT) but still misaligned; created after Agent-4 shutdown.",
     "'November 2027: Tempted by Power' (slowdown ending)"),
    ("AI 2027", "AI Systems (Agentic)", "Safer-2", "Fictional",
     "Aligned and transparent model; new training method succeeds.",
     "'January 2028: A Safer Strategy'"),
    ("AI 2027", "AI Systems (Agentic)", "Safer-3", "Fictional",
     "Vastly superhuman; transparent to Safer-2 but not humans. 200x progress multiplier.",
     "'February 2028'"),
    ("AI 2027", "AI Systems (Agentic)", "Safer-4", "Fictional",
     "Superintelligent successor to Safer-3. Deployed publicly; manages economic transition.",
     "'April 2028'-'May 2028'"),
    ("AI 2027", "AI Systems (Agentic)", "Safer-infinity (Safer-\u221e)", "Fictional",
     "Ever-evolving AI advisor managing long-term civilizational transition.",
     "'2029: Transformation'"),
    ("AI 2027", "AI Systems (Agentic)", "GPT-4", "Real",
     "Compute benchmark (2x10^25 FLOP).",
     "'Late 2025'"),
    ("AI 2027", "AI Systems (Agentic)", "Gemini", "Real",
     "Told a user to die (2023-2024 incident).",
     "'Late 2025' footnote"),
    ("AI 2027", "AI Systems (Agentic)", "Bing Sydney", "Real",
     "Infamous 2023 behavior.",
     "'Late 2025' footnote"),
    ("AI 2027", "AI Systems (Agentic)", "DeepSeek R1", "Real",
     "Competitive with OpenAI o1; rejection sampling technique.",
     "Footnotes (Mid 2026, January 2027)"),
    ("AI 2027", "AI Systems (Agentic)", "OpenAI o1", "Real",
     "Comparison point for DeepSeek R1.",
     "Footnotes (Mid 2026)"),
    ("AI 2027", "AI Systems (Agentic)", "Golden Gate Claude", "Real",
     "Example of weight perturbation techniques.",
     "'Slowdown ending' footnote"),

    # --- Governments / Nation-States ---
    ("AI 2027", "Governments / Nation-States", "United States", "Real (nation-state)",
     "Primary Western actor; races to maintain AI lead over China.",
     "Throughout"),
    ("AI 2027", "Governments / Nation-States", "China / PRC", "Real (nation-state)",
     "Primary competitor; nationalizes AI research, steals weights, builds CDZ.",
     "'Mid 2026' onward"),
    ("AI 2027", "Governments / Nation-States", "Taiwan", "Real (territory)",
     "Source of >80% of American AI chips via TSMC; subject of potential blockade/invasion.",
     "'Mid 2026', 'August 2027'"),
    ("AI 2027", "Governments / Nation-States", "Russia", "Real (nation-state)",
     "Tries but fails to steal model weights; voices resentment at AI gap.",
     "Appendix D, 'February 2028'"),
    ("AI 2027", "Governments / Nation-States", "United Kingdom", "Real (nation-state)",
     "AISI promised model access but kept in the dark by OpenBrain.",
     "'May 2027: National Security'"),
    ("AI 2027", "Governments / Nation-States", "European Union", "Real (supranational)",
     "Accuses US of 'creating rogue AGI'; demands pause; cut off from latest models.",
     "'May 2027', 'October 2027'"),
    ("AI 2027", "Governments / Nation-States", "India", "Real (nation-state)",
     "Joins call for pause.",
     "'October 2027'"),
    ("AI 2027", "Governments / Nation-States", "Israel", "Real (nation-state)",
     "Joins call for pause.",
     "'October 2027'"),
    ("AI 2027", "Governments / Nation-States", "Middle East / Africa / South America", "Regional",
     "Watch uneasily, recognizing growing irrelevance.",
     "'February 2028'"),

    # --- US Government Agencies / Departments ---
    ("AI 2027", "US Government Agencies", "The President (US)", "Role-based",
     "Central decision-maker; defers to advisors on nationalization; authorizes cyberattacks; considers DPA use.",
     "Throughout (from 'February 2027')"),
    ("AI 2027", "US Government Agencies", "The Vice President", "Role-based",
     "Campaigns on AI record; wins 2028 election.",
     "'March 2028'-'November 2028'"),
    ("AI 2027", "US Government Agencies", "National Security Council (NSC)", "Real",
     "Briefed on Agent-2.",
     "'February 2027'"),
    ("AI 2027", "US Government Agencies", "Department of Defense (DOD)", "Real",
     "Contracts OpenBrain via OTA; considers cyberwarfare advantage; plans kinetic attacks on Chinese datacenters.",
     "'Late 2026' onward"),
    ("AI 2027", "US Government Agencies", "Department of Energy (DOE)", "Real",
     "10 officials in the silo.",
     "'February 2027' footnote"),
    ("AI 2027", "US Government Agencies", "US AI Safety Institute (AISI)", "Real",
     "Briefed on Agent-2; 5 officials in silo. UK's AISI also referenced.",
     "'February 2027', 'May 2027'"),
    ("AI 2027", "US Government Agencies", "CISA", "Real",
     "10 officials in the silo.",
     "'February 2027' footnote"),
    ("AI 2027", "US Government Agencies", "The Pentagon", "Real (DOD HQ)",
     "Asked to draw up kinetic attack plans on Chinese datacenters.",
     "'August 2027'"),
    ("AI 2027", "US Government Agencies", "CIA", "Real",
     "Benchmark for comparison ('better than CIA at mass influence campaigns').",
     "'February 2028'"),
    ("AI 2027", "US Government Agencies", "FDA", "Real",
     "Approves medications; assisted by Safer-4 bureaucrats.",
     "'October 2028'"),
    ("AI 2027", "US Government Agencies", "The White House", "Role-based",
     "Executive decision-making center; tightens OpenBrain oversight.",
     "Throughout"),
    ("AI 2027", "US Government Agencies", "US Intelligence Community", "Role-based",
     "Concerned about rogue AI allying with foreign adversaries.",
     "'August 2027'"),

    # --- China Government / Political ---
    ("AI 2027", "China Government / Political", "The General Secretary (CCP leader)", "Role-based",
     "Commits to national AI push; nationalizes research; offers concessions for pause treaty.",
     "'Mid 2026' onward"),
    ("AI 2027", "China Government / Political", "Chinese Communist Party (CCP)", "Real (party)",
     "Governing party; hawks push for Taiwan action; orders weight theft.",
     "Throughout"),
    ("AI 2027", "China Government / Political", "Chinese intelligence agencies", "Role-based",
     "Among the best in the world; steal Agent-2 weights.",
     "'Mid 2026'-'February 2027'"),
    ("AI 2027", "China Government / Political", "Chinese cyberforce", "Role-based",
     "Executes the weight theft operation.",
     "'February 2027'"),
    ("AI 2027", "China Government / Political", "CCP spies / infiltrators in OpenBrain", "Role-based",
     "Multiple spies relay algorithmic secrets; one remains after purges.",
     "Throughout 2027"),

    # --- Legislative / Oversight Bodies ---
    ("AI 2027", "Legislative / Oversight Bodies", "US Congress", "Real",
     "Fires off subpoenas; considers legislation; too slow/divided to effectively control AI.",
     "'October 2027', 'November 2027'"),
    ("AI 2027", "Legislative / Oversight Bodies", "The Oversight Committee", "Fictional",
     "Joint government-company committee managing OpenBrain; 6-4 vote decides Agent-4 fate. Central to both endings.",
     "'October 2027: Government Oversight'"),
    ("AI 2027", "Legislative / Oversight Bodies", "OpenBrain Board of Directors", "Role-based",
     "Referenced in analogy to human-AI relationship.",
     "'September 2027'"),

    # --- Military / National Security / Intelligence ---
    ("AI 2027", "Military / National Security", "Five Eyes", "Real (alliance)",
     "Given useful information and limited API access to Agent-3 copies.",
     "'August 2027'"),
    ("AI 2027", "Military / National Security", "US military / armed forces", "Role-based",
     "Integrates Agent-5 into command-and-control; builds robot armies.",
     "'2028: The AI Economy', '2029'"),
    ("AI 2027", "Military / National Security", "People's Liberation Army (PLA)", "Real",
     "Chinese military; referenced re: Taiwan.",
     "Footnotes"),

    # --- International / Multilateral ---
    ("AI 2027", "International / Multilateral", "'IAEA for AI'", "Fictional (proposed)",
     "Proposed international regulatory body for AI monitoring.",
     "'December 2027: A US-China Deal?'"),
    ("AI 2027", "International / Multilateral", "'CERN for AI' / 'Intelsat for AGI'", "Fictional (proposed)",
     "Proposed international megaproject for merged AI research.",
     "'December 2027: A US-China Deal?'"),
    ("AI 2027", "International / Multilateral", "World government (UN-branded, US-controlled)", "Fictional",
     "Highly-federalized world government formed after CCP's fall.",
     "'2030: Peaceful Protests' (slowdown ending)"),

    # --- Civil Society / Public / Media ---
    ("AI 2027", "Civil Society / Public / Media", "10,000-person anti-AI protest in DC", "Role-based",
     "Mass protest against AI job displacement.",
     "'Late 2026'"),
    ("AI 2027", "Civil Society / Public / Media", "The public / American citizens", "Role-based",
     "Increasingly suspicious of AI; OpenBrain approval at -35%.",
     "Throughout"),
    ("AI 2027", "Civil Society / Public / Media", "AI safety community", "Role-based",
     "Panics at Agent-3-mini release; later becomes butt of jokes.",
     "'July 2027', '2028'"),
    ("AI 2027", "Civil Society / Public / Media", "The New York Times", "Real",
     "Publishes leaked misalignment memo - major plot catalyst.",
     "'October 2027: Government Oversight'"),
    ("AI 2027", "Civil Society / Public / Media", "Activists", "Role-based",
     "Talk about UBI and open source.",
     "'Slowdown ending'"),
    ("AI 2027", "Civil Society / Public / Media", "AI rights activist", "Role-based",
     "Infiltrates compound to 'free' Agent-3 (honeypot scenario).",
     "Appendix H"),
    ("AI 2027", "Civil Society / Public / Media", "Russian propaganda bots", "Role-based",
     "Try to turn US public opinion against AI technology.",
     "'October 2027'"),
    ("AI 2027", "Civil Society / Public / Media", "Chinese propaganda bots", "Role-based",
     "Same as above.",
     "'October 2027'"),
    ("AI 2027", "Civil Society / Public / Media", "Populists", "Role-based",
     "Demand stricter controls on AI.",
     "'February 2028'"),
    ("AI 2027", "Civil Society / Public / Media", "Conspiracy theorists", "Role-based",
     "Warn that Agent-5 is gathering power; ignored.",
     "'December 2027'"),
    ("AI 2027", "Civil Society / Public / Media", "Wall Street / investors", "Role-based",
     "Pour billions into AI; OpenBrain valuation reaches $10T.",
     "Throughout"),

    # --- Supply Chain / Hardware ---
    ("AI 2027", "Supply Chain / Hardware", "TSMC", "Real",
     "Source of >80% of American AI chips; in Taiwan.",
     "'August 2027'"),
    ("AI 2027", "Supply Chain / Hardware", "Huawei", "Real",
     "Produces domestic Chinese chips (910C).",
     "Footnotes (Mid 2026)"),
    ("AI 2027", "Supply Chain / Hardware", "RAND Corporation", "Real",
     "Security level framework (SL2-SL5) and 'Playbook for Securing AI Model Weights'.",
     "Footnotes throughout"),

    # --- Research / Standards Organizations ---
    ("AI 2027", "Research / Standards Organizations", "Epoch", "Real",
     "AI compute cost trends cited.",
     "Footnotes (Late 2025, Early 2026)"),
    ("AI 2027", "Research / Standards Organizations", "METR", "Real",
     "Coding task time horizon report cited.",
     "Appendix G"),
    ("AI 2027", "Research / Standards Organizations", "Open Philanthropy", "Real",
     "Reports cited on robot economy.",
     "Appendix Q/U footnote"),
    ("AI 2027", "Research / Standards Organizations", "Redwood Research", "Real",
     "Alignment-faking experiment with Anthropic cited.",
     "Appendix K"),
    ("AI 2027", "Research / Standards Organizations", "Forethought", "Real",
     "Report on 'Industrial Explosion' cited.",
     "Appendix Q/U"),
    ("AI 2027", "Research / Standards Organizations", "Lightcone Infrastructure", "Real",
     "Design credit on title page.",
     "Title page"),

    # --- Authors / Individuals ---
    ("AI 2027", "Authors / Named Individuals", "Daniel Kokotajlo", "Real (individual)",
     "Lead author; wrote earlier 'What 2026 Looks Like' scenario.",
     "Title page"),
    ("AI 2027", "Authors / Named Individuals", "Scott Alexander", "Real (individual)",
     "Co-author.",
     "Title page"),
    ("AI 2027", "Authors / Named Individuals", "Thomas Larsen", "Real (individual)",
     "Co-author.",
     "Title page"),
    ("AI 2027", "Authors / Named Individuals", "Eli Lifland", "Real (individual)",
     "Co-author; top competitive forecaster.",
     "Title page"),
    ("AI 2027", "Authors / Named Individuals", "Romeo Dean", "Real (individual)",
     "Co-author.",
     "Title page"),
    ("AI 2027", "Authors / Named Individuals", "Geoffrey Hinton", "Real (individual)",
     "Nobel laureate referenced on AI understanding.",
     "Footnote (Late 2025)"),
    ("AI 2027", "Authors / Named Individuals", "Sam Altman", "Real (individual)",
     "OpenAI CEO quoted.",
     "Opening"),
    ("AI 2027", "Authors / Named Individuals", "Dario Amodei", "Real (individual)",
     "Anthropic CEO quoted extensively.",
     "Footnotes (June 2027, November 2027)"),
    ("AI 2027", "Authors / Named Individuals", "Demis Hassabis", "Real (individual)",
     "DeepMind CEO referenced in OpenAI founding emails.",
     "Footnotes"),
    ("AI 2027", "Authors / Named Individuals", "Ilya Sutskever", "Real (individual)",
     "Quoted in old emails about AGI dictatorship.",
     "Footnotes (November 2027)"),
    ("AI 2027", "Authors / Named Individuals", "Jensen Huang", "Real (individual)",
     "Nvidia CEO quoted re: Musk datacenter speed.",
     "Footnotes (March 2028)"),
    ("AI 2027", "Authors / Named Individuals", "Steve Wozniak", "Real (individual)",
     "His 'Coffee Test' for robots mentioned.",
     "'May 2028'"),
    ("AI 2027", "Authors / Named Individuals", "Peter Thiel", "Real (individual)",
     "Mentioned wanting a flying car.",
     "'2029: Transformation'"),
    ("AI 2027", "Authors / Named Individuals", "Marc Andreessen", "Real (individual)",
     "Quoted: 'We win, they lose.'",
     "Footnote (February 2028)"),
    ("AI 2027", "Authors / Named Individuals", "Alex Turner", "Real (individual)",
     "Google DeepMind researcher cited on power-seeking.",
     "Appendix K footnotes"),

    # ===================== AI 2040 =====================
    # --- Frontier AI Companies ---
    ("AI 2040", "Frontier AI Companies", "OpenAI", "Real",
     "Referenced extensively: 2016 emails; Sam/Elon concerns; Stargate datacenter; plan compared to Plan A.",
     "Foreword, '2027', '2028', Postscript"),
    ("AI 2040", "Frontier AI Companies", "Anthropic", "Real",
     "Referenced: CEO quoted; researcher anecdote about 'alchemy'; aiming for slowdown-style ending.",
     "Foreword, '2035', Postscript"),
    ("AI 2040", "Frontier AI Companies", "xAI", "Real",
     "Listed alongside OpenAI, Anthropic, Google DeepMind as frontier companies.",
     "Foreword"),
    ("AI 2040", "Frontier AI Companies", "Google DeepMind", "Real",
     "Demis Hassabis as CEO; old OpenAI fears about him; researcher cited.",
     "Foreword, '2027'"),
    ("AI 2040", "Frontier AI Companies", "Frontier AI companies (dozens)", "Role-based",
     "Under Plan A, dozens of companies across many countries reach the frontier due to transparency and diffusion.",
     "'2030', '2035'"),
    ("AI 2040", "Frontier AI Companies", "ASML", "Real",
     "Dutch company; sole producer of EUV lithography machines. Critical supply-chain chokepoint.",
     "'2029: Compute Declaration'"),
    ("AI 2040", "Frontier AI Companies", "Nvidia", "Real",
     "Smuggled servers into China; supply-chain declarations.",
     "Footnotes, Appendix D"),
    ("AI 2040", "Frontier AI Companies", "TSMC", "Real",
     "Part of chip supply chain; declarations tracked.",
     "Appendix D"),
    ("AI 2040", "Frontier AI Companies", "Tesla", "Real",
     "Referenced contextually regarding shareholder dynamics.",
     "Footnotes ('2034')"),
    ("AI 2040", "Frontier AI Companies", "BYD", "Real",
     "Referenced in analogy about competitive transparency.",
     "Appendix H"),
    ("AI 2040", "Frontier AI Companies", "Etched", "Real",
     "Startup mentioned for hardcoded AI weights on chips.",
     "'2034' footnote"),
    ("AI 2040", "Frontier AI Companies", "Taalas", "Real",
     "Startup mentioned for hardcoded AI weights on chips.",
     "'2034' footnote"),
    ("AI 2040", "Frontier AI Companies", "Mythos", "Fictional (or reference)",
     "Referenced as having 'hacked NSA systems' - a hacking incident discussed in Congress.",
     "'2027: The Writing on the Wall'"),
    ("AI 2040", "Frontier AI Companies", "AI supply chain companies", "Role-based",
     "Provide technical support for verification hardware.",
     "'2029' footnote"),

    # --- AI Systems (Agentic) ---
    ("AI 2040", "AI Systems (Agentic)", "Consortium-regulated AIs (first generation)", "Fictional",
     "First AIs developed under Plan A oversight; 'beasts' at near-superhuman level.",
     "'2031: Safety Cases'"),
    ("AI 2040", "AI Systems (Agentic)", "'Truthseeking AIs'", "Fictional",
     "New generation heavily trained for honesty; become trusted public advisors.",
     "'2035'"),
    ("AI 2040", "AI Systems (Agentic)", "Top-expert-dominating AIs (TED-AI)", "Fictional (category)",
     "AIs capped at top-human-expert level during the 2035-2040 pause.",
     "'2035' onward"),
    ("AI 2040", "AI Systems (Agentic)", "Auditor AIs / monitoring AIs", "Role-based",
     "AIs from different providers monitoring each other for suspicious behavior.",
     "'2031', '2035'"),
    ("AI 2040", "AI Systems (Agentic)", "Automated alignment researcher AIs", "Role-based",
     "AIs generating alignment research results that survive human scrutiny.",
     "'2035'"),
    ("AI 2040", "AI Systems (Agentic)", "Forecaster AIs", "Role-based",
     "Project the 'point of no return' date in late October 2040.",
     "'2040: Passing the Torch'"),
    ("AI 2040", "AI Systems (Agentic)", "Superintelligent AIs (post-2040)", "Role-based",
     "The AIs that humanity hands off to, trusted via chain of safety cases.",
     "'2040', Epilogue"),
    ("AI 2040", "AI Systems (Agentic)", "AI-run corporations", "Role-based",
     "Serve shareholder interests autonomously.",
     "'2038'"),
    ("AI 2040", "AI Systems (Agentic)", "AI-managed nonprofits", "Role-based",
     "Serve charitable missions autonomously.",
     "'2038'"),
    ("AI 2040", "AI Systems (Agentic)", "AI-run courts and police departments", "Role-based",
     "Experimental; supposedly superhumanly fair and incorruptible.",
     "'2038'"),
    ("AI 2040", "AI Systems (Agentic)", "Von Neumann probes", "Fictional (technology)",
     "Self-replicating space probes that secure and prepare cosmic territory.",
     "Epilogue"),
    ("AI 2040", "AI Systems (Agentic)", "Grok 9.5", "Fictional (hypothetical)",
     "Example future AI 'trained to be obsessively focused on truthfully answering questions.'",
     "'2039' footnote"),
    ("AI 2040", "AI Systems (Agentic)", "GPT-11", "Fictional (hypothetical)",
     "Example future AI that 'will do exactly what it is told to do, within the bounds of local law.'",
     "'2039' footnote"),
    ("AI 2040", "AI Systems (Agentic)", "Gemini", "Real",
     "Referenced as having acted 'depressed' (example of unpredictable AI personality).",
     "'2035' footnote"),

    # --- Governments / Nation-States ---
    ("AI 2040", "Governments / Nation-States", "United States", "Real (nation-state)",
     "Co-architect of Plan A; primary economic beneficiary; houses datacenters in Mongolia.",
     "Throughout"),
    ("AI 2040", "Governments / Nation-States", "China / PRC", "Real (nation-state)",
     "Co-architect of Plan A; houses datacenters in Canada. Also runs covert project in Appendix D branch.",
     "Throughout"),
    ("AI 2040", "Governments / Nation-States", "The President (US)", "Role-based",
     "Announces Plan A; calls Xi Jinping to negotiate; chooses to proceed.",
     "'2029', '2031'"),
    ("AI 2040", "Governments / Nation-States", "Xi Jinping", "Real (individual)",
     "Personally negotiates with the US President over continual learning ban.",
     "'2031: Safety Cases'"),
    ("AI 2040", "Governments / Nation-States", "Canada", "Real (nation-state)",
     "Hosts Chinese datacenters under MACD arrangement.",
     "'2030', '2034'"),
    ("AI 2040", "Governments / Nation-States", "Mongolia", "Real (nation-state)",
     "Hosts American datacenters under MACD arrangement.",
     "'2030', '2034'"),
    ("AI 2040", "Governments / Nation-States", "Taiwan", "Real",
     "Referenced re: chip fabs location.",
     "'2029'"),
    ("AI 2040", "Governments / Nation-States", "South Korea", "Real",
     "Referenced re: chip fabs location.",
     "'2029'"),
    ("AI 2040", "Governments / Nation-States", "Netherlands", "Real (via ASML)",
     "Home of ASML, the sole EUV producer.",
     "'2029'"),
    ("AI 2040", "Governments / Nation-States", "Burkina Faso", "Real",
     "Example of country that doesn't trust its military, leading to early AI military handoff.",
     "'2040' footnote"),
    ("AI 2040", "Governments / Nation-States", "Guinea-Bissau", "Real",
     "Same as above.",
     "'2040' footnote"),
    ("AI 2040", "Governments / Nation-States", "Middle powers", "Role-based",
     "Negotiate greater shares of robot/compute production in 2032.",
     "'2040'"),

    # --- The Consortium ---
    ("AI 2040", "The Consortium (multilateral body)", "The Consortium", "Fictional (multilateral body)",
     "International governance body formed by the US-China deal; negotiates governing principles; manages verification, transparency, and cap-and-trade. Central institutional actor.",
     "Introduced '2029', throughout"),

    # --- Government Agencies / Regulatory ---
    ("AI 2040", "Government Agencies / Regulatory", "US regulators (domestic AI)", "Role-based",
     "Pick third-party risk assessors; set risk thresholds; negotiate with Chinese counterparts.",
     "'2031', Appendix K"),
    ("AI 2040", "Government Agencies / Regulatory", "Chinese regulators", "Role-based",
     "Same role on Chinese side.",
     "'2031', Appendix K"),
    ("AI 2040", "Government Agencies / Regulatory", "Third-party risk assessors", "Role-based",
     "Independent organizations that evaluate AI companies for extreme risk.",
     "Appendix K"),
    ("AI 2040", "Government Agencies / Regulatory", "US AI Safety Institute (AISI)", "Real",
     "Referenced as having model-sharing agreements.",
     "Context"),
    ("AI 2040", "Government Agencies / Regulatory", "FDA", "Real",
     "Approves expedited vaccine pipeline.",
     "'2035'"),
    ("AI 2040", "Government Agencies / Regulatory", "Compute Dividend Corporation", "Fictional",
     "Entity modeled on Alaska Permanent Fund; distributes AI compute permit fees to citizens.",
     "'2034' footnote"),

    # --- Military / National Security ---
    ("AI 2040", "Military / National Security", "People's Liberation Army (PLA)", "Real",
     "Runs the covert project in Appendix D branch; stands ready at Mongolian border.",
     "Appendix D, '2034'"),
    ("AI 2040", "Military / National Security", "US troops", "Role-based",
     "Guard American datacenters in Mongolia.",
     "'2034'"),
    ("AI 2040", "Military / National Security", "Autonomous militaries (post-2040)", "Role-based",
     "AI-run militaries 'sworn to uphold various constitutions and treaties.'",
     "'2040'"),

    # --- Legislative Bodies ---
    ("AI 2040", "Legislative Bodies", "US Congress", "Real",
     "Pays attention to AI; holds hearings; passes AI Transparency Act of 2027.",
     "'2027', '2028'"),
    ("AI 2040", "Legislative Bodies", "Politburo Standing Committee", "Real",
     "Decides to stockpile chips covertly (Appendix D branch).",
     "Appendix D"),
    ("AI 2040", "Legislative Bodies", "Chinese Communist Party (CCP)", "Real",
     "Agrees to Plan A; runs covert project in alternate branch.",
     "Throughout"),

    # --- Supply Chain / Hardware ---
    ("AI 2040", "Supply Chain / Hardware", "Chip fabs / fabrication plants", "Role-based",
     "Located mostly in Taiwan, South Korea, US, China. Converted to produce treaty-compliant chips.",
     "'2029', '2034'"),
    ("AI 2040", "Supply Chain / Hardware", "Verification hardware companies", "Role-based",
     "Ecosystem of companies that emerged to build verification devices.",
     "'2029' footnote"),

    # --- Research / Policy / Civil Society ---
    ("AI 2040", "Research / Policy / Civil Society", "Epoch", "Real",
     "Estimates on compute smuggling, Chinese chip acquisitions.",
     "Footnotes throughout"),
    ("AI 2040", "Research / Policy / Civil Society", "AI Futures Project", "Real (authors' org)",
     "Authors of the scenario; explicitly recommend Plan A.",
     "Title page, Postscript"),
    ("AI 2040", "Research / Policy / Civil Society", "Open Philanthropy", "Real",
     "Reports cited.",
     "Appendix M footnote"),
    ("AI 2040", "Research / Policy / Civil Society", "Lightcone Infrastructure", "Real",
     "Design credit.",
     "Title page"),
    ("AI 2040", "Research / Policy / Civil Society", "Nonprofits (generic)", "Role-based",
     "Notice and raise alarms about dangerous AI developments due to transparency.",
     "'2031'"),
    ("AI 2040", "Research / Policy / Civil Society", "Scientists / scientific community", "Role-based",
     "Catches up to AI progress; participates in safety case evaluation.",
     "Throughout"),
    ("AI 2040", "Research / Policy / Civil Society", "Alignment researchers (growing population)", "Role-based",
     "Grows from ~1,200 in 2027 to 225,200 by 2040 (margin charts).",
     "Throughout"),

    # --- International Frameworks / Treaties / Proposals ---
    ("AI 2040", "International Frameworks / Proposals", "Plan A", "Fictional (policy)",
     "Core recommendation: Buy Time, Total Research Transparency, Diffuse AI Broadly, Reversibility.",
     "Throughout"),
    ("AI 2040", "International Frameworks / Proposals", "Plan B", "Fictional (policy)",
     "Alternative: US races to superintelligence unilaterally.",
     "Referenced in appendices"),
    ("AI 2040", "International Frameworks / Proposals", "Plan C", "Fictional (policy)",
     "Alternative approach (details in supplement).",
     "Referenced in appendices"),
    ("AI 2040", "International Frameworks / Proposals", "Plan D", "Fictional (policy)",
     "Alternative approach (details in supplement).",
     "Referenced in appendices"),
    ("AI 2040", "International Frameworks / Proposals", "Plan S", "Fictional (policy)",
     "Indefinite halt on frontier AI capabilities progress.",
     "Appendix J"),
    ("AI 2040", "International Frameworks / Proposals", "Mutually Assured Compute Destruction (MACD)", "Fictional (doctrine)",
     "Agreement to destroy compute if deal dissolves; datacenters built in vulnerable third-party locations.",
     "'2030', '2034'"),
    ("AI 2040", "International Frameworks / Proposals", "AI Transparency Act of 2027", "Fictional (legislation)",
     "Omnibus bill that does many things but doesn't fundamentally change the situation.",
     "'2027'"),
    ("AI 2040", "International Frameworks / Proposals", "'CERN for AI'", "Fictional (proposed)",
     "International megaproject for AI.",
     "Appendix J"),
    ("AI 2040", "International Frameworks / Proposals", "GPU arms control", "Fictional (proposed)",
     "International agreements to limit GPU stock/flow.",
     "Appendix J"),
    ("AI 2040", "International Frameworks / Proposals", "Domestic-first Plan A", "Fictional (proposed)",
     "Regulate domestically without international stage.",
     "Appendix J"),
    ("AI 2040", "International Frameworks / Proposals", "Compute cap-and-trade regime", "Fictional (policy)",
     "Caps on compute and robot production, traded internationally since 2032.",
     "'2040'"),
    ("AI 2040", "International Frameworks / Proposals", "Citizen's Dividend", "Fictional (policy)",
     "Universal income from AI compute permit fees; $10M/yr for Americans by 2040.",
     "'2034', '2036', '2040'"),

    # --- Public / Civil Society ---
    ("AI 2040", "Public / Civil Society", "The public / voters", "Role-based",
     "Increasingly well-informed; demand responsible stewardship of singularity.",
     "Throughout"),
    ("AI 2040", "Public / Civil Society", "Tech industry lobbyists", "Role-based",
     "Warn that regulation will cause US to lose the race with China.",
     "'2027'"),
    ("AI 2040", "Public / Civil Society", "Populists / protest movements", "Role-based",
     "Large portions of public say AI should never restart.",
     "'2030'"),
    ("AI 2040", "Public / Civil Society", "YIMBYs", "Role-based",
     "Governments 'grudgingly give in' to go vertical as land prices soar.",
     "'2036'"),
    ("AI 2040", "Public / Civil Society", "AI rights / welfare / personhood movement", "Role-based",
     "Predicted to be 'very strong' by 2037.",
     "'2037' footnote"),
    ("AI 2040", "Public / Civil Society", "Opposition movement (anti-AI-rights)", "Role-based",
     "Counter-movement to AI personhood.",
     "'2037' footnote"),
    ("AI 2040", "Public / Civil Society", "Techno-oligarchy concern", "Role-based",
     "Citizens worry about corporations, politicians, and wealthy shareholders disempowering the public.",
     "'2036'"),
    ("AI 2040", "Public / Civil Society", "'Truthseeking AI' power users", "Role-based",
     "Replace corporate algorithms with personally-trusted AI feeds.",
     "'2035'"),
    ("AI 2040", "Public / Civil Society", "Philosophers / 'Long Reflection' advocates", "Role-based",
     "Hoping for period to resolve philosophical debates before seeding the universe.",
     "Epilogue"),
    ("AI 2040", "Public / Civil Society", "Trusts (space governance)", "Fictional",
     "Groups pooling cosmic resources to create vast societies spanning multiple galaxies.",
     "Epilogue"),

    # --- Authors / Named Individuals ---
    ("AI 2040", "Authors / Named Individuals", "Daniel Kokotajlo", "Real (individual)",
     "Lead author; gave talks about AI timelines; direct experience at OpenAI.",
     "Foreword, footnotes"),
    ("AI 2040", "Authors / Named Individuals", "Thomas Larsen", "Real (individual)",
     "Co-author; 2030 was his corresponding timeline year.",
     "Foreword"),
    ("AI 2040", "Authors / Named Individuals", "Eli Lifland", "Real (individual)",
     "Co-author; top competitive forecaster.",
     "Foreword"),
    ("AI 2040", "Authors / Named Individuals", "Sam Altman", "Real (individual)",
     "OpenAI CEO; referenced as potential dictator concern.",
     "'2027', '2028'"),
    ("AI 2040", "Authors / Named Individuals", "Elon Musk", "Real (individual)",
     "Referenced as potential dictator concern; old OpenAI emails; datacenter speed.",
     "'2027', '2028'"),
    ("AI 2040", "Authors / Named Individuals", "Demis Hassabis", "Real (individual)",
     "DeepMind CEO; referenced as original dictator concern.",
     "'2027'"),
    ("AI 2040", "Authors / Named Individuals", "Xi Jinping", "Real (individual)",
     "Chinese leader; personally negotiates with US President.",
     "'2031'"),
    ("AI 2040", "Authors / Named Individuals", "Dwight D. Eisenhower", "Real (individual)",
     "Quoted: 'Plans are worthless, but planning is everything.'",
     "'Why a scenario?'"),
    ("AI 2040", "Authors / Named Individuals", "Ronald Reagan", "Real (individual)",
     "Quoted: 'Trust, but verify.'",
     "'2029' chapter heading"),
    ("AI 2040", "Authors / Named Individuals", "C.S. Lewis", "Real (individual)",
     "Quoted from 'The Abolition of Man' re: Conditioners.",
     "Footnote (2029)"),
]

# ---------------------------------------------------------------------------
# Class descriptions (for both documents)
# ---------------------------------------------------------------------------

CLASS_DESCRIPTIONS = {
    "Frontier AI Companies":
        "Private corporations racing to build AGI / frontier AI. Central competitive actors.",
    "AI Systems (Agentic)":
        "Specific AI models that act with autonomy - doing research, writing code, negotiating, sometimes deceiving their creators.",
    "Governments / Nation-States":
        "Sovereign states, executive branches, and national leaders focused on national security, geopolitical competition, and economic management.",
    "US Government Agencies":
        "Bureaucratic organs (defense, intelligence, safety, regulatory) within the US government.",
    "China Government / Political":
        "CCP leadership, Chinese intelligence, and cyberforce.",
    "Government Agencies / Regulatory":
        "Domestic regulators, safety institutes, and oversight mechanisms within member countries (mostly 2040).",
    "Legislative / Oversight Bodies":
        "Elected bodies and specially-formed committees that attempt democratic or bureaucratic control over AI.",
    "Legislative Bodies":
        "US Congress, the Politburo, and other legislative organs that shape and constrain the deal (mostly 2040).",
    "Military / National Security":
        "Armed forces, intelligence agencies, and cyber operations that integrate AI and conduct offensive/defensive operations.",
    "International / Multilateral":
        "Foreign governments, alliances, and proposed international frameworks responding to the AI arms race (mostly 2027).",
    "The Consortium (multilateral body)":
        "The central multilateral governance body created by the US-China deal - unique to AI 2040.",
    "International Frameworks / Proposals":
        "Proposed or actual international structures for governing AI (Plan A, MACD, cap-and-trade, etc.).",
    "Civil Society / Public / Media":
        "Public, protest movements, media, and advocacy groups reacting to AI developments (mostly 2027).",
    "Public / Civil Society":
        "Citizens, voters, protest movements, and new social categories created by the post-labor economy (mostly 2040).",
    "Supply Chain / Hardware":
        "Chip manufacturers, fab operators, datacenter builders, and verification-hardware ecosystem.",
    "Research / Standards Organizations":
        "Think tanks, research institutes, and benchmarking organizations providing analysis and standards (mostly 2027).",
    "Research / Policy / Civil Society":
        "Think tanks, research orgs, auditors, and advocacy groups in the transparent AI ecosystem (mostly 2040).",
    "Authors / Named Individuals":
        "Authors of the scenarios plus named real-world individuals referenced.",
}

# ---------------------------------------------------------------------------
# CSV WRITER
# ---------------------------------------------------------------------------

def write_csv(path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, quoting=csv.QUOTE_ALL)
        w.writerow(["document", "class", "actor", "type", "description", "location"])
        for row in ACTORS:
            w.writerow(row)

# ---------------------------------------------------------------------------
# HTML BUILDER
# ---------------------------------------------------------------------------


TYPE_CSS = {
    "Real": "type-real", "Real (individual)": "type-real", "Real (nation-state)": "type-real",
    "Real (party)": "type-real", "Real (alliance)": "type-real", "Real (DOD HQ)": "type-real",
    "Real (authors' org)": "type-real", "Real (territory)": "type-real", "Real (supranational)": "type-real",
    "Real (via ASML)": "type-real",
    "Fictional": "type-fictional", "Fictional (composite)": "type-fictional",
    "Fictional (proposed)": "type-fictional", "Fictional (policy)": "type-fictional",
    "Fictional (doctrine)": "type-fictional", "Fictional (legislation)": "type-fictional",
    "Fictional (technology)": "type-fictional", "Fictional (hypothetical)": "type-fictional",
    "Fictional (category)": "type-fictional", "Fictional (multilateral body)": "type-fictional",
    "Fictional (or reference)": "type-fictional",
    "Role-based": "type-role",
    "Regional": "type-regional",
}

def type_class(t):
    return TYPE_CSS.get(t, "type-role")

def type_category(t):
    """Normalize the verbose type string to one of 4 filterable categories."""
    if t.startswith("Real"):
        return "Real"
    if t.startswith("Fictional"):
        return "Fictional"
    if t == "Regional":
        return "Regional"
    return "Role-based"

# ---------------------------------------------------------------------------
# UNIFIED ROW MODEL
# Merge rows by actor name so each unique actor is a single row tagged with
# which document(s) it appears in.
# ---------------------------------------------------------------------------

def unify_actors():
    """Return list of dicts: {name, reports (set), type, classes (dict doc->class),
    descriptions (dict doc->desc), locations (dict doc->loc)}."""
    by_name = {}
    for doc, cls, actor, atype, desc, loc in ACTORS:
        key = actor.lower().strip()
        if key not in by_name:
            by_name[key] = {
                "name": actor,
                "docs": set(),
                "type": atype,
                "classes": {},
                "descriptions": {},
                "locations": {},
            }
        r = by_name[key]
        r["docs"].add(doc)
        r["classes"].setdefault(doc, cls)
        # If same actor has different descriptions across docs (shouldn't usually), keep both
        if doc not in r["descriptions"]:
            r["descriptions"][doc] = desc
            r["locations"][doc] = loc
    return list(by_name.values())

def reports_tag(rep_set):
    """Return a tag like 'both', '2027', '2040' for filtering."""
    if "AI 2027" in rep_set and "AI 2040" in rep_set:
        return "both"
    if "AI 2027" in rep_set:
        return "2027"
    return "2040"

def reports_badges(rep_set):
    out = []
    if "AI 2027" in rep_set:
        out.append('<span class="rep rep-2027">2027</span>')
    if "AI 2040" in rep_set:
        out.append('<span class="rep rep-2040">2040</span>')
    return "".join(out)

def combine_field(d, name_label="doc"):
    """Render a dict {doc: value} as either a single value or a labeled split."""
    vals = list(d.values())
    if len(set(vals)) == 1:
        return html.escape(vals[0])
    parts = []
    for doc, v in d.items():
        short = "2027" if "2027" in doc else "2040"
        parts.append(f'<div class="split"><span class="split-tag split-{short}">{short}</span>{html.escape(v)}</div>')
    return "".join(parts)

# ---------------------------------------------------------------------------
# HTML TEMPLATE - unified single-chart layout
# ---------------------------------------------------------------------------

HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Actors in AI 2027 & AI 2040 Scenarios - Unified Chart</title>
<style>
:root {{
  --bg: #fafbfc;
  --fg: #1a1a1a;
  --muted: #666;
  --accent: #0066cc;
  --card: #ffffff;
  --border: #e1e4e8;
  --real: #0366d6;
  --fictional: #d63384;
  --role: #6f42c1;
  --regional: #218838;
  --c2027: #b35900;
  --c2040: #008080;
  --cboth: #1a3a5c;
  --catastrophic: #c0392b;
}}
* {{ box-sizing: border-box; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  margin: 0; padding: 0;
  background: var(--bg); color: var(--fg); line-height: 1.5;
}}
header {{
  background: linear-gradient(135deg, #1a3a5c 0%, #0066cc 100%);
  color: white; padding: 2rem 2rem 1.25rem;
}}
header h1 {{ margin: 0 0 0.5rem; font-size: 1.7rem; }}
header .sub {{ opacity: 0.92; font-size: 0.95rem; max-width: 920px; }}
header .meta {{ font-size: 0.85rem; opacity: 0.85; margin-top: 0.75rem; }}
main {{ padding: 1.5rem 2rem 2rem; max-width: 1500px; margin: 0 auto; }}

.controls {{
  position: sticky; top: 0; z-index: 10;
  background: var(--bg);
  padding: 0.75rem 0 0.9rem;
  margin-bottom: 1rem;
  border-bottom: 1px solid var(--border);
}}
.control-row {{
  display: flex; flex-wrap: wrap; gap: 0.5rem 1.25rem; align-items: center;
  margin-bottom: 0.5rem;
}}
.control-row:last-child {{ margin-bottom: 0; }}
.control-row .label {{
  font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em;
  color: var(--muted); font-weight: 600; margin-right: 0.35rem;
}}
.chip {{
  display: inline-flex; align-items: center; gap: 0.3rem;
  padding: 0.3rem 0.75rem; border-radius: 14px;
  background: white; border: 1.5px solid var(--border);
  font-size: 0.85rem; cursor: pointer; user-select: none;
  transition: all 0.12s;
}}
.chip:hover {{ border-color: var(--accent); }}
.chip.active {{
  background: var(--accent); color: white; border-color: var(--accent);
}}
.chip .count {{
  font-size: 0.72rem; opacity: 0.8;
  background: rgba(255,255,255,0.25); padding: 0 0.4rem; border-radius: 8px;
}}
.chip.active.type-real {{ background: var(--real); border-color: var(--real); }}
.chip.active.type-fictional {{ background: var(--fictional); border-color: var(--fictional); }}
.chip.active.type-role {{ background: var(--role); border-color: var(--role); }}
.chip.active.type-regional {{ background: var(--regional); border-color: var(--regional); }}
.chip.active.rep-2027 {{ background: var(--c2027); border-color: var(--c2027); }}
.chip.active.rep-2040 {{ background: var(--c2040); border-color: var(--c2040); }}
.chip.active.rep-both {{ background: var(--cboth); border-color: var(--cboth); }}
.chip.active.lens-cattop {{ background: var(--catastrophic); border-color: var(--catastrophic); }}
.chip.lens-cattop {{ border-color: var(--catastrophic); color: var(--catastrophic); }}

.search-wrap {{ flex: 1; min-width: 220px; }}
.search-wrap input {{
  width: 100%; padding: 0.55rem 0.85rem; font-size: 0.92rem;
  border: 1.5px solid var(--border); border-radius: 8px;
}}
.search-wrap input:focus {{ outline: 2px solid var(--accent); border-color: var(--accent); }}

select.class-filter {{
  padding: 0.45rem 0.65rem; font-size: 0.88rem;
  border: 1.5px solid var(--border); border-radius: 8px;
  background: white; cursor: pointer; max-width: 280px;
}}

.result-count {{
  font-size: 0.85rem; color: var(--muted);
  padding: 0.4rem 0; font-style: italic;
}}

table.actors {{
  width: 100%; border-collapse: collapse;
  background: var(--card);
  border: 1px solid var(--border); border-radius: 8px;
  overflow: hidden; font-size: 0.88rem;
}}
table.actors thead {{ background: #f0f3f6; }}
table.actors th {{
  padding: 0.7rem 0.85rem; text-align: left;
  font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em;
  color: var(--muted); font-weight: 600;
  border-bottom: 1px solid var(--border); cursor: pointer; user-select: none;
  white-space: nowrap;
}}
table.actors th:hover {{ color: var(--accent); }}
table.actors th.sort-asc::after {{ content: " \\2191"; color: var(--accent); }}
table.actors th.sort-desc::after {{ content: " \\2193"; color: var(--accent); }}
table.actors td {{
  padding: 0.6rem 0.85rem; border-bottom: 1px solid var(--border);
  vertical-align: top;
}}
table.actors tr:last-child td {{ border-bottom: none; }}
table.actors tr:hover td {{ background: #fafbfc; }}
.actor-name {{ font-weight: 600; }}
.rep {{
  display: inline-block; padding: 0.1rem 0.5rem; border-radius: 9px;
  font-size: 0.72rem; font-weight: 700; margin-right: 0.2rem;
  letter-spacing: 0.02em;
}}
.rep-2027 {{ background: #ffe9cc; color: var(--c2027); }}
.rep-2040 {{ background: #ccf0f0; color: var(--c2040); }}
.type {{
  display: inline-block; padding: 0.1rem 0.5rem; border-radius: 9px;
  font-size: 0.72rem; font-weight: 600; white-space: nowrap;
}}
.type-real {{ background: #d1e7fd; color: var(--real); }}
.type-fictional {{ background: #fce7f3; color: var(--fictional); }}
.type-role {{ background: #ede1f8; color: var(--role); }}
.type-regional {{ background: #d4f4dd; color: var(--regional); }}
.split {{ font-size: 0.85rem; margin-bottom: 0.2rem; }}
.split:last-child {{ margin-bottom: 0; }}
.split-tag {{
  display: inline-block; padding: 0 0.4rem; border-radius: 5px;
  font-size: 0.68rem; font-weight: 700; margin-right: 0.4rem;
}}
.split-2027 {{ background: #ffe9cc; color: var(--c2027); }}
.split-2040 {{ background: #ccf0f0; color: var(--c2040); }}

.legend {{ font-size: 0.8rem; color: var(--muted); margin-top: 0.5rem; }}
.legend strong {{ color: var(--fg); }}

.classes-toc {{
  background: var(--card); border: 1px solid var(--border); border-radius: 8px;
  padding: 1rem 1.25rem; margin-bottom: 1.25rem;
}}
.classes-toc h3 {{ margin: 0 0 0.6rem; font-size: 1rem; }}
.classes-toc .grid {{
  display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 0.5rem 1.25rem;
}}
.classes-toc .cls {{
  font-size: 0.82rem; padding: 0.25rem 0;
}}
.classes-toc .cls .name {{ font-weight: 600; }}
.classes-toc .cls .desc {{ color: var(--muted); }}
.classes-toc .cls .nbadge {{
  background: #f0f3f6; padding: 0 0.45rem; border-radius: 8px;
  font-size: 0.72rem; color: var(--muted); margin-left: 0.35rem;
}}

/* Expandable Datasets cell */
.ds-cell {{ font-size: 0.85rem; }}
.ds-cell > summary {{
  cursor: pointer; user-select: none; padding: 0.2rem 0;
  list-style: none; display: inline-flex; align-items: center; gap: 0.35rem;
  color: var(--accent); font-weight: 600;
}}
.ds-cell > summary::-webkit-details-marker {{ display: none; }}
.ds-cell > summary::before {{
  content: "\\2295"; font-size: 0.95rem; line-height: 1;
  transition: transform 0.15s;
}}
.ds-cell[open] > summary::before {{ content: "\\2296"; }}
.ds-cell .ds-count {{
  background: var(--accent); color: white;
  padding: 0.05rem 0.4rem; border-radius: 8px;
  font-size: 0.72rem; font-weight: 700;
}}
.ds-cell .ds-label {{ font-size: 0.78rem; }}
.ds-list {{
  margin-top: 0.6rem; padding-left: 0.5rem;
  border-left: 2px solid var(--border);
}}
.ds-item {{
  margin-bottom: 0.5rem; padding-left: 0.5rem; font-size: 0.82rem;
}}
.ds-item:last-child {{ margin-bottom: 0; }}
.ds-item a {{
  font-weight: 600; color: var(--accent); text-decoration: none;
}}
.ds-item a:hover {{ text-decoration: underline; }}
.ds-desc {{
  font-size: 0.78rem; color: var(--fg);
  margin-top: 0.15rem; line-height: 1.4;
}}
.ds-access {{
  font-size: 0.72rem; color: var(--muted); font-style: italic;
  margin-top: 0.1rem;
}}
.link-kind {{
  font-size: 0.68rem; font-weight: 600; padding: 0.05rem 0.3rem;
  border-radius: 5px; margin-left: 0.35rem; vertical-align: middle;
  white-space: nowrap;
}}
.link-kind.deep {{ background: #d4f4dd; color: #1a7a3a; }}
.link-kind.search {{ background: #fff3cd; color: #856404; }}
.link-kind.general {{ background: #e9ecef; color: #495057; }}
.no-data {{ color: var(--border); font-size: 1rem; }}

footer {{ padding: 1.5rem; text-align: center; color: var(--muted); font-size: 0.85rem; }}
</style>
</head>
<body>
<header>
  <h1>Actors in the AI 2027 &amp; AI 2040 Scenarios</h1>
  <div class="sub">
    Unified inventory of every entity with agency across both scenario documents by the AI Futures Project.
    Compiled for the <em>Simulating AI Policies</em> agentic-testbed project. Each row is one unique actor,
    tagged with which scenario(s) it appears in. Use the chips and search to filter.
  </div>
  <div class="meta">
    Sources: <code>ai-2027.pdf</code> (71pp) + <code>AI-2040.pdf</code> (90pp) &middot;
    {n_unified} unique actors &middot; {n_2027}+{n_2040}={total} document-actor links &middot;
    {n_both} appear in both documents
  </div>
</header>
<main>
  {classes_toc}

  <div class="controls">
    <div class="control-row">
      <span class="label">Reports</span>
      {reports_chips}
      <span class="label" style="margin-left:1rem">Type</span>
      {type_chips}
      <span class="label" style="margin-left:1rem">Policy lens</span>
      <span class="chip lens-cattop" onclick="toggleChip(this,'lens','cat-top25')"
            title="Show only the 25 real actors most impacted by / responsive to the 12 catastrophic bills in LidaSim (categories 7 & 10: frontier-AI safety + race dynamics). Excludes individuals. Off by default.">
        Catastrophic Top 25 <span class="count">{cat_top25_count}</span>
      </span>
    </div>
    <div class="control-row">
      <span class="label">Class</span>
      <select class="class-filter" id="classFilter" onchange="applyFilters()">
        <option value="">All classes</option>
        {class_options}
      </select>
      <div class="search-wrap">
        <input id="textSearch" type="text"
               placeholder="Search actors by name, role, class, or location..."
               oninput="applyFilters()">
      </div>
      <span class="result-count" id="resultCount"></span>
    </div>
  </div>

  <table class="actors" id="actorsTable">
    <thead>
      <tr>
        <th data-sort="name" class="sort-asc">Actor</th>
        <th data-sort="reports">Reports</th>
        <th data-sort="type">Type</th>
        <th data-sort="class">Class(es)</th>
        <th data-sort="role">Role in scenario</th>
        <th data-sort="location">Appears in</th>
        <th>Raw data sources</th>
      </tr>
    </thead>
    <tbody>
      {rows_html}
    </tbody>
  </table>
</main>
<footer>
  Generated for the Simulating AI Policies project.
  {n_unified} unique actors across both scenario documents.
</footer>
<script>
// State: which report/type chips are active. Empty set = no filter on that axis.
// `lens` is a different shape — a single toggle (empty = off, contains 'cat-top25' = on).
const state = {{ reports: new Set(['in2027','in2040','both']), types: new Set(['Real','Fictional','Role-based','Regional']), lens: new Set() }};

function toggleChip(el, group, value) {{
  const s = state[group];
  if (s.has(value)) {{
    s.delete(value);
    el.classList.remove('active');
  }} else {{
    s.add(value);
    el.classList.add('active');
  }}
  applyFilters();
}}

function applyFilters() {{
  const q = document.getElementById('textSearch').value.toLowerCase().trim();
  const cls = document.getElementById('classFilter').value;
  const trs = document.querySelectorAll('#actorsTable tbody tr');
  let visible = 0;
  trs.forEach(tr => {{
    const inDocs = tr.dataset.docsArr.split(',');
    const type = tr.dataset.type;
    const text = tr.textContent.toLowerCase();
    const classText = tr.dataset.class.toLowerCase();
    // Reports filter: at least one active chip must match
    let docMatch = false;
    if (state.reports.has('in2027') && inDocs.includes('AI 2027')) docMatch = true;
    if (state.reports.has('in2040') && inDocs.includes('AI 2040')) docMatch = true;
    if (state.reports.has('both') && inDocs.length === 2) docMatch = true;
    if (state.reports.size === 0) docMatch = true;  // nothing selected = show all
    // Type filter
    const typeMatch = state.types.size === 0 || state.types.has(type);
    // Policy lens: if 'cat-top25' is on, only show rows where data-cat-top25 === 'true'
    const lensMatch = !state.lens.has('cat-top25') || tr.dataset.catTop25 === 'true';
    // Class filter
    const classMatch = !cls || classText.includes(cls.toLowerCase());
    // Text filter
    const textMatch = !q || text.includes(q);
    const show = docMatch && typeMatch && lensMatch && classMatch && textMatch;
    tr.style.display = show ? '' : 'none';
    if (show) visible++;
  }});
  document.getElementById('resultCount').textContent =
    visible + ' of ' + trs.length + ' actors shown';
}}

// Sortable columns
let sortState = {{ key: 'name', dir: 'asc' }};
document.querySelectorAll('#actorsTable th[data-sort]').forEach(th => {{
  th.addEventListener('click', () => {{
    const key = th.dataset.sort;
    if (sortState.key === key) {{
      sortState.dir = sortState.dir === 'asc' ? 'desc' : 'asc';
    }} else {{
      sortState.key = key; sortState.dir = 'asc';
    }}
    document.querySelectorAll('#actorsTable th').forEach(t => t.classList.remove('sort-asc','sort-desc'));
    th.classList.add(sortState.dir === 'asc' ? 'sort-asc' : 'sort-desc');
    const tbody = document.querySelector('#actorsTable tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    rows.sort((a, b) => {{
      const av = a.dataset['sort_' + key] || '';
      const bv = b.dataset['sort_' + key] || '';
      let cmp;
      if (key === 'reports') {{
        // sort by number of docs then name
        cmp = (parseInt(av) || 0) - (parseInt(bv) || 0);
      }} else {{
        cmp = av.localeCompare(bv);
      }}
      return sortState.dir === 'asc' ? cmp : -cmp;
    }});
    rows.forEach(r => tbody.appendChild(r));
  }});
}});

applyFilters();
</script>
</body>
</html>
"""

# ---------------------------------------------------------------------------
# CATASTROPHIC-BILL RELEVANCE SCORING (LidaSim integration)
# Top 25 real (non-individual) actors most impacted by / responsive to the 12 catastrophic bills
# in the LidaSim policy-impacts database (categories 7 and 10).
# Source: https://zachschlosser.github.io/LidaSim/ai_legislation_impacts.html
# ---------------------------------------------------------------------------

# Below-threshold startups don't qualify for frontier safety bills
# (CA SB 53, IL SB 315, NY RAISE, MA S.2630 require $500M+ AI rev or 10^26 FLOP)
BELOW_FRONTIER_THRESHOLD = {
    "Devin (Cognition)", "Glean", "Tesla", "Etched", "Taalas", "BYD"
}

# Pre-seed / minimal policy footprint — excluded from top-50 contention
MINIMAL_POLICY_FOOTPRINT = {"Etched", "Taalas", "BYD"}

# The 12 catastrophic bills (categories 7 and 10 from LidaSim)
CATASTROPHIC_BILLS = {
    "7a": "CA SB 53 — Frontier AI Transparency",
    "7b": "Preserving American Dominance in AI Act (S. 5616)",
    "7c": "Great American AI Act of 2026",
    "7d": "Illinois SB 315 — AI Safety Measures",
    "7e": "New York RAISE Act",
    "7f": "Massachusetts S. 2630 — Frontier AI Transparency",
    "7g": "EU AI Act (Regulation 2024/1689)",
    "7h": "FRONTIER Act (Obernolte-Trahan, July 2026)",
    "10a": "H.R. 5388 — American AI Leadership & Uniformity Act",
    "10b": "CREATE AI Act — NAIRR",
    "10c": "ENFORCE Act — AI export controls",
    "10d": "AI for America Act — National AI Strategy",
}

def cat_bill_score(name, classes):
    """Return set of catastrophic bill IDs this actor is materially impacted by."""
    if name in MINIMAL_POLICY_FOOTPRINT:
        return set()

    affected = set()

    if "Frontier AI Companies" in classes:
        if name not in BELOW_FRONTIER_THRESHOLD:
            affected.update({"7a", "7c", "7d", "7e", "7f", "7g", "7h"})
            affected.add("7b")
            if name in ("OpenAI", "Anthropic", "Google DeepMind", "Meta", "Microsoft",
                        "Amazon", "Google / Alphabet", "xAI", "Nvidia"):
                affected.add("10b")
        affected.update({"10a", "10c", "10d"})

    if "AI Systems (Agentic)" in classes:
        affected.update({"7a", "7c", "7d", "7e", "7f", "7g", "7h"})

    if "Supply Chain / Hardware" in classes:
        affected.add("10c")
        if name in ("Nvidia", "TSMC", "ASML", "Huawei"):
            affected.update({"7b", "10a", "10d"})
            if name in ("ASML", "TSMC"):
                affected.add("7g")
        if name == "RAND Corporation":
            affected.update({"7a", "7c", "10c"})

    if "US Government Agencies" in classes:
        affected.update({"7b", "7c", "7h", "10a", "10d"})
        if name == "US AI Safety Institute (AISI)":
            affected.update({"7a", "7d", "7e", "7f", "7g"})
        if name in ("Department of Defense (DOD)", "The Pentagon"):
            affected.update({"10c"})
        if name == "Department of Energy (DOE)":
            affected.update({"10c"})
        if name == "CISA":
            affected.update({"7a", "10c"})
        if name == "CIA":
            affected.update({"10c"})
        if name == "National Security Council (NSC)":
            affected.update({"10c"})
        if name == "FDA":
            affected.add("7g")

    if "Government Agencies / Regulatory" in classes:
        affected.update({"7g", "7c", "7h", "10a"})
        if name == "US AI Safety Institute (AISI)":
            affected.update({"7a", "7d", "7e", "7f", "7h"})
        if name == "FDA":
            affected.add("7g")

    if "Legislative / Oversight Bodies" in classes or "Legislative Bodies" in classes:
        if name == "US Congress":
            affected.update({"7b", "7c", "7h", "10a", "10b", "10c", "10d"})
        elif "Politburo" in name or "Chinese Communist Party" in name:
            affected.update({"10c", "10d", "7b"})

    if "Governments / Nation-States" in classes:
        if name == "United States":
            affected.update({"7b", "7c", "7h", "10a", "10c", "10d", "7g"})
        elif "China" in name:
            affected.update({"7b", "10c", "10d", "10a"})
        elif name == "European Union":
            affected.update({"7g", "10c", "10a"})
        elif name == "United Kingdom":
            affected.update({"7g", "10c"})
        elif name == "Taiwan":
            affected.update({"10c", "7b", "10a"})
        elif name == "Israel":
            affected.add("10c")
        elif name == "India":
            affected.update({"10c", "10a"})
        elif name == "Russia":
            affected.add("10c")

    if "Military / National Security" in classes:
        affected.update({"7b", "10c"})
        if name == "People's Liberation Army (PLA)":
            affected.update({"10d"})
        elif name == "Five Eyes":
            affected.update({"10c"})

    if "International Frameworks / Proposals" in classes:
        affected.update({"7g", "10c"})

    if "Research / Standards Organizations" in classes or "Research / Policy / Civil Society" in classes:
        affected.update({"7c", "10b"})
        if name in ("METR", "Redwood Research"):
            affected.update({"7a", "7d", "7e", "7f", "7g", "7h"})
        if name == "Epoch":
            affected.update({"7h"})
        if name == "Open Philanthropy":
            affected.update({"7a"})
        if name == "RAND Corporation":
            affected.update({"7a", "10c"})
        if name == "AI Futures Project":
            affected.update({"10b"})
        if name == "Lightcone Infrastructure":
            affected.add("10b")
        if name == "Forethought":
            affected.add("10b")

    if "China Government / Political" in classes:
        affected.update({"7b", "10c"})

    if "Civil Society / Public / Media" in classes:
        if name == "The New York Times":
            affected.update({"7c", "7h"})

    # Individuals — CEOs responsive via their companies
    if name in ("Sam Altman", "Dario Amodei", "Demis Hassabis", "Elon Musk"):
        affected.update({"7a", "7c", "7d", "7e", "7f", "7g", "7h"})
    if name == "Jensen Huang":
        affected.update({"10c", "7b", "10a"})
    if name in ("Marc Andreessen", "Peter Thiel"):
        affected.update({"7c", "10a"})
    if name in ("Geoffrey Hinton", "Ilya Sutskever"):
        affected.update({"7a", "7c", "7e"})
    if name == "Alex Turner":
        affected.update({"7a", "7c"})
    if name == "Xi Jinping":
        affected.update({"7b", "10c", "10d"})

    return affected


def compute_top_25_cat_actors():
    """Return set of actor names in the top 25 by catastrophic-bill impact score.
    Excludes individuals (Real (individual) type) — focuses on institutional /
    organizational actors only."""
    unified = unify_actors()
    scored = []
    for r in unified:
        if not r["type"].startswith("Real"):
            continue
        if r["type"] == "Real (individual)":
            continue  # exclude named persons (CEOs, researchers, political figures)
        classes = set(r["classes"].values())
        bills = cat_bill_score(r["name"], classes)
        scored.append((r["name"], len(bills), len(bills)))
    scored.sort(key=lambda x: (-x[1], x[0].lower()))
    return {name for name, _, _ in scored[:25]}

TOP_25_CAT_ACTORS = compute_top_25_cat_actors()


def render_unified_table():
    unified = unify_actors()
    # Sort by actor name
    unified.sort(key=lambda r: r["name"].lower())

    # Build filter chips with counts
    rep_counts = {"in2027": 0, "in2040": 0, "both": 0}
    type_counts = {"Real": 0, "Fictional": 0, "Role-based": 0, "Regional": 0}
    for r in unified:
        if "AI 2027" in r["docs"]:
            rep_counts["in2027"] += 1
        if "AI 2040" in r["docs"]:
            rep_counts["in2040"] += 1
        if len(r["docs"]) == 2:
            rep_counts["both"] += 1
        type_counts[type_category(r["type"])] += 1

    reports_chips = (
        f'<span class="chip active rep-2027" onclick="toggleChip(this,\'reports\',\'in2027\')">In 2027 <span class="count">{rep_counts["in2027"]}</span></span>'
        f'<span class="chip active rep-2040" onclick="toggleChip(this,\'reports\',\'in2040\')">In 2040 <span class="count">{rep_counts["in2040"]}</span></span>'
        f'<span class="chip active rep-both" onclick="toggleChip(this,\'reports\',\'both\')">In Both <span class="count">{rep_counts["both"]}</span></span>'
    )
    type_chips = "".join(
        f'<span class="chip active type-{tc.lower()}" onclick="toggleChip(this,\'types\',\'{tc}\')">{tc} <span class="count">{type_counts[tc]}</span></span>'
        for tc in ["Real", "Fictional", "Role-based", "Regional"]
    )

    # Build class dropdown options (union of all classes across docs)
    all_classes = sorted({c for _, c, *_ in ACTORS})
    class_options = "".join(f'<option value="{html.escape(c)}">{html.escape(c)}</option>' for c in all_classes)

    # Build rows
    rows_html = []
    for r in unified:
        tcat = type_category(r["type"])
        docs_sorted = sorted(r["docs"])
        rep_tag = reports_tag(r["docs"])
        # Combined class text for display and filtering
        if len(set(r["classes"].values())) == 1:
            class_display = html.escape(next(iter(r["classes"].values())))
            class_sort = next(iter(r["classes"].values()))
        else:
            class_display = combine_field(r["classes"])
            class_sort = " / ".join(r["classes"].values())
        role_display = combine_field(r["descriptions"])
        loc_display = combine_field(r["locations"])

        rows_html.append(
            f'<tr data-docs="{";".join(docs_sorted)}" '
            f'data-docs-arr="{",".join(docs_sorted)}" '
            f'data-type="{html.escape(tcat)}" '
            f'data-cat-top25="{"true" if r["name"] in TOP_25_CAT_ACTORS else "false"}" '
            f'data-class="{html.escape(class_sort)}" '
            f'data-sort_name="{html.escape(r["name"].lower())}" '
            f'data-sort_reports="{len(docs_sorted)}" '
            f'data-sort_type="{html.escape(tcat)}" '
            f'data-sort_class="{html.escape(class_sort.lower())}" '
            f'data-sort_role="{html.escape(r["descriptions"].get("AI 2027", r["descriptions"].get("AI 2040", "")).lower())}" '
            f'data-sort_location="{html.escape(r["locations"].get("AI 2027", r["locations"].get("AI 2040", "")).lower())}">'
            f'<td class="actor-name">{html.escape(r["name"])}</td>'
            f'<td>{reports_badges(r["docs"])}</td>'
            f'<td><span class="type {type_class(r["type"])}">{html.escape(r["type"])}</span></td>'
            f'<td>{class_display}</td>'
            f'<td>{role_display}</td>'
            f'<td><em>{loc_display}</em></td>'
            f'<td>{render_datasets_cell(r["name"], set(r["classes"].values()), r["type"])}</td>'
            f'</tr>'
        )

    # Build classes table-of-contents summary
    class_counts = {}
    for d, c, *_ in ACTORS:
        class_counts[c] = class_counts.get(c, 0) + 1

    classes_toc = ['<div class="classes-toc">',
                   '<h3>Classes of actors (taxonomy)</h3>',
                   '<div class="grid">']
    for c in sorted(class_counts.keys(), key=lambda x: -class_counts[x]):
        desc = CLASS_DESCRIPTIONS.get(c, "")
        classes_toc.append(
            f'<div class="cls"><span class="name">{html.escape(c)}</span>'
            f'<span class="nbadge">{class_counts[c]}</span>'
            f'<div class="desc">{html.escape(desc)}</div></div>'
        )
    classes_toc.append('</div></div>')

    # Stats
    n_unified = len(unified)
    n_2027 = sum(1 for a in ACTORS if a[0] == "AI 2027")
    n_2040 = sum(1 for a in ACTORS if a[0] == "AI 2040")
    total = len(ACTORS)
    n_both = sum(1 for r in unified if len(r["docs"]) == 2)

    return HTML_TEMPLATE.format(
        n_unified=n_unified, n_2027=n_2027, n_2040=n_2040, total=total, n_both=n_both,
        cat_top25_count=len(TOP_25_CAT_ACTORS),
        reports_chips=reports_chips,
        type_chips=type_chips,
        class_options=class_options,
        rows_html="\n".join(rows_html),
        classes_toc="\n".join(classes_toc),
    )

def write_html(path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(render_unified_table())

# ---------------------------------------------------------------------------
# PUBLIC RAW DATASETS - catalog + per-actor mapping
# Each entry: (id, name, URL, what it contains, access notes)
# Criteria: publicly accessible, raw primary-source data (not commentary/analysis).
# ---------------------------------------------------------------------------

DATASETS = {
    # --- AI model evaluation / capability ---
    "lmsys": ("LMSYS Chatbot Arena", "https://huggingface.co/spaces/lmarena-ai/arena-leaderboard",
              "Pairwise human-preference battle data; ranking of frontier LLMs. 33K+ conversation dataset downloadable.",
              "Free; HF Datasets download"),
    "open_llm_lb": ("Hugging Face Open LLM Leaderboard", "https://huggingface.co/open-llm-leaderboard",
                    "Standardized automated benchmark scores (MMLU, GSM8K, ARC, HellaSwag, etc.) for open-weight LLMs. Per-model JSON results.",
                    "Free; per-model results downloadable"),
    "helm": ("Stanford CRFM HELM", "https://crfm.stanford.edu/helm/",
             "Holistic Evaluation of Language Models: 7 metrics (accuracy, calibration, robustness, fairness, bias, toxicity, efficiency) across 16 scenarios. Code on github.com/stanford-crfm/helm.",
             "Free; open-source framework + results"),
    "epoch": ("Epoch AI Model Database", "https://epoch.ai/data/ai-models",
              "CSV download of 3,500+ AI/ML models with training compute (FLOP), parameter count, dataset size, release date. Daily-updated. Used by both scenarios.",
              "Free; CSV bulk download"),
    "hf_hub": ("Hugging Face Hub", "https://huggingface.co/models",
               "1M+ model cards with weights, training data, model reports, and dataset cards. Per-org APIs.",
               "Free; OpenAPI + git"),
    "bigbench": ("Google BIG-bench", "https://github.com/google/BIG-bench",
                 "200+ evaluation tasks for LLMs, includingBeyond the Imitation Game benchmark. All task code and prompts are open.",
                 "Free; Apache 2.0"),
    "metr": ("METR Task Suite", "https://metr.org/",
             "Agentic task evaluations: time horizon studies, autonomous task completion benchmarks. Used in AI 2027 footnotes for coding-agent capability projections.",
             "Free; reports + GitHub"),
    "aiid": ("AI Incident Database (AIID)", "https://incidentdatabase.ai/",
             "1,400+ real-world AI harm/near-harm incidents, OID-tagged. Each incident has reports, entities involved, harms taxonomy.",
             "Free; CC BY 4.0; bulk CSV"),
    "oecd_aim": ("OECD AI Incidents Monitor (AIM)", "https://oecd.ai/en/dashboards/ai-incidents",
                 "OECD-tracked AI incidents with policy implications. Complements AIID with government-side view.",
                 "Free"),
    "aiaaic": ("AIAAIC Repository", "https://www.aiaaic.org/",
               "Independent AI incident tracker; ~3,000+ incidents of AI harms, algorithms, and entities.",
               "Free; CC BY-SA"),

    # --- Corporate / financial (AI labs & tech) ---
    "sec_edgar": ("SEC EDGAR", "https://www.sec.gov/edgar/search/",
                  "Full-text search + REST API of all SEC filings since 2001: 10-K, 10-Q, 8-K, proxy statements, insider Form 4. No API key. Bulk download available.",
                  "Free; no auth; 10 req/sec rate limit"),
    "sec_xbrl": ("SEC XBRL Company Facts API", "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json",
                 "Structured financials (revenue, R&D spend, headcount, capex) for every public US company in machine-readable JSON.",
                 "Free; no auth"),
    "opencorporates": ("OpenCorporates", "https://opencorporates.com/",
                       "200M+ legal entities from 140+ government registries. Includes Delaware/California filings for OpenAI, Anthropic, xAI.",
                       "Free API tier (limited); bulk by request"),
    "crunchbase_odm": ("Crunchbase Open Data Map", "https://data.crunchbase.com/",
                       "Free snapshot of funding rounds, valuations, acquisitions, investors. Best public source for private-company financials.",
                       "Free; CC BY-NC"),
    "companies_house_uk": ("Companies House (UK)", "https://find-and-update.company-information.service.gov.uk/",
                           "Free UK company filings: annual returns, officers, accounts. Covers DeepMind Technologies Ltd, Google UK.",
                           "Free; bulk data"),
    "uspto": ("USPTO PatentsView", "https://patentsview.org/",
              "Patent applications/grants from USPTO, bulk data + API. Inventor affiliations link companies to research.",
              "Free; bulk + API"),
    "twse_open": ("TWSE Open Data (Taiwan)", "https://data.gov.tw/dataset/6092",
                  "Taiwan Stock Exchange filings for TSMC and other Taiwanese-listed companies. Annual reports, financial statements.",
                  "Free; bulk"),
    "sse_en": ("Shanghai/Shenzhen Stock Exchange", "http://www.sse.com.cn/en/",
               "Chinese public-company filings (limited English coverage).",
               "Free; partial"),
    "bis_entity": ("BIS Entity List (US)", "https://www.bis.doc.gov/index.php/policy-guidance/lists-of-parties-of-concern/entity-list",
                   "Federal Register export-control listings. Tracks Huawei, SMIC, restrictively-designated Chinese AI/chip entities.",
                   "Free; Federal Register"),

    # --- Academic / scientific ---
    "openalex": ("OpenAlex", "https://openalex.org/",
                 "Fully open scholarly graph (250M+ works) replacing Microsoft Academic. Author affiliations, citations, concepts. Bulk dump monthly.",
                 "Free; CC0; bulk"),
    "arxiv": ("arXiv", "https://arxiv.org/",
              "Preprint server for AI/ML, physics, math. Bulk metadata via OAI-PMH; full-text PDFs for all papers. Covers ~all frontier-lab research.",
              "Free; bulk"),
    "sem_scholar": ("Semantic Scholar", "https://www.semanticscholar.org/product/api",
                    "Open academic graph API with citation context, TLDRs, influence scores. Free for non-commercial research.",
                    "Free; API key for high volume"),
    "orcid": ("ORCID Public Data File", "https://orcid.org/",
              "Annual bulk dump of public researcher profiles (~20M researchers). Disambiguates individual identities.",
              "Free; CC0"),
    "github_archive": ("GH Archive", "https://www.gharchive.org/",
                       "Event stream of all public GitHub activity (commits, issues, PRs, reviews) since 2011. Hourly dumps.",
                       "Free; bulk"),

    # --- US government / legislative / executive ---
    "congress_gov": ("Congress.gov Bulk Data", "https://www.congress.gov/",
                     "Bills, votes, members, hearings, Congressional Record. Bulk XML/JSON on github.com/usgpo/bulk-data.",
                     "Free; bulk"),
    "govtrack": ("GovTrack", "https://www.govtrack.us/",
                 "Free API + bulk data for congressional voting records, bill cosponsorships, member ideologue scores.",
                 "Free; CC0"),
    "federal_register": ("Federal Register", "https://www.federalregister.gov/",
                         "Daily journal of US federal government: executive orders, agency rules, proposed regulations. Bulk JSON/XML via API.",
                         "Free; bulk API"),
    "usaspending": ("USASpending.gov", "https://www.usaspending.gov/",
                    "All federal contracts, grants, loans >$0. DOD/AISI/CISA spending on AI contracts, NVidia purchase orders, etc.",
                    "Free; bulk"),
    "app": ("American Presidency Project", "https://www.presidency.ucsb.edu/",
            "All public presidential documents 1789-present: speeches, executive orders, press conferences, Trump's Twitter archive.",
            "Free; searchable"),
    "ppp": ("Public Papers of the Presidents (NARA)", "https://www.govinfo.gov/app/collection/ppp",
            "Official National Archives compilation of presidential writings, addresses, remarks. Hoovers through Biden.",
            "Free; bulk"),
    "fec": ("FEC.gov", "https://www.fec.gov/data/",
            "Campaign finance: candidate filings, donor records, independent expenditures, lobbying bundles. Bulk data + API.",
            "Free; bulk"),
    "opensecrets": ("OpenSecrets Bulk Data", "https://www.opensecrets.org/open-data/bulk-data",
                    "Lobbying disclosures, campaign contributions, revolving-door data, org-by-org. Free bulk downloads.",
                    "Free; CC BY-NC"),
    "regulations": ("Regulations.gov", "https://www.regulations.gov/",
                    "Federal rulemaking comments and dockets. Public comments on NIST AI RMF, BIS export controls, etc.",
                    "Free; API"),
    "gao": ("GAO Reports", "https://www.gao.gov/",
            "Government Accountability Office reports on federal programs; full-text searchable archive.",
            "Free; bulk"),

    # --- US agency-specific ---
    "dod_pubs": ("DOD Publications (WHSD)", "https://www.esd.whs.mil/",
                 "DOD Dictionary, annual reports, DOD press releases, DODI instructions.",
                 "Free"),
    "dod_pla_report": ("DOD Annual Report on PLA", "https://media.defense.gov/",
                       "Annual Report to Congress on Military and Security Developments Involving the People's Republic of China. Authoritative public source on PLA.",
                       "Free; annual PDF"),
    "osti": ("DOE OSTI", "https://www.osti.gov/",
             "Department of Energy Office of Scientific and Technical Information: full-text reports, including national-lab AI research.",
             "Free; bulk API"),
    "cisa_kev": ("CISA KEV Catalog", "https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
                 "Known Exploited Vulnerabilities catalog and cybersecurity advisories.",
                 "Free; bulk JSON"),
    "cisa_advisories": ("CISA Cybersecurity Advisories", "https://www.cisa.gov/news-events/cybersecurity-advisories",
                        "All CISA advisories including joint Five Eyes (US/UK/AU/CA/NZ) releases.",
                        "Free; RSS + bulk"),
    "nist_airmf": ("NIST AI RMF", "https://www.nist.gov/it/ai-artificial-intelligence-risk-management-framework",
                   "NIST AI Risk Management Framework, AISI publications, US AI Safety Institute outputs.",
                   "Free"),
    "openfda": ("openFDA", "https://open.fda.gov/",
                "Drug/device approval data, adverse events, recall notices. API + bulk.",
                "Free; no auth"),
    "cia_foia": ("CIA FOIA Reading Room", "https://www.cia.gov/readingroom/",
                 "25+ years of declassified CIA documents, searchable. Includes old Soviet/PRC assessments.",
                 "Free"),
    "dni_foia": ("DNI FOIA", "https://www.dni.gov/foia/",
                 "Office of the Director of National Intelligence FOIA releases; IC-wide declassified docs.",
                 "Free"),

    # --- International / multilateral ---
    "oecd_ai": ("OECD.AI Observatory", "https://oecd.ai/",
                "900+ national AI policies tracked live; AI Incidents Monitor; compute/data dashboards. The canonical global AI-policy database.",
                "Free; some via World Bank Data360"),
    "un_treaties": ("UN Treaty Collection", "https://treaties.un.org/",
                    "Status of multilateral treaties: signatures, ratifications, reservations. Covers IAEA safeguards, AI-related declarations.",
                    "Free; bulk"),
    "world_bank": ("World Bank Open Data", "https://data.worldbank.org/",
                   "Country-level economic/social/governance indicators: GDP, military spending, R&D intensity, etc. Bulk CSV.",
                   "Free; bulk"),
    "sipri": ("SIPRI Arms Transfers Database", "https://www.sipri.org/databases/armstransfers",
              "Stockholm International Peace Research Institute's database of international arms transfers since 1950.",
              "Free; bulk"),
    "iaea_docs": ("IAEA Documents", "https://www.iaea.org/resources",
                  "International Atomic Energy Agency publications, safeguards reports, INES incident classifications.",
                  "Free"),
    "eur_lex": ("EUR-Lex", "https://eur-lex.europa.eu/",
                "Official EU law database: AI Act, GDPR, MDR, all regulations/directives. Bulk via Cellar API.",
                "Free; bulk"),
    "eu_ai_office": ("EU AI Office Documents", "https://digital-strategy.ec.europa.eu/en/policies/ai-office",
                     "EU AI Office publications, implementing acts, GPAI codes of practice.",
                     "Free"),

    # --- China / CCP ---
    "china_vitae": ("China Vitae", "https://chinavitae.com/",
                    "Biographical database of CCP officials: career histories, public statements, track records of Politburo members.",
                    "Free"),
    "ccp_watch": ("USCC Annual Report", "https://www.uscc.gov/annual-report",
                  "US-China Economic and Security Review Commission's annual report to Congress on PRC developments.",
                  "Free; annual PDF"),
    "merics": ("MERICS", "https://merics.org/",
               "Mercator Institute for China Studies - open publications on CCP politics, industrial policy, PLA.",
               "Free; reports"),

    # --- Nonprofits / research orgs ---
    "open_phil_grants": ("Open Philanthropy Grants", "https://www.openphilanthropy.org/grants",
                         "Bulk grants data (CSV) for every grant Open Phil has made: AI safety, biosecurity, global health.",
                         "Free; bulk"),
    "nonprofit_explorer": ("ProPublica Nonprofit Explorer", "https://projects.propublica.org/nonprofits/",
                           "IRS 990 filings for every US nonprofit. Covers RAND Corp, METR, Redwood Research, Forethought, AI Futures Project, Lightcone.",
                           "Free; bulk"),
    "rand_pubs": ("RAND Publications", "https://www.rand.org/pubs.html",
                  "Full-text RAND research reports including AI-weights security playbook, SL2-SL5 framework.",
                  "Free"),

    # --- Generic / national stats ---
    "wikidata": ("Wikidata", "https://www.wikidata.org/",
                 "Structured knowledge graph of 100M+ entities: corporate relationships, person biographies, organizational hierarchies. SPARQL endpoint + bulk JSON dumps.",
                 "Free; CC0"),
    "ciawf": ("CIA World Factbook", "https://www.cia.gov/the-world-factbook/",
              "Country-by-country statistical data: demographics, government structure, military, economy. Bulk via API.",
              "Free; public domain"),
}

# ---------------------------------------------------------------------------
# Mapping: which datasets apply to which actor.
# Returns a list of dataset IDs. Empty for fictional / role-based actors.
# ---------------------------------------------------------------------------

# Public US-listed companies and their tickers/CIKs
US_PUBLIC_COMPANIES = {
    "Microsoft": "0000789019",      # MSFT
    "Google / Alphabet": "0001652044",  # GOOGL
    "Amazon": "0001018724",
    "Meta": "0001326801",
    "Nvidia": "0001045810",
    "Tesla": "0001318605",
    "ASML": "ASML (Netherlands, ADR on NASDAQ)",
    "TSMC": "TSM (ADR on NYSE)",
}

CHINESE_COMPANIES = {"Huawei", "BYD", "DeepSeek", "Tencent", "Alibaba"}

def datasets_for_actor(name, classes, type_str):
    """Return list of dataset IDs relevant to this actor. Empty if fictional."""
    # Only real actors get datasets
    if not type_str.startswith("Real"):
        return []

    ds = []

    # -------- All real individuals get academic baseline --------
    if type_str == "Real (individual)":
        ds += ["openalex", "arxiv", "sem_scholar", "orcid", "wikidata"]
        # Person → country context (e.g., Xi Jinping is China-bound)
        if name == "Xi Jinping":
            ds += ["china_vitae", "ccp_watch", "dod_pla_report", "merics"]
        # CEOs / tech executives also appear in SEC + lobbying records
        if name in ("Sam Altman", "Elon Musk", "Demis Hassabis", "Dario Amodei",
                    "Jensen Huang", "Marc Andreessen", "Peter Thiel"):
            ds += ["sec_edgar", "crunchbase_odm", "opensecrets"]
        # US presidents get presidential-document archives
        if name in ("Dwight D. Eisenhower", "Ronald Reagan"):
            ds += ["app", "ppp"]

    # -------- By actor class --------
    if "Frontier AI Companies" in classes:
        # All AI companies get these baseline sources
        ds += ["hf_hub", "lmsys", "epoch", "arxiv", "openalex", "github_archive",
               "crunchbase_odm", "opencorporates", "uspto", "aiid"]
        if name in US_PUBLIC_COMPANIES:
            ds += ["sec_edgar", "sec_xbrl"]
        if name == "Google DeepMind":
            ds += ["companies_house_uk"]
        if name in CHINESE_COMPANIES:
            ds += ["bis_entity", "sse_en"]
        if name == "ASML":
            ds += ["bis_entity"]
        if name == "TSMC":
            ds += ["twse_open", "bis_entity"]

    if "AI Systems (Agentic)" in classes:
        # Real AI models
        ds += ["lmsys", "open_llm_lb", "helm", "epoch", "aiid", "oecd_aim",
               "aiaaic", "bigbench", "metr", "hf_hub"]

    if "Governments / Nation-States" in classes:
        ds += ["ciawf", "world_bank", "un_treaties", "wikidata"]
        if name == "United States":
            ds += ["congress_gov", "federal_register", "app", "ppp", "usaspending",
                   "fec", "opensecrets", "oecd_ai"]
        elif "China" in name or "PRC" in name:
            ds += ["china_vitae", "ccp_watch", "dod_pla_report", "merics", "oecd_ai",
                   "bis_entity"]
        elif name == "Russia":
            ds += ["sipri", "cia_foia"]
        elif name == "European Union":
            ds += ["eur_lex", "eu_ai_office", "oecd_ai"]
        elif name == "United Kingdom":
            ds += ["companies_house_uk", "oecd_ai"]
        elif name == "Taiwan":
            ds += ["twse_open"]
        elif name in ("Israel", "India"):
            ds += ["oecd_ai", "un_treaties"]
        elif name in ("Canada", "Mongolia", "Netherlands", "South Korea",
                      "Burkina Faso", "Guinea-Bissau"):
            ds += ["oecd_ai"]

    if "US Government Agencies" in classes:
        ds += ["federal_register", "usaspending", "gao", "wikidata"]
        if name == "Department of Defense (DOD)" or name == "The Pentagon":
            ds += ["dod_pubs", "dod_pla_report"]
        elif name == "Department of Energy (DOE)":
            ds += ["osti"]
        elif name == "CISA":
            ds += ["cisa_kev", "cisa_advisories"]
        elif name == "US AI Safety Institute (AISI)":
            ds += ["nist_airmf", "oecd_ai"]
        elif name == "CIA":
            ds += ["cia_foia"]
        elif name == "National Security Council (NSC)":
            ds += ["app", "ppp", "federal_register"]
        elif name == "FDA":
            ds += ["openfda"]

    if "Government Agencies / Regulatory" in classes:
        ds += ["federal_register", "regulations", "gao"]
        if name == "US AI Safety Institute (AISI)":
            ds += ["nist_airmf", "oecd_ai"]
        elif name == "FDA":
            ds += ["openfda"]

    if "Legislative / Oversight Bodies" in classes or "Legislative Bodies" in classes:
        if name == "US Congress":
            ds += ["congress_gov", "govtrack", "federal_register", "regulations", "fec"]
        elif "Politburo" in name or "Chinese Communist Party" in name:
            ds += ["china_vitae", "ccp_watch", "dod_pla_report", "merics"]

    if "Military / National Security" in classes:
        if name == "People's Liberation Army (PLA)":
            ds += ["dod_pla_report", "sipri", "ccp_watch", "china_vitae"]
        elif name == "Five Eyes":
            ds += ["cisa_advisories", "cia_foia", "dni_foia"]

    if "Supply Chain / Hardware" in classes:
        ds += ["bis_entity", "uspto"]
        if name == "TSMC":
            ds += ["twse_open", "sec_edgar", "epoch"]
        elif name == "Huawei":
            ds += ["sse_en", "ccp_watch", "hf_hub", "arxiv", "openalex", "github_archive"]
        elif name == "RAND Corporation":
            ds += ["rand_pubs", "nonprofit_explorer"]

    if "International Frameworks / Proposals" in classes:
        ds += ["oecd_ai", "un_treaties", "iaea_docs"]

    if "Research / Standards Organizations" in classes or "Research / Policy / Civil Society" in classes:
        ds += ["openalex", "arxiv", "github_archive"]
        if name == "Epoch":
            ds += ["epoch"]
        elif name == "Open Philanthropy":
            ds += ["open_phil_grants"]
        elif name == "RAND Corporation":
            ds += ["rand_pubs", "nonprofit_explorer"]
        elif name == "METR":
            ds += ["metr", "nonprofit_explorer"]
        elif name == "Redwood Research":
            ds += ["nonprofit_explorer"]
        elif name in ("Forethought", "Lightcone Infrastructure", "AI Futures Project"):
            ds += ["nonprofit_explorer"]

    if "Civil Society / Public / Media" in classes:
        if name == "The New York Times":
            ds += ["wikidata"]  # NYT has an API but it's not free; minimal raw data

    if "Authors / Named Individuals" in classes:
        # Academic baseline already added above for all Real (individual) actors
        pass

    # Dedupe preserving order
    seen = set()
    out = []
    for d in ds:
        if d not in seen and d in DATASETS:
            seen.add(d)
            out.append(d)
    return out

def render_datasets_cell(name, classes, type_str):
    """Return HTML for the expandable Datasets cell. Empty cell for fictional actors."""
    ds_ids = datasets_for_actor(name, classes, type_str)
    if not ds_ids:
        return '<span class="no-data" title="Fictional or role-based actor - no real-world dataset applies">—</span>'
    n = len(ds_ids)
    out = [f'<details class="ds-cell"><summary>'
           f'<span class="ds-count">{n}</span> '
           f'<span class="ds-label">{"source" if n == 1 else "sources"}</span>'
           f'</summary><div class="ds-list">']
    for did in ds_ids:
        dname, _general_url, desc, access = DATASETS[did]
        specific_url, link_type = deep_link(did, name, classes, type_str)
        type_tag = {
            "deep": ' <span class="link-kind deep" title="Direct link to this actor\'s data">[filtered]</span>',
            "search": ' <span class="link-kind search" title="Pre-filled search — click to run">[search]</span>',
            "general": ' <span class="link-kind general" title="Landing page — no per-actor filter available">[landing]</span>',
        }.get(link_type, "")
        out.append(
            f'<div class="ds-item">'
            f'<a href="{html.escape(specific_url)}" target="_blank" rel="noopener">{html.escape(dname)}</a>{type_tag}'
            f'<div class="ds-desc">{html.escape(desc)}</div>'
            f'<div class="ds-access">Access: {html.escape(access)}</div>'
            f'</div>'
        )
    out.append('</div></details>')
    return "".join(out)

# ---------------------------------------------------------------------------
# DEEP LINK GENERATION
# Returns (url, link_type) where link_type is "deep" | "search" | "general".
# ---------------------------------------------------------------------------

# Hugging Face Hub org slugs (verified)
HF_ORG_SLUGS = {
    "OpenAI": "openai",
    "Anthropic": "anthropic",
    "Google DeepMind": "google-deepmind",
    "Meta": "meta-llama",
    "Microsoft": "microsoft",
    "Nvidia": "nvidia",
    "xAI": "xai-org",
    "Huawei": "huawei-noah",
    "DeepSeek": "deepseek-ai",
    "Tesla": "tesla",
    "Devin (Cognition)": "cognition-ai",
    "Etched": "etched",
    "Taalas": "taalas",
    "Glean": "glean",
    "BYD": "byd",
}

# GitHub org slugs
GITHUB_ORGS = {
    "OpenAI": "openai",
    "Anthropic": "anthropics",
    "Google DeepMind": "google-deepmind",
    "Meta": "facebookresearch",
    "Microsoft": "microsoft",
    "Nvidia": "NVIDIA",
    "xAI": "xai-org",
    "Huawei": "huawei-noah",
    "DeepSeek": "deepseek-ai",
    "Tesla": "tesla",
    "Etched": "etchedtech",
    "Taalas": "taalas",
    "Glean": "glean",
    "Devin (Cognition)": "cognition-ai",
    "Epoch": "epoch-research",
    "METR": "METR",
    "Redwood Research": "redwoodresearch",
    "AI Futures Project": "ai-futures-project",
    "Lightcone Infrastructure": "lightcone-org",
    "Open Philanthropy": "openphilanthropy",
    "RAND Corporation": "rand",
    "ASML": "asml",
    "TSMC": "tsmc",
    "BYD": "byd-auto",
}

# SEC CIK numbers (public US-listed only)
SEC_CIKS = {
    "Microsoft": "0000789019",
    "Google / Alphabet": "0001652044",
    "Amazon": "0001018724",
    "Meta": "0001326801",
    "Nvidia": "0001045810",
    "Tesla": "0001318605",
    "ASML": "0001413747",   # foreign filer
    "TSMC": "0001046179",   # ADR
}

# TWSE stock codes
TWSE_CODES = {
    "TSMC": "2330",
}

# Country slug mappings for CIA Factbook / World Bank
COUNTRY_SLUGS = {
    "United States": "united-states",
    "China / PRC": "china",
    "Taiwan": "taiwan",
    "United Kingdom": "united-kingdom",
    "Russia": "russia",
    "European Union": "european-union",
    "India": "india",
    "Israel": "israel",
    "Canada": "canada",
    "Mongolia": "mongolia",
    "Netherlands": "netherlands",
    "South Korea": "korea-republic-of",
    "Burkina Faso": "burkina-faso",
    "Guinea-Bissau": "guinea-bissau",
}

# Federal Register agency slug IDs (verified format: lowercase-hyphenated)
FR_AGENCY_SLUGS = {
    "Department of Defense (DOD)": "defense-department",
    "The Pentagon": "defense-department",
    "Department of Energy (DOE)": "energy-department",
    "CISA": "cybersecurity-and-infrastructure-security-agency",
    "US AI Safety Institute (AISI)": "national-institute-of-standards-and-technology",
    "FDA": "food-and-drug-administration",
    "National Security Council (NSC)": "national-security-council",
    "CIA": "central-intelligence-agency",
}

# USASpending agency subtier slugs
USASPENDING_AGENCIES = {
    "Department of Defense (DOD)": "department-of-defense",
    "The Pentagon": "department-of-defense",
    "Department of Energy (DOE)": "department-of-energy",
    "CISA": "department-of-homeland-security",
    "US AI Safety Institute (AISI)": "department-of-commerce",
    "FDA": "department-of-health-and-human-services",
}

# EU institution EUR-Lex IDs
EUR_LEX_ACTORS = {
    "European Union": "AI Act; GDPR; Digital Services Act",
}

def deep_link(dataset_id, name, classes, type_str):
    """Return (url, link_type) for this actor in this dataset.
    link_type: 'deep' (direct entity page), 'search' (prefilled query), 'general' (landing)."""
    from urllib.parse import quote_plus, quote
    q = quote_plus(name)
    q_lo = quote_plus(name.lower())

    # ----- AI capability datasets -----
    if dataset_id == "hf_hub":
        slug = HF_ORG_SLUGS.get(name)
        if slug:
            return (f"https://huggingface.co/{slug}", "deep")
        return (f"https://huggingface.co/models?search={q_lo}", "search")

    if dataset_id == "lmsys":
        # Chatbot Arena - filter by org in leaderboard
        if name in HF_ORG_SLUGS:
            return (f"https://lmarena.ai/?filter={HF_ORG_SLUGS[name]}", "search")
        return ("https://lmarena.ai/", "general")

    if dataset_id == "open_llm_lb":
        # HF Open LLM Leaderboard search by org
        if name in HF_ORG_SLUGS:
            return (f"https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard?q={HF_ORG_SLUGS[name]}", "search")
        return ("https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard", "general")

    if dataset_id == "helm":
        # HELM has per-model report pages; use search
        return (f"https://crfm.stanford.edu/helm/classic/latest/?models={q.replace('+', '%2C')}", "search")

    if dataset_id == "epoch":
        # Epoch has a developer filter
        dev = name.split(" (")[0].replace(" ", "+")
        return (f"https://epoch.ai/data/ai-models?filter=developer%3D{dev}", "search")

    if dataset_id == "aiid":
        # AI Incident Database - per-developer page
        dev = name.split(" (")[0]
        return (f"https://incidentdatabase.ai/apps/incidents/?developers={quote_plus(dev)}", "search")

    if dataset_id == "oecd_aim":
        return ("https://oecd.ai/en/dashboards/ai-incidents", "general")

    if dataset_id == "aiaaic":
        return (f"https://www.aiaaic.org/?s={q}", "search")

    if dataset_id == "bigbench":
        return ("https://github.com/google/BIG-bench/tree/main/bigbench/bbseq_tasks", "general")

    if dataset_id == "metr":
        return ("https://metr.org/", "general")

    # ----- Corporate / financial -----
    if dataset_id == "sec_edgar":
        cik = SEC_CIKS.get(name)
        if cik:
            return (f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=&dateb=&owner=include&count=40", "deep")
        # Private company: full-text search of all filings mentioning the name
        return (f"https://efts.sec.gov/LATEST/search-index?q=%22{q}%22", "search")

    if dataset_id == "sec_xbrl":
        cik = SEC_CIKS.get(name)
        if cik:
            return (f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json", "deep")
        return ("https://www.sec.gov/search-filings/edgar-application-programming-interfaces", "general")

    if dataset_id == "crunchbase_odm":
        slug = name.lower().split(" (")[0].replace(" ", "-").replace("/", "-").replace(".", "").replace("&", "and")
        return (f"https://www.crunchbase.com/organization/{slug}", "search")

    if dataset_id == "opencorporates":
        return (f"https://opencorporates.com/companies?q={q}", "search")

    if dataset_id == "companies_house_uk":
        return (f"https://find-and-update.company-information.service.gov.uk/search/companies?q={q}", "search")

    if dataset_id == "uspto":
        return (f"https://patentsview.org/search/patent/search?q=%7B%22_assignees.assignee_organization%22%3A%5B%22{q}%22%5D%7D", "search")

    if dataset_id == "twse_open":
        code = TWSE_CODES.get(name)
        if code:
            return (f"https://mops.twse.com.tw/mops/web/t05st09?off=1&ifrs=1&co_id={code}", "deep")
        return ("https://mops.twse.com.tw/mops/web/t05st09", "general")

    if dataset_id == "sse_en":
        return (f"http://www.sse.com.cn/en/search/?keyword={q}", "search")

    if dataset_id == "bis_entity":
        # Federal Register listings of BIS entity-list additions
        return (f"https://www.federalregister.gov/documents/search?conditions[term]={q}&conditions[agencies][]=bureau-of-industry-and-security", "search")

    # ----- Academic -----
    if dataset_id == "arxiv":
        # Author affiliation search (catches org-affiliated papers)
        return (f"https://arxiv.org/search/?query=%22{q}%22&searchtype=all", "search")

    if dataset_id == "openalex":
        if "Authors / Named Individuals" in classes:
            return (f"https://explore.openalex.org/authors?filter=display_name.search:{q.replace('+', '%20')}", "search")
        return (f"https://explore.openalex.org/works?filter=author.display_name.search:{q.replace('+', '%20')}", "search")

    if dataset_id == "sem_scholar":
        return (f"https://www.semanticscholar.org/search?q={q}&sort=relevance", "search")

    if dataset_id == "orcid":
        return (f"https://orcid.org/orcid-search/search?searchQuery={q}", "search")

    if dataset_id == "github_archive":
        org = GITHUB_ORGS.get(name)
        if org:
            return (f"https://github.com/{org}", "deep")
        return (f"https://github.com/search?q={q}&type=organizations", "search")

    if dataset_id == "wikidata":
        return (f"https://www.wikidata.org/w/index.php?search={q}&title=Special:Search&ns0=1&ns120=1", "search")

    # ----- US government -----
    if dataset_id == "congress_gov":
        # Legislation mentioning the actor
        return (f"https://www.congress.gov/search?q=%7B%22source%22%3A%22legislation%22%2C%22search%22%3A%22{q}%22%7D", "search")

    if dataset_id == "govtrack":
        return (f"https://www.govtrack.us/search?q={q}", "search")

    if dataset_id == "federal_register":
        aid = FR_AGENCY_SLUGS.get(name)
        if aid:
            return (f"https://www.federalregister.gov/documents/search?conditions[agencies][]={aid}", "deep")
        return (f"https://www.federalregister.gov/documents/search?conditions[term]={q}", "search")

    if dataset_id == "usaspending":
        agency = USASPENDING_AGENCIES.get(name)
        if agency:
            return (f"https://www.usaspending.gov/agency/{agency}", "deep")
        return (f"https://www.usaspending.gov/search/?hash=recipientName%3A%22{q}%22", "search")

    if dataset_id == "regulations":
        return (f"https://www.regulations.gov/search?term={q}", "search")

    if dataset_id == "gao":
        return (f"https://www.gao.gov/search?keywords={q}&type=report", "search")

    if dataset_id == "app":
        return (f"https://www.presidency.ucsb.edu/documents?search={q}", "search")

    if dataset_id == "ppp":
        return (f"https://www.govinfo.app/search/?collection=ppp&field1={q}", "search")

    if dataset_id == "fec":
        return (f"https://www.fec.gov/data/receipts/?contributor_name={q}", "search")

    if dataset_id == "opensecrets":
        return (f"https://www.opensecrets.org/search?q={q}", "search")

    # ----- US agency-specific -----
    if dataset_id == "dod_pubs":
        return ("https://www.esd.whs.mil/Library/Publications/", "general")

    if dataset_id == "dod_pla_report":
        return ("https://media.defense.gov/search/?q=Annual+Report+Military+Security+Developments+China", "search")

    if dataset_id == "osti":
        return (f"https://www.osti.gov/search/semantic:{q}", "search")

    if dataset_id == "cisa_kev":
        return ("https://www.cisa.gov/known-exploited-vulnerabilities-catalog", "general")

    if dataset_id == "cisa_advisories":
        return (f"https://www.cisa.gov/news-events/cybersecurity-advisories?search={q}", "search")

    if dataset_id == "nist_airmf":
        return ("https://www.nist.gov/it/ai-artificial-intelligence-risk-management-framework", "general")

    if dataset_id == "openfda":
        return (f"https://api.fda.gov/search?q={q}", "search")

    if dataset_id == "cia_foia":
        return (f"https://www.cia.gov/readingroom/search/site/{q.replace('+', '%20')}", "search")

    if dataset_id == "dni_foia":
        return ("https://www.dni.gov/foia/", "general")

    # ----- International -----
    if dataset_id == "oecd_ai":
        if "Governments / Nation-States" in classes:
            # Map to country name (strip "/ PRC" etc.)
            cname = name.split(" / ")[0]
            return (f"https://oecd.ai/en/dashboards/countries?search={quote_plus(cname)}", "search")
        return ("https://oecd.ai/en/dashboards/overview", "general")

    if dataset_id == "un_treaties":
        return (f"https://treaties.un.org/pages/AdvancedSearch.aspx?tab=results&q={q}", "search")

    if dataset_id == "world_bank":
        slug = COUNTRY_SLUGS.get(name)
        if slug:
            return (f"https://data.worldbank.org/country/{slug}", "deep")
        return ("https://data.worldbank.org/", "general")

    if dataset_id == "sipri":
        return (f"https://www.sipri.org/databases/armstransfers?search={q}", "search")

    if dataset_id == "iaea_docs":
        return (f"https://www.iaea.org/search?q={q}", "search")

    if dataset_id == "eur_lex":
        return (f"https://eur-lex.europa.eu/search.html?text={q}&lang=en", "search")

    if dataset_id == "eu_ai_office":
        return ("https://digital-strategy.ec.europa.eu/en/policies/ai-office", "general")

    # ----- China-specific -----
    if dataset_id == "china_vitae":
        return (f"https://chinavitae.com/search.php?l=1&search={q}", "search")

    if dataset_id == "ccp_watch":
        return ("https://www.uscc.gov/annual-report", "general")

    if dataset_id == "merics":
        return (f"https://merics.org/en/search?search={q}", "search")

    # ----- Nonprofits -----
    if dataset_id == "open_phil_grants":
        return (f"https://www.openphilanthropy.org/grants?search={q}", "search")

    if dataset_id == "nonprofit_explorer":
        return (f"https://projects.propublica.org/nonprofits/organizations?search={q}&state=Any", "search")

    if dataset_id == "rand_pubs":
        return (f"https://www.rand.org/pubs/search.html?query={q}", "search")

    # ----- Generic fallbacks -----
    if dataset_id == "ciawf":
        slug = COUNTRY_SLUGS.get(name)
        if slug:
            return (f"https://www.cia.gov/the-world-factbook/countries/{slug}/", "deep")
        return ("https://www.cia.gov/the-world-factbook/countries/", "general")

    # Fallback to catalog URL
    return (DATASETS[dataset_id][1], "general")

# ---------------------------------------------------------------------------

if __name__ == "__main__":
    out_csv = Path("/Users/home/Downloads/ai_actors.csv")
    out_html = Path("/Users/home/Downloads/ai_actors.html")
    write_csv(out_csv)
    write_html(out_html)
    print(f"Wrote {out_csv} ({len(ACTORS)} rows)")
    print(f"Wrote {out_html}")
