# Case Study 02 — Two-Sided Marketplace Cold-Start: First 50 Transactions

> Synthetic example for skill training, not a real customer. Numbers are plausible against marketplace literature (NFX, Sharetribe) but should not be cited as primary research.

## Why this example

A two-person team builds a regional services marketplace. Default SaaS marketing playbook fails on a marketplace because demand has nothing to match against until supply is liquid in a single niche. Shows the skill applied when **the right answer is to do less than the founder originally planned**.

Antipatterns this case study deliberately avoids:
- Launching all cities / all categories on day one.
- Buying paid demand before supply density is healthy.
- Treating supply listings as proof of supply liquidity.
- Optimizing for take rate before there is liquidity to take from.

## Founder snapshot

- **Product:** Stack — marketplace connecting solo home-improvement contractors (handypeople, painters, electricians) with homeowners in a single metro.
- **Team:** Two co-founders (one ex-PM, one ex-operations).
- **Stage:** v1 web app live, 80 contractors signed up across 5 categories citywide, 6 transactions completed in 6 weeks.
- **Cash:** ~$80k in pre-seed, ~9 months runway.

---

## Step 1 — Intake (`00_product_intake`)

| Field | Answer |
|---|---|
| Business model | Two-sided marketplace, take-rate (15% on completed jobs) |
| Current ACV/AOV | $340 average job value |
| Geography | One US metro (Austin) |
| Current traffic | 1,200 weekly homeowner visitors, 80 supply (contractors) |
| Match rate | 6 transactions / 230 demand-side requests = **2.6%** |
| Supply utilization | 6 jobs / 80 contractors = **7.5%** |
| Supply concentration | 32 painters, 28 handypeople, 12 electricians, 5 plumbers, 3 movers |

**Founder framing:** "We need more demand. Should we run paid ads?"

**Skill response:** stop and look at the numbers. The marketplace literature flags healthy match rate >40% and supply utilization >30%. Both metrics here are **below the warning thresholds**. Adding demand to a low-liquidity marketplace produces a worse experience for new buyers, who churn and tell people the marketplace doesn't work.

This is the first kill/pivot/narrow signal: **liquidity, not demand.**

---

## Step 2 — Segment scoring — supply side (`02_icp_jtbd_segment_map`)

Treat the *supply* side as the primary segment, because in marketplaces with a "hard side," that's the seed.

| Factor | Painters | Handypeople | Electricians | Plumbers |
|---|---:|---:|---:|---:|
| Pain (slow weeks/marketing burden) | 5 | 4 | 3 | 3 |
| Trigger (regular dead patches Mar–Apr) | 5 | 3 | 2 | 2 |
| WTP (15% take rate) | 4 | 3 | 4 | 4 |
| Reachability | 4 (Facebook groups, supply runs at Sherwin) | 3 | 2 (regulated, certs needed) | 3 |
| Switching cost | 2 | 2 | 4 | 4 |
| **SAS (numerator/denominator)** | **800/3** = 267 | **216/3** = 72 | **48/5** = 10 | **72/5** = 14 |

**Decision:** Narrow supply-side from 5 categories to **just painters in Austin** for the next 90 days. Painters have:
- A clear seasonal trigger (post-winter/Easter dead spot) the marketplace can solve.
- Reachable communities (Facebook groups, paint supplier runs).
- Lower regulatory friction than electrical/plumbing.
- Highest score on the SAS rubric.

Founder's objection: "But that abandons 48 contractors we already onboarded."
Skill response: parking ≠ abandoning. Email them: "We're concentrating on painters this quarter to make matches actually happen; we'll reactivate your category when match rate exceeds 40% — here's why."

---

## Step 3 — Demand-side ICP (`segmentation_icp`)

Now narrow the demand side to match: **homeowners in Austin needing exterior or interior paint within the next 60 days, with a job > $1,000.**

JTBD story:

> When I get a fresh-paint quote that's higher than expected and I don't trust the contractor, I want to compare 3 painters with verified reviews and get an apples-to-apples bid, so I can pick the right one without spending a Saturday calling references. I currently use HomeAdvisor or Nextdoor, but HomeAdvisor sells my number to 5 contractors and Nextdoor reviews are unreliable. I'll switch if reviews are real and bids are formatted the same way; I'll resist if I have to give a phone number before seeing prices.

Implications:
- **Don't ask for phone first** — competitor anti-pattern.
- **Standardize bid format** — comparison is the value.
- **Show review verification** — the wedge.

---

## Step 4 — Competitive teardown (`browsing_recipe`)

Competitors browsed (retrieval 2026-04-23): HomeAdvisor, Thumbtack, Nextdoor, Yelp Services, Angi, plus the substitute "ask in neighborhood Facebook group."

Norms:
- All charge contractors per-lead (not per-job).
- All require homeowner phone before showing pricing.
- No competitor verifies reviews against completed jobs (only signed-in users).

Gaps:
- **Trust gap:** review verification is genuine whitespace.
- **Pricing gap:** take-rate (15% on completed) flips contractor incentives — they only pay when paid.
- **UX gap:** comparison page without phone-first.

Three positioning angles imply: lead with verified-review trust, lead with take-rate vs. lead-cost, lead with comparable bids.

---

## Step 5 — Positioning (`04_positioning_messaging_copy`)

**Statement:**

> Stack is a paint-job marketplace for Austin homeowners who want comparable bids from verified painters. Unlike HomeAdvisor or Thumbtack, every painter on Stack is review-verified against completed jobs and bids are standardized side-by-side, so homeowners can decide without giving a phone number first. Painters pay 15% only when a job completes — no lead fees.

**Hero, after lint:**

> Three verified Austin painter bids, side-by-side, in 24 hours. No phone number required.

(`copy_lint.py landing.md` → 0 findings.)

---

## Step 6 — Pricing / packaging (`05_pricing_packaging_offer`)

Take-rate is the right model here, not subscription, because:
- Contractor wins only when matched → zero downside risk for supply.
- Standardizes incentives across both sides.
- Take-rate research (Sharetribe, NFX) puts services marketplaces at 10–25%; Stack at 15% sits mid-range.

Risk reversal:
- **Supply:** "First 5 jobs, we waive the 15%. Pay nothing until you book."
- **Demand:** "If we can't deliver 3 bids in 24 hours, we'll personally call painters until we do."

The personal-call offer is concierge — explicitly not scalable, but appropriate during cold-start (case studies 100% support this for first-50 transactions).

---

## Step 7 — Cold-start playbook (`marketplace_network` — proposed reference; for now: NFX cold-start tactics)

Operational moves before any acquisition spend:

1. **Single side, single niche, single geo** — painters in Austin only.
2. **Concierge match** — co-founders manually call painters when a request comes in until automation is reliable. Track time-to-first-bid as a metric.
3. **Seed supply density** — get from 32 painters to 80+ before reopening demand acquisition. Tactic: founder visits 3 paint suppliers (Sherwin-Williams, Benjamin Moore, Behr Pro) and signs up painters at the counter with the no-fee pilot.
4. **Free first-5-jobs offer** to supply removes the "is this worth my time?" objection.
5. **Concierge bid formatting** — co-founder manually rewrites the first 50 bids into the standard format until painters internalize it.

Goal: **first 10 completed transactions per week, then 25, then 50.** Not "more visitors."

---

## Step 8 — Experiment table (`07_experiment_plan`)

| # | Experiment | Side | Metric | Threshold | Decision rule |
|---|---|---|---|---|---|
| 1 | Visit 3 paint suppliers + 5 Facebook groups, sign up painters with no-fee pilot | Supply | Painters signed in 14 days | ≥ 30 (target: 80 total) | <15: kill supplier-counter tactic; ≥ 30: continue |
| 2 | Concierge bid formatting on every request | Both | Match rate (request → 3 bids in 24h) | ≥ 60% | <40%: not enough supply; pause demand |
| 3 | Demand acquisition test: post in 2 Austin homeowner subreddits, neighborhood newsletter | Demand | Qualified requests/week | ≥ 25 | <10: positioning unclear; >25 with low match rate: throttle and grow supply first |
| 4 | First-job experience NPS-style 1-question survey | Both | "Would you book again?" | ≥ 70% | <50%: rebuild matching/onboarding before scaling |

Stats note: with ~25 transactions per week early, frequentist A/B is impossible. Founder uses **`stats_cli.py bayes`** weekly to compare match-rate before/after each operational change. Rough decision rule: P(post > pre) ≥ 0.90 to keep a change, else revert.

---

## Step 9 — Funnel and retention (`06_funnel_instrumentation`)

Marketplace metric tree (adapted starter):

```
North star: Completed jobs per week per active demand user
├── Supply liquidity (utilization)
│   ├── Painters with ≥ 1 job last 30 days / total active painters
│   └── Time-to-first-job for new painter
├── Demand fulfillment
│   ├── Match rate (request → 3 bids ≤ 24h)
│   └── Bid-to-booking rate
├── Repeat
│   ├── Demand: bookings per cohort week
│   └── Supply: jobs per painter per month
└── Take-rate health
    ├── Revenue per match
    └── Disintermediation rate (off-platform messaging)
```

Activation events:
- **Supply:** painter completes first job through Stack with payment cleared.
- **Demand:** homeowner books a painter and the job completes.

---

## Step 10 — Decision (`09_kill_pivot_narrow`)

After 90 days of the narrowed playbook:

| Metric | Pre-narrow | Post-narrow (Day 90) | Verdict |
|---|---:|---:|---:|
| Active painters in Austin | 32 | 94 | + |
| Painter utilization (jobs/30d) | 7.5% | 38% | + (above 30% threshold) |
| Match rate (req → 3 bids in 24h) | 2.6% | 67% | + (above 40% threshold) |
| Weekly completed jobs | 1.0 | 14.2 | + |
| Take-rate revenue/week | $51 | $725 | + |
| Disintermediation rate | unknown | 11% | watch — flag for product (in-app messaging, payment) |

**Result:** liquidity targets reached. Per the marketplace cold-start kill rule (90 days, 1 city/vertical), Stack passes. Decision: hold geo + vertical for one more 90-day window, then expand to a *second* category in Austin (handypeople — second-highest SAS), not a second city.

Disintermediation now becomes the priority risk; PM scopes in-app messaging and Stripe Connect-mediated payments for next quarter.

---

## What the skill produced (artifact summary)

1. Forced the founder off the "more demand" frame onto the liquidity frame.
2. Narrowed 5 categories → 1; kept founder from expanding to second city.
3. Defined the seed side (supply, painters) and the seasonal trigger (Mar–Apr dead patch).
4. 15% take-rate defended against literature ranges.
5. Pre-registered match-rate and utilization thresholds.
6. Replaced unrunnable A/B math with weekly Bayesian comparisons via `stats_cli.py bayes`.
7. Identified disintermediation as the next-window risk before it becomes a churn problem.

## What the skill protected the founder from

- Burning $20k of remaining runway on paid ads to a low-liquidity marketplace.
- Adding a second city before the first city's match rate reached threshold (the canonical cold-start failure mode).
- Lowering take-rate to "compete" before liquidity, which would have produced an unprofitable marketplace.
- Calling the matchmaking concierge work "unscalable" and skipping it — the case studies in NFX literature uniformly endorse manual matching during cold-start.
