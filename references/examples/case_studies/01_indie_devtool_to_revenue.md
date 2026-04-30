# Case Study 01 — Indie Devtool: $0 → $3.4k MRR in 14 weeks

> Synthetic example for skill training, not a real customer. Numbers are plausible against 2026 indie SaaS benchmarks (median free-to-paid 8%, activation × 2.5 with a defined activation event) but should not be cited as primary research.

## Why this example

A solo technical founder ships a niche devtool, has no audience, $0 marketing budget, and can't afford a category mistake. Shows the skill applied to the most common indie path: pick a wedge → cold outbound + content → land first 5 paying customers → instrument → narrow.

Antipatterns this case study deliberately avoids:
- Building a waitlist and calling it demand.
- Running paid ads before the offer converts manually.
- Writing a clever tagline before the positioning statement.
- Treating "interested" reply as a buying signal.

## Founder snapshot

- **Product:** Stripe Sentry — watches a customer's Stripe webhook stream and alerts when a webhook fails or returns non-2xx.
- **Founder:** Solo, ex-payments engineer, 2 years at a fintech.
- **Stage:** Working prototype, no customers, no domain authority.
- **Cash runway:** 6 months. No marketing budget.

---

## Step 1 — Intake (`00_product_intake`)

| Field | Answer |
|---|---|
| Product | Stripe Sentry |
| One-sentence | Catches broken Stripe webhooks before customers do. |
| Founder's category | "Webhook reliability tool" |
| Buyer's category (hypothesis) | "Stripe monitoring" / "payments observability" |
| Core workflow | Connect Stripe → we replay last 7 days → live monitor going forward |
| Stage | Working prototype |
| Pricing (initial guess) | $49/mo flat |
| Margin | ~80% — minimal infra |
| Capacity | Solo, ~20 hrs/wk on marketing |

**Highest-risk assumptions (founder's gut):**
1. SaaS finance teams notice and care when webhooks fail.
2. They'd pay $49/mo when Stripe's own dashboard is "free."
3. Reachable through Stripe-related communities.

These three assumptions drive the experiment table at step 6.

---

## Step 2 — Segment scoring (`02_icp_jtbd_segment_map`, `references/segmentation_icp.md`)

Three candidate segments. Score 1–5.

| Factor | A: Indie SaaS founders ($1–10k MRR) | B: B2B SaaS finance/ops teams (Series A+) | C: Stripe Connect platforms |
|---|---:|---:|---:|
| Pain | 3 (annoying, rarely catastrophic) | 4 (revenue-leak when undetected) | 5 (compliance + revenue risk) |
| Trigger | 2 (random) | 3 (audit / incident / new hire) | 4 (compliance review, partner SLA) |
| WTP | 2 (DIY culture) | 4 (clear budget) | 5 (named line item) |
| Reachability | 5 (IndieHackers, X, Discord) | 3 (LinkedIn, communities, outbound) | 2 (small list, outbound only) |
| Differentiation | 4 (no competitor focused here) | 3 (Datadog/Bedrock cover this) | 4 |
| Proof availability | 3 (sample reports easy) | 3 (case study possible) | 2 (need named logo, slow) |
| **Numerator** | 720 | 1,728 | 1,600 |
| Sales complexity | 1 (self-serve) | 2 (light sales) | 4 (security review) |
| Switching cost | 1 | 2 | 4 |
| **Denominator (1+...)** | 2 | 3 | 5 |
| **SAS** | **360** | **576** | **320** |

**Decision:** Segment B wins on attractiveness, but the founder has zero existing Series-A connections. **Choose A first as a wedge** — high reachability, fast feedback, will produce proof to bring to B later.

ICP statement (segment A):

> For solo and 2-person SaaS founders running on Stripe with $500–$10k MRR, who lose revenue when webhooks silently fail and currently `tail -f` their logs or wait for customer complaints, triggered by a payment incident or migration, Stripe Sentry alerts within 30 seconds of a webhook failure with a one-click replay. Unlike Datadog/Bedrock, it requires no agent install and is priced for a 1-person team. Buyers can pay because $49/mo is below the cost of one missed renewal. Reachable through IndieHackers, indie SaaS Discords, and Stripe community forums.

---

## Step 3 — Competitive teardown (`browsing_recipe`, `competitor_matrix.py`)

Browsed (logged with retrieval date 2026-04-22): Datadog Synthetics, Bedrock, Webhook.site, Hookdeck, Svix monitoring, manual Stripe dashboard.

Norms found:
- All competitors target "developers" generically; none name SaaS-founder-on-Stripe.
- 4 of 6 hide pricing; 2 show $99+ entry.
- Proof is logo-strip heavy; only 1 has a webhook-specific case study.
- All assume agent install or middleware deploy.

Gaps:
- **Segment gap:** no competitor speaks to indie SaaS founders specifically.
- **Pricing gap:** $49 transparent flat fee is a 50% cut against the cheapest visible option.
- **Setup gap:** competitors require infra changes; Stripe Sentry uses the Stripe API directly.

Three positioning angles imply: lead with the segment, lead with $0-install, lead with $49/mo transparent.

---

## Step 4 — Positioning (`04_positioning_messaging_copy`)

**Statement:**

> Stripe Sentry is webhook monitoring for solo SaaS founders on Stripe who lose revenue when a webhook silently fails. Unlike Datadog or building it yourself, it connects in 30 seconds with no agent install and starts at $29/mo so a 1-person team can afford it.

**Hero, after lint:**

> Find broken Stripe webhooks before your customers do. 30-second setup. No agent install. $29/mo for the first 100k events.

Ran `scripts/copy_lint.py landing.md` — 0 findings (no vague adjectives, named price, named outcome).

---

## Step 5 — Pricing (`05_pricing_packaging_offer`, `pricing_research_analyzer.py`)

Founder ran a Van Westendorp on 28 indie SaaS Discord members:

| Output | Result |
|---|---:|
| Optimal Price Point (OPP) | $34 |
| Indifference Price Point (IDP) | $42 |
| Acceptable range (PMC–PME) | $24 – $58 |

Ran Gabor-Granger separately on 31 IndieHackers respondents:

| Price | P(buy) | Revenue index |
|---:|---:|---:|
| $19 | 0.45 | 8.55 |
| $29 | 0.39 | 11.31 |
| $49 | 0.19 | 9.31 |
| $79 | 0.06 | 4.74 |

**Decision:** Anchor at $29/mo for the first tier (Gabor revenue-max), $79/mo for the team tier. This is below the founder's gut $49 — but the segment will not bear $49 until proof exists. Reprice once 5 named-logo case studies land.

---

## Step 6 — Experiment table (`07_experiment_plan`, `experiment_prioritizer.py`)

Top 4 from `experiment_prioritizer.py` (full ranking dropped here for brevity):

| # | Experiment | Channel | Metric | Threshold | Decision rule |
|---|---|---|---|---|---|
| 1 | 50 cold-outbound emails to indie SaaS founders | Email + Twitter DM | Positive replies | ≥ 3 (6%) | <1% → kill list/segment; 1–5% → tune; ≥5% → scale |
| 2 | Hero comparison test on landing | IndieHackers homepage post + 5 Discord shares | Trial signups / 100 qualified visits | ≥ 4% | <2% → rewrite hero; 2–4% → ship; ≥4% → scale traffic |
| 3 | Concierge "audit" lead magnet | Reach 10 founders, run free audit | Audit → paid pilot conversion | ≥ 3 of 10 | <2/10 → reposition; 3+ → productize |
| 4 | Activation funnel instrumentation | All channels | Time-to-first-alert ≤ 1 hour after signup | ≥ 60% | <40% → rebuild onboarding |

**Sample size note:** founder ran `stats_cli.py sample-size --baseline 0.04 --mde 0.5` — required N ≈ 1,440/arm. With ~80 weekly visitors expected, that's 6 months. Switched to **Bayesian sequential** via `stats_cli.py bayes`, stopping at P(B>A) ≥ 0.95 OR after 8 weeks, whichever first. Pre-registered.

---

## Step 7 — Funnel instrumentation (`06_funnel_instrumentation`, `funnel_analyzer.py`)

Activation event chosen: **first_alert_received_after_install** (within 7 days of signup).

Why this and not `signup_completed`: research bibliography flags activation events 2.5× trial-to-paid. "First real alert" proves the product is wired correctly to the buyer's Stripe.

Tracked events (taxonomy):
```
page_view, signup_completed, stripe_connected, first_alert_received,
trial_to_paid_completed, alert_replay_used, weekly_active
```

Funnel after 6 weeks (`funnel_analyzer.py`):

| Step | Users | Step CVR |
|---|---:|---:|
| page_view | 1,142 | – |
| signup_completed | 78 | 6.8% |
| stripe_connected | 51 | 65.4% |
| first_alert_received | 33 | 64.7% |
| trial_to_paid_completed | 11 | 33.3% |

Activation rate: 33/78 = 42% (slightly above 37.5% indie SaaS median).
Trial-to-paid: 11/78 = 14% (above 8% median, below the 15–20% benchmark for 14-day trials).

---

## Step 8 — Decision (`09_kill_pivot_narrow`)

Week 14 result against pre-registered thresholds:

| Test | Pre-registered threshold | Observed | Decision |
|---|---|---|---|
| Outbound positive reply | ≥ 3 of 50 (6%) | 7 of 50 (14%) | Strong — scale outbound |
| Hero CVR | ≥ 4% | 6.8% | Ship — keep hero |
| Concierge audit → paid | ≥ 3 of 10 | 4 of 10 | Productize the audit as a lead magnet |
| Activation rate | ≥ 60% | 42% | **Iterate — onboarding gap** |
| Bayes P(B>A) on hero | ≥ 0.95 to ship | 0.97 after week 8 | Shipped early |

Status: **$3.4k MRR / 14 weeks / 28 paying customers**. Activation gap is the binding constraint, not acquisition.

Next move: rather than buying more traffic, founder runs onboarding session-recordings and finds the Stripe-connect step is where 35% drop. Fix scoped, then revisit segment B with the case studies now in hand.

---

## What the skill produced (artifact summary)

1. ICP statement + scored segment matrix
2. Competitive teardown with 3 named gaps
3. Positioning statement that passes `copy_lint.py`
4. Van Westendorp + Gabor pricing study with a defended $29 price
5. Pre-registered experiment table with Bayesian stopping rule
6. Event taxonomy + activation event with retention prediction
7. Decision memo identifying activation as the binding constraint

## What the skill protected the founder from

- Spending on paid ads before $29 converts manually.
- Pricing at $49 because "competitors are $99+" — research showed segment WTP didn't support it without proof.
- Calling the test a winner from frequentist alpha at week 4 (P(B>A) was only 0.81 then; would have been a false ship).
- Building a "team" tier feature pile before the activation hole was fixed.
