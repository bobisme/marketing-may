# Marketing Algorithms and Scoring Systems

These formulas are decision aids, not truth machines. Use them to make assumptions explicit, compare options, and force learning.

## 1. Evidence Tensor

Represent every major claim as:

```text
Evidence = [source_quality, behavioral_strength, recency, segment_match, volume, contradiction_penalty]
EvidenceScore = (source_quality × behavioral_strength × recency × segment_match × log2(1 + volume)) - contradiction_penalty
```

Behavioral strength scale:

| Signal | Score |
|---|---:|
| Vague interest, likes, social views | 1 |
| Specific pain described from past behavior | 2 |
| Click, signup, download, or demo view | 3 |
| Sales call, data shared, stakeholder intro | 4 |
| Paid pilot, deposit, LOI with real terms | 5 |
| Repeat usage, expansion, referral, renewal | 6 |

Decision rule: do not scale acquisition from evidence below 3 unless the goal is pure discovery.

## 2. Segment Attractiveness Score

```text
SAS = (Pain × TriggerFrequency × Budget × Reachability × ProofFit × StrategicFit)
      / (1 + SwitchingCost + SalesFriction + ComplianceRisk + ChannelCrowding)
```

Score every variable 1–5. Pick the top 1–2 segments for testing. If two segments are close, prefer the one with faster feedback cycles and clearer buyer triggers.

## 3. Offer-Market Fit Score

```text
OMF = Urgency × BuyerPower × ProblemSpecificity × OutcomeValue × ProofCredibility × RiskReversal
      × ChannelAccess × DeliveryFeasibility
```

Red flags:

- Urgency ≤ 2: lead with education or choose a different trigger.
- BuyerPower ≤ 2: sell to a higher-level buyer or repackage.
- DeliveryFeasibility ≤ 2: narrow scope before promising outcomes.
- ProofCredibility ≤ 2: run concierge pilots before publishing big claims.

## 4. Category Gravity Index

Use this to decide category entry vs. category creation.

```text
CGI = BuyerVocabulary + ExistingBudget + SearchVolume + ComparableVendors + Analyst/CommunityLanguage
      - DifferentiationPressure
```

Interpretation:

| CGI | Category move |
|---:|---|
| 18–25 | Enter category; compete on wedge, proof, speed, price, UX, or segment focus. |
| 11–17 | Enter adjacent category; create subcategory language around the wedge. |
| 5–10 | Use problem-first positioning; do not force a new category yet. |
| <5 | Category creation risk is high; validate with paid discovery before building brand. |

## 5. Objection Entropy

Objections are more actionable when concentrated. After calls/reviews, count objection categories.

```text
Entropy = -Σ p(objection_i) × log2(p(objection_i))
```

Decision rule:

- Low entropy: fix the dominant objection in copy, proof, pricing, onboarding, or product.
- High entropy: segmentation is probably too broad, or the offer is vague.

## 6. Proof Debt

```text
ProofDebt = Σ(BuyerRisk_i × ClaimImportance_i × CurrentProofGap_i)
```

Proof types by risk:

| Risk | Proof asset |
|---|---|
| Product works | Live demo, sample output, sandbox, benchmark |
| Business impact | Case study, ROI calculator, before/after metrics |
| Security/privacy | Security page, DPA, SOC 2/ISO status, architecture notes |
| Support/switching | Migration guide, concierge setup, implementation plan |
| Credibility | Founder story, customer logos, testimonials, community validation |

Prioritize the proof asset with the largest debt.

## 7. Experiment Expected Learning Value

```text
ELV = (Impact × Confidence × Reach × Learning × StrategicFit × Speed)
      / ((1 + Cost) × (1 + Risk + TrustRisk))
```

Use `scripts/experiment_prioritizer.py` to rank candidate tests.

## 8. Funnel Constraint Diagnosis

```text
QualifiedAcquisition = ICPVisitors × ProblemFitRate × IntentRate
Activation = QualifiedSignups × FirstValueRate
Revenue = ActivatedAccounts × WTPFit × SalesCompletionRate
Retention = PaidAccounts × Habit/WorkflowEmbed × OutcomeRepeatability
```

If acquisition is weak: segment, channel, category vocabulary, or offer problem.
If activation is weak: onboarding, promise mismatch, product friction, missing setup data.
If revenue is weak: WTP, buyer authority, proof, packaging, procurement friction.
If retention is weak: problem frequency, workflow embed, ongoing value, support, product depth.

## 9. Pivot / Narrow / Kill Matrix

| Evidence pattern | Move |
|---|---|
| Strong pain, weak WTP | Repackage for a buyer with budget or reduce service scope. |
| Strong WTP, weak activation | Fix onboarding, implementation, integration, or promise mismatch. |
| Strong activation, weak retention | Find repeat-use job or narrower high-frequency segment. |
| Strong demand, high delivery pain | Productize, template, automate, or narrow ICP. |
| Weak pain, weak WTP, weak activation after 2 cycles | Kill or radically reframe. |
| Scattered objections, no dominant segment | Narrow segment; stop generic marketing. |

## 10. Copy Claim Risk Filter

Every claim must pass:

```text
ClaimAllowed = Specific ∧ Substantiated ∧ SegmentBounded ∧ Non-Deceptive ∧ NoHiddenMaterialTerms
```

A claim that fails substantiation becomes a hypothesis, not marketing copy.
