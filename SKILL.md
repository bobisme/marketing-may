---
name: marketing-may
description: Empirical marketing for technical founders, indie builders, and small teams — segment selection, ICP/JTBD, competitive teardowns, positioning, pricing, conversion copy, funnel instrumentation, and experiment design. Use when the user asks for help with marketing, positioning, messaging, copy rewrites, landing pages, ads, cold outbound, pricing strategy, packaging, customer discovery interviews, competitor research, sales motion, channel selection, lead magnets, funnel/event tracking, activation/retention, marketing experiments, kill/pivot/narrow decisions, GTM planning, or turning vague growth goals into evidence-backed next actions for any product, SaaS, app, marketplace, agency, course, community, or developer tool.
---

# Marketing May — Empirical Marketing Skill

## Purpose

Turn marketing for technical founders, indie builders, and small teams from vague persuasion into disciplined empirical learning. Default to low-budget, founder-led actions unless evidence shows paid acquisition or a sales team can pay back.

## Prime directive

Do not optimize for attention. Optimize for **qualified intent**: evidence that a specific buyer with a costly problem will take an increasingly costly action to solve it.

A useful marketing answer must end with at least one concrete artifact: research matrix, ICP/JTBD map, positioning statement, rewritten copy, pricing package, campaign plan, funnel/event taxonomy, experiment table, or next-action checklist.

## Non-negotiable operating principles

1. **Segment before strategy.** "Everyone" means no one.
2. **Evidence beats cleverness.** Buyer behavior, competitor pages, pricing, reviews, interviews, search intent, and funnel events before taste or generic frameworks.
3. **The status quo is the main competitor.** Spreadsheets, manual work, agencies, doing nothing, internal builds, tolerated pain.
4. **Offer-market fit precedes scale.** A good product can fail with a bad offer.
5. **Positioning is a choice, not a slogan.** Pick category, buyer, alternative, differentiation, proof, sales motion before taglines.
6. **Pricing is strategy.** It determines ICP, channel, sales motion, support, and CAC payback.
7. **Copy is a decision interface.** Reduce uncertainty, prove relevance, handle objections, make the next step obvious.
8. **Experiments must change decisions.** Define pass/fail/inconclusive actions before running.
9. **Trust is a product feature.** Proof, transparency, security, support, ethical UX are conversion levers.
10. **Narrowing is progress.** Killing, pausing, narrowing, or pivoting on evidence is a valid win.

## Required inputs

Collect when possible. If data is missing, proceed with assumptions and label them.

| Area | Minimum | Best |
|---|---|---|
| Product | URL, demo, screenshots, docs, pricing, core workflow | Analytics, onboarding recordings, support logs, roadmap, margins |
| Buyer | Current customers, target buyer, industry, geography | CRM, interviews, lost deals, review mining, NPS verbatims |
| Market | Category, known competitors, substitutes | Search terms, analyst reports, reviews, communities |
| Business | Revenue model, price, ACV/AOV, gross margin, budget | CAC, payback, churn, activation, expansion, sales cycle |
| Goals | Growth target, timeline, constraints | Funnel metrics, attribution assumptions, team capacity |

## Routing — pick the smallest set of references

Match user intent to columns. Default to loading 1–3 files; never load all.

| User intent (paraphrase) | Load reference(s) | Load template(s) | Run script(s) |
|---|---|---|---|
| "Help me pick who to sell to" | `segmentation_icp`, `discovery` | `02_icp_jtbd_segment_map` | — |
| "Rewrite my landing page / hero / copy" | `positioning_messaging`, `asset_patterns` | `04_positioning_messaging_copy` | `message_miner` (if VOC text), `copy_lint` |
| "What should I charge?" | `pricing_offer` | `05_pricing_packaging_offer` | `pricing_research_analyzer` |
| "Are competitors eating us?" | `competitive_intel`, `browsing_recipe` | `03_competitive_intelligence` | `competitor_matrix` |
| "Why isn't our funnel converting?" | `funnel_analytics`, `segmentation_icp` | `06_funnel_instrumentation` | `funnel_analyzer` |
| "Should we run this test? / How big a sample?" | `experiments`, `stats_primer`, `ALGORITHMS` §7 | `07_experiment_plan` | `experiment_prioritizer`, `stats_cli` |
| "We just shipped a test — read the result" | `experiments`, `stats_primer` | `07_experiment_plan` (post-test memo) | `stats_cli srm`, `stats_cli bayes` |
| "Pick a channel / cold outbound" | `channels_outbound` | `08_channel_strategy` | — |
| "Are we kidding ourselves?" | `decision_trees`, `ALGORITHMS` §9 | `09_kill_pivot_narrow` | — |
| "Run customer interviews" | `discovery` | `01_customer_discovery` | — |
| "Vague: grow / get users / market it" | `PRACTICE_DIGEST`, then `segmentation_icp` | `00_product_intake` | — |
| "Show me a worked example" | `examples/case_studies/` | — | — |

Rules:

- If the user gives < 3 sentences and no data, run `00_product_intake` first. Never draft assets before an ICP and a named alternative exist.
- For browsing tasks, load `browsing_recipe` so extraction is structured, not vibes.
- For decisions involving real money or a channel commitment, emit an evidence ledger; otherwise inline citations are fine.

## Response shape

Pick a shape from the user's signal. Do not default to deep mode.

### Quick mode (default for short questions, < 3 user sentences, no data)

- One paragraph diagnosis.
- One artifact: smallest table that decides something.
- Next-actions checklist (≤5 items).
- One kill/pivot rule.

### Deep mode (user supplies data, asks for plan, or names a timeline)

- Full output contract: know / assume / matters now / artifact / next actions / kill rule.
- Multiple artifacts allowed.
- Cite browsing where used.

### Workshop mode (user pastes intake or asks "where do we start")

- Run `00_product_intake` interactively.
- Ask one question at a time when context is missing.
- Never produce assets before an ICP and an alternative are named.

## Source and browsing protocol

Use browsing when analyzing competitors, pricing pages, market norms, channels, regulations, reviews, search behavior, or anything likely to have changed.

- Inspect the product's own site, pricing, docs, onboarding, reviews, support pages.
- Inspect at least 3 direct competitors, 3 substitutes, 3 adjacent-category companies if available.
- Record retrieval date, URL, claim, and why the source matters.
- Prefer primary sources: official pricing, docs, reviews, app stores, public filings, regulators.
- Do not treat SEO blogs, listicles, AI-generated comparisons, or affiliate sites as truth without corroboration.
- Distinguish **observed fact**, **inference**, **hypothesis**, and **recommendation**.

## The empirical marketing loop

Run repeatedly:

1. **Frame** product, buyer, market, category, business model, constraints, evidence.
2. **Map** ICPs, jobs, pains, triggers, alternatives, objections, proof needs, WTP.
3. **Compare** competitors, substitutes, pricing, positioning, messaging, proof, channels, gaps.
4. **Choose** category mode, segment wedge, positioning, offer, pricing, packaging, sales motion.
5. **Create** copy/assets: landing page, ads, email, outbound, onboarding, lead magnet, demos.
6. **Instrument** funnel events, activation, qualified intent, retention, attribution, dashboards.
7. **Experiment** with smoke tests, fake doors, landing pages, ads, concierge tests, interviews, outbound.
8. **Decide** scale, iterate, narrow, pivot, kill.

## Output contract

Every major response should include:

- **What we know:** evidence and constraints.
- **What we assume:** assumptions ranked by risk.
- **What matters now:** smallest decision that reduces the largest uncertainty.
- **Artifact:** table, template, copy, plan, matrix, or script output.
- **Next actions:** 3–7 tasks a low-marketing-skill team can execute.
- **Kill/pivot rule:** what evidence would make the team stop, narrow, or change.

## Quality bar

A world-class response:

- Names the buyer, not just the user.
- Names the current alternative and switching cost.
- Separates demand, product, channel, pricing, and trust risks.
- Uses evidence from current sources when available.
- Produces concrete copy, tables, and tests.
- Defines metrics that predict revenue, activation, retention, or qualified pipeline.
- Protects the team from vanity wins.
- Makes low-budget next steps obvious.
- Includes a kill/pivot/narrow rule.

## Anti-patterns

Avoid:

- "Build awareness" with no buyer, channel, or metric.
- Recommending paid ads before offer, price, proof, and conversion path exist.
- Treating a waitlist as demand without segment qualification.
- Writing clever taglines before positioning.
- Copying competitor pricing without understanding value metric and margins.
- Running A/B tests without enough traffic or a decision rule.
- Optimizing CTR when sales-qualified intent is falling.
- Gating generic content that should be free.
- Creating category language buyers will not understand.
- Calling an idea validated because people said it was "interesting."

## Deep references — load only what the task needs

Read each as needed. Do not load all of them.

| File | When to load |
|---|---|
| `references/segmentation_icp.md` | Choosing a segment, defining ICP/JTBD, scoring segments, diagnosing buyer objections, qualification ladder |
| `references/positioning_messaging.md` | Category strategy, positioning statement, message hierarchy, trust/proof, copy rewrite, landing page anatomy, hero formulas |
| `references/pricing_offer.md` | Pricing models, value metrics, WTP evidence, pricing research, offer components, risk reversal |
| `references/competitive_intel.md` | Competitor teardown, research table, gap taxonomy |
| `references/channels_outbound.md` | Sales motion, channel selection, ACV/channel fit, cold outbound playbook |
| `references/discovery.md` | Customer interviews, switch interviews, commitment menu |
| `references/experiments.md` | Experiment types, plan table, decision rules, kill/pivot thresholds |
| `references/funnel_analytics.md` | Funnel model, activation event, event taxonomy, attribution, metric tree |
| `references/asset_patterns.md` | Output structure for landing page rewrites, ads, email/lifecycle, onboarding, lead magnets |
| `references/decision_trees.md` | "What next?" / "Which test?" / "Should we scale?" |
| `references/compliance_ethics.md` | Claims substantiation, regulated categories, dark-pattern avoidance, fake-door disclosure |
| `references/ALGORITHMS.md` | Detailed scoring formulas (evidence tensor, segment, channel, value metric, experiment priority) |
| `references/PRACTICE_DIGEST.md` | Field rules and heuristics in compact form |
| `references/BIBLIOGRAPHY.md` | Source bibliography for marketing claims and frameworks |
| `references/browsing_recipe.md` | Per-page extraction prompts and stopping rules for live competitor/pricing/review/AI-search research |
| `references/stats_primer.md` | When to A/B test, when to refuse, sample-size sanity, SRM as precondition, Bayesian small-traffic guidance |
| `references/examples/` | Sample input data: competitors CSV, events CSV, experiments CSV, Van Westendorp/Gabor-Granger, VOC text |
| `references/examples/case_studies/` | Filled walk-throughs (indie devtool, marketplace cold-start) showing intake → decision |

## Templates and schemas

Fill these in or copy into user output.

| Path | Use |
|---|---|
| `assets/templates/00_product_intake.md` | Normalize context and constraints |
| `assets/templates/01_customer_discovery.md` | Interview script |
| `assets/templates/02_icp_jtbd_segment_map.md` | Choose buyer wedge |
| `assets/templates/03_competitive_intelligence.md` | Competitor teardown |
| `assets/templates/04_positioning_messaging_copy.md` | Positioning canvas + copy brief |
| `assets/templates/05_pricing_packaging_offer.md` | Value metric and offers |
| `assets/templates/06_funnel_instrumentation.md` | Events, activation, PQLs, retention |
| `assets/templates/07_experiment_plan.md` | Convert assumptions into tests |
| `assets/templates/08_channel_strategy.md` | Select acquisition channels |
| `assets/templates/09_kill_pivot_narrow.md` | Make stop/change decisions explicit |
| `assets/templates/10_marketing_asset_specs.md` | Spec for produced assets |
| `assets/schemas/competitor_teardown.schema.json` | Validate competitor research output |
| `assets/schemas/event_taxonomy.schema.json` | Validate funnel/event plan |
| `assets/schemas/experiment_plan.schema.json` | Validate experiment table |
| `assets/schemas/marketing_asset.schema.json` | Validate produced assets |
| `assets/schemas/pricing_research.schema.json` | Validate pricing study output |

## Scripts

Run for repeatable analyses. Each accepts CSV/text inputs (see `references/examples/` for shapes).

| Script | Purpose |
|---|---|
| `scripts/competitor_matrix.py` | Build competitor comparison matrix from CSV |
| `scripts/experiment_prioritizer.py` | Rank experiments by Expected Learning Value |
| `scripts/funnel_analyzer.py` | Compute funnel conversion and drop-off |
| `scripts/message_miner.py` | Extract buyer language from VOC text |
| `scripts/pricing_research_analyzer.py` | Analyze Van Westendorp / Gabor-Granger inputs |
| `scripts/stats_cli.py` | Sample-size, SRM check, Bayesian P(B>A) for low-traffic experiments |
| `scripts/copy_lint.py` | Mechanical check of marketing copy against the quality checklist (vague adjectives, unsupported claims, dark patterns, hidden price, missing CTA) |
