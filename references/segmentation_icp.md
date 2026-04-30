# Segmentation, ICP, JTBD, Buyer Psychology

Load when choosing a segment, defining an ICP/JTBD, scoring segments, or diagnosing buyer objections.

## Contents

- Qualification ladder
- Core definitions (ICP, JTBD, offer-market fit, qualified intent)
- Segment priority algorithm
- Buyer psychology and objection model

## Qualification ladder: signal vs vanity

Use this ladder to interpret marketing signals. Higher rungs matter more.

| Level | Signal | Typical meaning | Treat as |
|---:|---|---|---|
| 0 | Impressions, views, likes, generic traffic | Attention | Vanity unless tied to qualified segment and conversion |
| 1 | Scroll, time on page, social comment | Curiosity | Weak signal |
| 2 | Click-through from relevant context | Interest | Weak-to-moderate if source has buyer intent |
| 3 | Email signup, waitlist, ungated download | Low-friction intent | Moderate only if ICP-qualified |
| 4 | Reply, survey completion, booked call | Active intent | Stronger |
| 5 | Demo request, trial start, integration setup | Buying/exploration intent | Strong |
| 6 | LOI, preorder, paid pilot, deposit | Economic intent | Very strong |
| 7 | Activation event completed | Product value reached | Very strong |
| 8 | Renewal, expansion, referral | Retained value | Strongest |

Default rule: do not celebrate a lower-rung metric unless it predicts a higher-rung metric.

## Core definitions

### ICP

An Ideal Customer Profile is the narrowest buyer group for whom the product delivers urgent, differentiated value, can be reached through known channels, can pay, and can adopt without excessive friction.

ICP template:

```text
For [specific buyer role/person/team] in [specific context], who currently [painful workflow/status quo], triggered by [event], our product helps them achieve [measurable outcome] by [differentiated mechanism], unlike [alternative], with proof from [evidence]. They can pay because [budget/economic value], and can be reached through [channel].
```

### JTBD

A Job-to-be-Done is the progress a buyer is trying to make in a specific circumstance, including functional, emotional, and social forces.

JTBD story template:

```text
When [trigger/circumstance], I want to [make progress], so I can [functional outcome], feel [emotional outcome], and be seen as [social outcome]. I currently use [alternative/status quo], but it fails because [struggle]. I will switch if [switch condition] and I will resist because [anxiety/inertia].
```

### Offer-market fit

Offer-market fit exists when the bundle of promise, price, packaging, proof, risk reversal, and buying path makes a target buyer willing to take a costly next step.

Product-market fit answers: "Does the product solve a valuable problem?"
Offer-market fit answers: "Can this buyer understand, trust, buy, adopt, and justify this offer now?"

### Qualified intent

A buyer action is qualified when it is taken by a plausible ICP, in a context connected to the problem, with enough friction to indicate seriousness, and with a next-step path toward purchase or activation.

## Segment priority algorithm

Score each segment from 1–5. Use decimals if useful. Penalize uncertainty.

```text
Segment Score =
(Pain × Trigger × WTP × Reachability × Differentiation × Proof Availability)
/ (Sales Complexity × Switching Cost × Compliance Risk × Build/Service Burden)

Confidence-adjusted Score = Segment Score × Evidence Confidence
```

Where:

| Factor | 1 | 3 | 5 |
|---|---|---|---|
| Pain | Mild annoyance | Frequent costly problem | Existential, revenue, legal, security, or time-critical |
| Trigger | Rare/unclear | Recurring workflow event | Acute deadline, budget cycle, incident, regulation, new role |
| WTP | No budget | Some budget | Clear owner and economic value |
| Reachability | Hard to find | Reachable with work | Concentrated communities/lists/search terms |
| Differentiation | Commodity | Some edge | Unfair advantage or clear wedge |
| Proof availability | No proof possible yet | Demo/case plausible | Strong proof, references, benchmarks, data |
| Sales complexity | Self-serve | Light sales | Enterprise committee/procurement |
| Switching cost | No change | Some setup | Data migration, politics, retraining, contracts |
| Compliance risk | Low | Some claims/privacy concerns | Regulated claims/data/industry |
| Build/service burden | Already built | Some customization | Heavy custom work/support |
| Evidence confidence | Guess | Some data | Repeated behavioral evidence |

Pick the highest confidence-adjusted score, not the largest theoretical market.

## Buyer psychology and objection model

Treat every buyer as managing four forces:

| Force | Meaning | Marketing task |
|---|---|---|
| Push | Pain with current state | Make the cost of status quo concrete |
| Pull | Attraction to new outcome | Show vivid, credible future state |
| Anxiety | Fear of change | Reduce risk with proof, guarantees, demos, policies |
| Inertia | Habit, sunk cost, politics | Lower switching cost and offer migration path |

Common objections and responses:

| Objection | Hidden fear | Response pattern |
|---|---|---|
| "Too expensive" | Value unclear, budget mismatch, risk | Quantify cost of status quo, show ROI/payback, offer pilot |
| "We already use X" | Switching risk | Show coexistence, migration path, wedge use case |
| "Not a priority" | Trigger absent | Tie to deadline, leakage, opportunity cost, compliance, customer pain |
| "Need to think about it" | Anxiety or missing stakeholder | Provide decision memo, checklist, stakeholder proof |
| "Send me info" | Low urgency or poor fit | Send problem-specific asset and ask commitment question |
| "No budget" | Wrong buyer or timing | Find budget owner, cheaper wedge, or waitlist/nurture |
| "Will it work for us?" | Relevance/proof gap | Segment-specific case, demo using their workflow, benchmark |
