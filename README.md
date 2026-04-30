# /marketing-may

Agent skill for doing data-driven marketing.

## Install

```shell
npx skills add bobisme/marketing-may
```

## How to Use

Ask your agent.

## Disclaimer

This will only lose you money. Don't use it.

If it makes you money, Bob is not liable for any injuries caused by carrying large sacks of currency, the burden of turning down excessive requests for romantic relationships, or accidents in your overpriced sports cars.

## Features

### Decision frameworks (references)

- **Segmentation, ICP & JTBD** — qualification ladder, segment scoring, buyer-psychology / objection model.
- **Positioning & messaging** — category-strategy decision tree, positioning system, message hierarchy, hero-formula bank, copy quality checklist.
- **Pricing & offer design** — pricing-model decision table, value-metric fit score, WTP evidence ladder, risk-reversal menu.
- **Competitive intel** — research table, gap taxonomy, four-group competitor set (direct / adjacent / substitutes / aspirational).
- **Channels & cold outbound** — sales-motion decision tree, ACV/channel fit heuristic, channel-fit scoring, outbound thresholds and template.
- **Modern channels** — AI search / AEO / GEO citation patterns, podcast sponsorship math (2026 CPMs), community playbooks for Discord/Slack/Reddit, newsletter sponsorships.
- **Marketplace & network effects** — cold-start playbook, liquidity targets by marketplace type, take-rate ranges, disintermediation defenses.
- **Customer discovery** — interview rules, structure, commitment menu.
- **Experiments** — experiment types, ELV scoring, kill/pivot/narrow rules, decision-rule pre-registration.
- **Funnel analytics** — stage model, activation event selection, event taxonomy rules, attribution caveats.
- **Metric trees** — pre-built starter trees for self-serve SaaS, usage-based / API, marketplace, OSS-led, course/community, sales-led B2B, e-commerce.
- **Stats primer** — when to A/B test, when to refuse, sample-size sanity, SRM as precondition, Bayesian small-traffic guidance.
- **Browsing recipe** — per-page extraction shapes for competitor homepages, pricing pages, reviews, search/AI-search citations, with stopping rules.
- **Compliance & ethics** — never-recommend list, substantiation, dark-pattern avoidance.
- **Decision trees** — "what next?", "which test?", "should we scale this channel?".
- **Algorithms & practice digest** — evidence tensor, segment attractiveness, offer-market fit, category gravity, objection entropy, proof debt, copy-claim risk filter; field rules in compact form.

### Templates

Fillable templates for product intake, customer-discovery interviews, ICP/JTBD/segment maps, competitive teardowns, positioning + messaging + copy, pricing/packaging/offer, funnel instrumentation, experiment plans, channel strategy, kill/pivot/narrow decisions, and asset specs.

### JSON schemas

Validatable schemas for competitor teardowns, event taxonomies, experiment plans, marketing assets, pricing research, and an evidence ledger for tracking each load-bearing claim's source, behavioral strength, and kill rule.

### Scripts (Python, no third-party deps unless noted)

- `competitor_matrix.py` — summarize competitor research CSV into category norms, gap counts, and whitespace prompts.
- `experiment_prioritizer.py` — rank experiments by Expected Learning Value with a decision hint per row.
- `funnel_analyzer.py` — ordered funnel conversion + drop-off, optional segment grouping.
- `retention_analyzer.py` — cohort × week-N retention table with directional curve-shape verdict (plateau / flattening / declining).
- `message_miner.py` — extract repeated buyer language from voice-of-customer text; bucket by pain / outcome / objection / trigger / alternative / proof.
- `pricing_research_analyzer.py` — Van Westendorp and Gabor-Granger directional analysis with segment cuts.
- `outbound_list_scorer.py` — score account CSV against weighted ICP criteria (firmographic / tech / role / recency-bounded triggers / negatives) and rank into A/B/C tiers.
- `stats_cli.py` — A/B test sample size, sample-ratio mismatch (Microsoft p<0.0005 threshold), Bayesian Beta-Binomial P(B>A) with credible interval and expected-loss decision aid.
- `copy_lint.py` — mechanical check of marketing copy for vague adjectives, unsupported superlatives, dark-pattern urgency, hidden price, weak social proof, missing CTA, buzzword density. Supports inline `<!-- lint:ignore <rule> -->`.
- `validate_artifact.py` — validate any JSON artifact against the corresponding schema; auto-detects schema by filename.

### Worked case studies

Two filled walk-throughs (synthetic but realistic) showing the full skill flow from intake through decision: an indie devtool reaching $3.4k MRR, and a two-sided marketplace narrowing to first 50 transactions.

### Quality layer

- 83-test pytest suite covering every script (sample-size formula, SRM detection, Bayesian determinism, funnel ordering invariant, Van Westendorp edge cases, copy-lint rules, retention curve helpers, outbound recency windows).
- Pyright-friendly with `pyrightconfig.json`.
- `just test` / `just test-quiet` / `just setup-dev` recipes.
