# Marketplaces & Network-Effects Products

Load when working on a two-sided marketplace, multi-sided platform, or product whose value depends on other users being present (community, social, network-good API). Standard SaaS playbook fails on these because demand has nothing to match against until supply is liquid in a single niche.

## Why a separate reference

Most marketing-skill content assumes a single-buyer product. Marketplaces have:

- **Two (or more) buyers.** Selling to demand without supply makes the product worse.
- **A liquidity precondition.** Adding any acquisition while liquidity is low *destroys* trust, doesn't grow it.
- **A different unit-economics model.** Take-rate vs. subscription, not a free choice.
- **A disintermediation risk.** Buyers and sellers want to leave once introduced — your platform must keep providing value beyond match.

If you treat a marketplace like a SaaS, the SaaS playbook will tell you to "fix demand," and you will scale a leaky bucket.

---

## The cold-start playbook

Source: NFX, Sharetribe, Chen "Cold Start Problem," and case study 02 in this skill.

### 1. Pick one side first

Default: seed the **hard side** — the side that's slower or more expensive to acquire.

- Services marketplace → seed **suppliers** (contractors, providers, hosts).
- Goods marketplace → seed **sellers**, especially anchor SKUs.
- Knowledge / Q&A marketplace → seed **answerers** (experts, contributors).
- Dating / social → seed the side with worse natural reachability.

Why supply default: suppliers have a financial incentive (income), tolerate worse early UX, and gain more from the platform's existence. Demand has alternatives and walks if matches don't appear.

Exception: when supply is already commoditized and trivially listable (e.g., scraping public listings), seed demand instead and use bots/scrapers to simulate supply density during cold-start.

### 2. Single niche, single geo

Marketplaces are **local** even when they look global. A national food-delivery marketplace is actually 50 city-marketplaces stacked on top of each other. Liquidity is per-city, per-vertical.

For first 90 days:

- **One vertical.** "Painters" not "home services."
- **One geo.** "Austin" not "Texas."
- **One use case.** "Exterior paint jobs >$1,000" not "any paint work."

When founders insist this is "too small," remind them: the goal is the first 50 transactions, not market share. Network goods compound only after liquidity exists somewhere.

### 3. Concierge before automation

Manually match the first transactions. Examples:

- Founder calls suppliers when a request lands until algorithm is reliable.
- Founder rewrites bids/listings into a standard format until suppliers internalize it.
- Founder onboards both sides personally, captures friction language for product.

This is *not* unscalable — it's unscalable on purpose, because automating the wrong thing is the failure mode you're avoiding. NFX, Sharetribe, and Chen all endorse this for first-50.

### 4. Seed with non-customer value

Reasons supply joins before demand exists:

- **Financial** — first N transactions free of take-rate.
- **Workflow** — better tools for their existing customers (CRM, scheduling, payments).
- **Distribution promise** — "we'll bring you N customers in 90 days or refund your time."
- **Status** — verified / featured supplier badge that has value beyond your platform.
- **Forced quality** — "we've already screened these buyers."

Pick the one that's *true now*, not aspirational.

### 5. Don't expand prematurely

The cardinal sin of marketplace growth is launching a second city or vertical before the first hits liquidity targets. You divide your founder attention by 2 and your liquidity by ~4 (because liquidity is roughly proportional to density²).

Holding rule: do not expand to a second geo or vertical until the first sustains liquidity targets (below) for 4 consecutive weeks.

---

## Liquidity targets (directional)

These are warning thresholds, not goals. Below them, more demand makes things worse.

### Services marketplaces

| Metric | Healthy | Warning | Crisis |
|---|---:|---:|---:|
| Demand match rate (request → completed match in target window) | >40% | <25% | <15% |
| Supply utilization (jobs per active supplier per period) | >30% | <15% | <5% |
| Time to first match | <24h | >72h | >7d |

### Goods marketplaces

| Metric | Healthy | Warning | Crisis |
|---|---:|---:|---:|
| Search → purchase rate | >5% | <2% | <1% |
| % listings with ≥ 1 view in 30d | >70% | <40% | <20% |
| Repeat buyer rate (90d) | >25% | <10% | <5% |

### Two-sided knowledge / Q&A

| Metric | Healthy | Warning | Crisis |
|---|---:|---:|---:|
| Question answered rate (24h) | >60% | <30% | <15% |
| Median time to first answer | <2h | >12h | >24h |
| Repeat questioner rate | >30% | <15% | <5% |

If you're below "warning," **stop acquiring the abundant side and seed the constrained side** until you're back above warning before you turn marketing back on.

---

## Take-rate ranges (directional, 2026)

| Type | Common range | Notes |
|---|---|---|
| Services (skilled labor) | 10–25% | Higher when matching solves real friction (trust, payment, dispute) |
| Services (commodity tasks) | 5–15% | Race to the bottom; defensibility weak |
| Physical goods | 5–15% | Logistics + payments often eat margin |
| B2B vertical (high ACV) | 3–10% | Disintermediation risk grows with ACV; offset with workflow lock-in |
| Digital goods / content | 15–30% | Higher tolerable because no logistics |
| Rentals (long-tail) | 10–20% | Insurance + dispute + escrow services justify |

Pricing principle: take-rate is the price your platform charges for **solving the matching problem**. If the platform doesn't materially reduce friction beyond match (no payments, no dispute, no quality signal), take-rate will erode under disintermediation pressure no matter what you set it at.

Watchout: a low take-rate doesn't make supply happier — it telegraphs that the platform doesn't add much value.

---

## Disintermediation defense

Once a buyer and seller have met on your platform once, they have an incentive to deal off-platform next time. Your job is to make leaving the platform *worse* for them than staying.

### Defenses, ordered by effectiveness

1. **Embedded payments + escrow** — deal off-platform = lose dispute and chargeback protection.
2. **Trust + review layer** — supplier's reputation lives only on the platform.
3. **Repeat-customer pricing** — reward the supplier for repeat customers via lower take-rate or rebate.
4. **Workflow tools both sides depend on** — calendar, comms, contracts, invoicing.
5. **Quality scoring with consequences** — supplier loses placement / badge if they go off-platform.
6. **Insurance** — damage / no-show / quality insurance available only via platform.
7. **Demand acquisition supplier can't replicate** — the supplier's reason to stay is "you bring me leads I can't get elsewhere."

Track **disintermediation rate** as a guardrail: % of off-platform messages, % of repeat customers booking direct, supplier churn cohorted by months-active.

---

## Channel mix

Marketplaces have asymmetric channel preferences by side.

### Supply acquisition

- **Targeted outbound** — list of suppliers in vertical+geo. Cold email, LinkedIn, in-person visits.
- **Vertical communities** — supplier Facebook groups, trade associations, supply-side forums.
- **Single-geo paid** — Facebook / Instagram targeted by job title in geo radius.
- **Direct biz-dev** — founder visits trade shows, supplier conferences, supply hubs (paint stores, contractor expos).
- **Anchor partnerships** — sign one named supplier whose presence attracts others.

### Demand acquisition (only after supply density)

- **SEO long-tail** — "[service] in [city]" pages, structured data, schema for AI engines.
- **Retargeting** — visitors who saw listings but didn't book.
- **Adjacent-platform partnerships** — integrations with tools demand already uses.
- **Direct response paid** — Google search on transactional intent, geo-targeted.
- **Referrals** — post-completion referral with both-side incentive.

Anti-pattern: paid demand acquisition while liquidity is below "warning." You're paying to make people leave dissatisfied.

---

## Kill / narrow / pivot rules

| Evidence | Default move |
|---|---|
| Liquidity below warning after 90 days at single niche/geo | Narrow further (sub-niche, sub-geo) before adding spend |
| Strong supply, weak demand, high listing decay | Demand acquisition or value-prop is broken — stop adding supply |
| Strong demand, weak supply | Concierge match plus aggressive supply-side incentive (free first N) |
| Liquidity hits, then drops as you scale | You expanded too early — refocus on original niche, scale slower |
| Disintermediation rate >25% | Add escrow / payments / repeat-customer incentive before more growth |
| CAC payback impossible at current take-rate | Raise take-rate, narrow to higher-value transactions, or kill |
| Supply churn >40% in 90 days | Supplier value-prop is broken — utilization too low or take-rate too high |
| Both sides growing but transactions flat | Matching algorithm or trust layer broken; not a marketing problem |

---

## What good looks like at year-1

For a single-niche, single-geo marketplace:

- ≥ 25 transactions/week sustained for 4 consecutive weeks.
- Match rate above warning threshold.
- Supply utilization above warning threshold.
- Disintermediation rate < 15%.
- ≥ 1 case study from each side (supplier earning, buyer outcome) usable in marketing.
- Defined repeat-rate cohort behavior — at least one cohort with >25% repeat at week 8 (per `references/metric_trees.md` retention shape).

Below this, do not expand. Above this, expand to the *second-best vertical in the same geo* before opening a second geo.

## References

- NFX, "19 Tactics to Solve the Chicken-or-Egg Problem and Grow Your Marketplace."
- Andrew Chen, *The Cold Start Problem*. Network effects, hard side, atomic networks.
- Sharetribe, "Chicken-and-egg problem in marketplaces."
- David Ciccarelli, "Marketplace cold-start product marketing playbook."
