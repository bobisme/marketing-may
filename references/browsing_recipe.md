# Browsing Recipe

Load when inspecting live competitor pages, pricing pages, reviews, search behavior, or AI-search citations.

The skill mandates browsing for anything likely to have changed (pricing, positioning, reviews, channels). This file makes that browsing structured, comparable across vendors, and bounded — so research feeds the templates and scripts cleanly instead of producing impressionistic notes.

## Operating rules

1. **Extract before you opine.** Pull the structured rows below before drawing any cross-vendor conclusion.
2. **Quote, don't paraphrase, the hero noun and outcome promise.** Paraphrase loses the comparison.
3. **Record retrieval date and URL** for every claim that ends up in the output.
4. **Distinguish observed fact, inference, hypothesis, recommendation** when transcribing.
5. **Stop when marginal new claim per page < 1**, or when 3 direct competitors + 3 substitutes + 3 reviews per competitor are logged. Whichever first.

## Per-page extraction shapes

### Competitor homepage

Extract one row per competitor:

| Field | What to capture |
|---|---|
| Name + URL | exact domain |
| Hero noun (verbatim) | the category claim — what they say it *is* |
| ICP signal in hero | named role/industry/size? y/n + quote |
| Outcome promise (verbatim) | what changes for the buyer |
| Mechanism (verbatim or "absent") | why it works, in their words |
| Top-of-page proof | logo strip, customer count, named customer? y/n |
| Primary CTA verb | start, book, try, get, request, etc. |
| Secondary CTA verb | if any |
| Pricing visible above the fold? | y/n |
| Implied buyer risk | from the proof intensity above the fold |

Feeds: `assets/templates/03_competitive_intelligence.md`, `scripts/competitor_matrix.py`.

### Competitor pricing page

| Field | Capture |
|---|---|
| Pricing model | flat / tiered / per-seat / usage / hybrid / custom |
| Value metric | seats, events, requests, GB, transactions, etc. |
| Lowest entry price | numeric or `custom` |
| Free tier? | y/n + limits |
| Trial length | days; card required? |
| Money-back / guarantee | text quote |
| Enterprise CTA | "talk to sales" presence |
| Hidden price? | y/n (entire page custom) |
| Discounts | annual prepay %, volume tier breaks |
| Add-on categories | what the pricing page upsells |

One row per competitor; concatenate into the competitors CSV format expected by `scripts/competitor_matrix.py`.

### Reviews / G2 / Capterra / app store / Reddit

For each competitor, sample ≥ 10 reviews spanning ratings 2–5 (skip 1-stars unless the issue repeats).

Bucket every review into:

- **Pain:** what was broken in the buyer's life before this product.
- **Outcome:** what the product enabled.
- **Objection / regret:** what the buyer wishes they had known.
- **Switch trigger:** event that drove them to look (deadline, incident, hire, audit).
- **Alternative named:** what they used before / compared to.

Pull 5 verbatim quotes per bucket per competitor. Quotes feed `scripts/message_miner.py`.

### Search behavior

For 3–5 queries the buyer would actually type (not what you'd type), log:

| Field | Capture |
|---|---|
| Query | exact text |
| Result mix | vendor pages, articles, comparisons, ads, AI overview presence |
| Top 3 organic domains | for category-language calibration |
| "X vs Y" pages present? | y/n + which |
| AI Overview / Perplexity / ChatGPT answer | does it answer the query and cite which domains? |
| Your domain present? | y/n in organic, ads, AI citations |

If "X vs Y" pages exist, those are the buyer's working comparison set — your hero must address those alternatives, not the ones you wish they'd compare to.

### AI search citation pattern

AI assistants (ChatGPT, Perplexity, Google AI Overviews, Gemini, Claude) increasingly mediate buyer research. They cite differently than they rank — only ~38% of AI Overview citations come from top-10 organic in early 2026.

For each buyer query in the search behavior step, also capture:

| Field | Capture |
|---|---|
| AI engines tested | which ones |
| Citations chosen | URLs cited per engine |
| Cited content shape | leading number, definition, table, FAQ, quote, or prose? |
| Wikipedia / Reddit / YouTube share | rough % of citations from these |
| Your domain cited? | y/n per engine |
| If yes: which page? which claim? | so you can preserve it on rewrites |

Patterns that get cited (current, principle-led):

- **Leading-numeric or definition opener** in the first 40–60 words of the answer.
- **Comparison tables** with named tradeoffs ("X vs Y").
- **Standalone-extractable claims** (not buried in 600-word intros).
- **Structured data** (Article, FAQPage, HowTo, Q&A schema).
- **Date and named entities** in the visible text.

Don't write content *for* AI — write content where each section's first 40–60 words could be lifted as a complete answer.

## Stopping rules

Stop browsing when ANY of the following:

- ≥ 3 direct competitors + ≥ 3 substitutes + ≥ 3 reviews per competitor logged, AND
- the last page added fewer than 1 new claim to your aggregate notes; OR
- you have answered the original user question and any further detail won't change the recommendation.

Browsing rabbitholes (30+ tabs, hours of reading) usually mean the segment is too broad. Stop, narrow, restart.

## What goes back to the user

After browsing, produce in this order:

1. **Aggregate competitor row** (or rows) — one line per vendor, comparable.
2. **3–5 norms** — what's true across the category (pricing model, hero noun, primary CTA).
3. **3–5 gaps** — what's missing (proof type, segment named, channel ignored, objection unhandled).
4. **Whitespace** — 2–3 specific positioning angles the gaps imply.
5. **Inline citations** — URL + retrieval date for any claim that load-bears a recommendation.

If the user asked a specific question (e.g., "is our hero good?"), answer that question first, then attach the structured rows as evidence — not the other way around.
