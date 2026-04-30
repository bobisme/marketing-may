# Modern Channels — AI Search, Podcasts, Communities, Newsletters

Load alongside `channels_outbound.md` when planning channel mix in 2026. This file covers channels that have shifted enough since classic channel taxonomy was written that the old playbooks miss the point. Numbers are directional and dated; verify with current sources before betting.

## How to read this file

For each channel:

- **When it works** — preconditions that distinguish "this could work for us" from wishful thinking.
- **First test** — minimum experiment with a pre-registered threshold.
- **Kill rule** — observable outcome that says "stop, this isn't ours."
- **What you optimize** — the metric that's actually predictive (not the vanity metric).

If a channel doesn't pass its first-test threshold inside the kill window, do not "tune" your way to growth there. Pick a different channel.

---

## AI search / generative engines (AEO / GEO)

ChatGPT browsing, Perplexity, Google AI Overviews, Gemini, Claude. The fastest-growing top-of-funnel for technical buyers in 2026 — and citation patterns differ enough from organic search that "good SEO" no longer guarantees AI-citation share.

### When it works

- Your buyer asks specific, comparison-shaped questions ("X vs Y for Z").
- Your category has searchable language at all (skip if pre-category).
- You can produce content with leading-numeric answers, comparison tables, and structured data.
- Your domain already has some traditional search authority (AI engines lean on it as a prior, just less than they used to).

### What gets cited (current patterns, 2026)

- **Leading-numeric or definition opener** in the first 40–60 words.
- **Comparison tables** with named tradeoffs (X vs Y vs Z).
- **Standalone-extractable claims** — each section answers a question on its own.
- **Structured data** — Article, FAQPage, HowTo, Q&A, SpeakableSpecification, VideoObject, Organization schema. Pages with structured data are cited ~3× more often.
- **Visible dates and named entities.**
- **Wikipedia, Reddit, YouTube** disproportionately cited — community-validated content earns trust.

Citations from top-10 organic dropped from ~76% to ~38% in early 2026 — rankings still correlate but no longer guarantee AI-citation share.

### First test

Pick 5 buyer queries (the literal sentences a buyer would type). Run each through ChatGPT browsing, Perplexity, and Google AI Overviews. Log:

- Are you cited?
- If yes, which page and which claim?
- Top 3 cited domains per engine.
- Cited content shape: leading number, definition, table, FAQ, prose.

Then: rewrite your top 3 traffic-dependent pages so each section's first 40–60 words could be lifted as a complete answer. Add structured data. Re-run after 3–4 weeks.

**Threshold:** appear in ≥ 1 of 3 engines for ≥ 2 of 5 queries within 90 days of rewrite. Below that, the page is not citation-shaped.

### Kill rule

If after 90 days of rewrite + structured data + buyer-language alignment you are still cited for < 1 query in any engine, the issue is upstream — domain authority, category language, or content depth — not page format. Don't keep tweaking pages.

### What you optimize

- **Citation share for buyer-shaped queries**, not generic traffic.
- **Click-through from AI engines** (track via referrer when possible).
- **Conversion rate of AI-referred sessions** (often 2-3× organic if the question and citation are sharp).

### Anti-patterns

- Writing content *for* AI engines (LLM-generated walls of generic prose). Engines down-rank obviously-AI text.
- Stuffing FAQ schema on every page.
- Treating AI search as "another SEO channel" rather than a different surface with different conventions.

---

## Podcasts (sponsorship + founder-led appearance)

Two distinct plays: sponsoring others' podcasts, or appearing on them. Different math, different threshold.

### When it works

- ACV ≥ $500 (lower ACV rarely pays back podcast attribution windows).
- Buyer listens to ≥ 2 named pods *you can name without research*.
- Founder is articulate and the topic isn't generic ("we built a SaaS" vs "we cut webhook-debug time from 4 hours to 30 seconds for solo SaaS founders on Stripe").
- You can attribute via vanity URL, code, or self-reported attribution survey.

### Sponsorship rates (directional, 2026)

- General-interest CPM: $20–$40
- Business / marketing niches: $35–$60
- B2B / finance: $50–$100+
- Niche B2B (small audience, high-value buyer) frequently goes flat-rate ≈ $125 CPM equivalent
- Host-read mid-roll: $20–$50 CPM ($50–$100+ for niche B2B)

A B2B podcast with 8,000 downloads at $1,000 flat-rate = $125 effective CPM — premium but justified by audience quality.

### First test (sponsorship)

Pick **one** pod. Mid-tier audience (50–500 listeners *who match your ICP*, not absolute size). Buy 1 host-read mid-roll spot with a unique landing page or vanity code.

**Pre-register thresholds:**

| Result | Action |
|---|---|
| ≥ 5 ICP-qualified visits per 1,000 downloads | strong, test 2 more pods in the same niche |
| 1–5 visits per 1,000 | weak; check landing page first, then test different ICP angle |
| < 1 visit per 1,000 | wrong audience, wrong host, or wrong offer — kill |

**Don't measure CPM as success.** Measure cost-per-qualified-meeting or cost-per-trial, with a realistic 30–60 day attribution window.

### First test (founder-led appearance)

5 targeted pitches to mid-tier pods (50–500 listeners) with offer-aligned topics. Threshold: ≥ 1 pod books, ≥ 5 qualified replies from outbound after the episode releases.

### Kill rule

3 sponsorships across 2 niches with no qualified-meeting attribution in 60 days = the channel doesn't fit. Don't do "one more test, but different copy" — switch channels.

### What you optimize

- **Cost per qualified meeting**, not CPM, downloads, or impressions.
- **Reply quality** to outbound that references the episode (replies that book, not "thanks for being on Y").

### Anti-patterns

- Sponsoring pods because the host is famous. Famous-but-wrong-audience converts at zero.
- Treating downloads as evidence. Plenty of pods inflate download counts.
- Skipping the unique landing page or code. Without it you can't tell the channel from the noise.

---

## Communities (Discord, Slack, Reddit, niche forums)

Communities are durable demand sources when treated as ongoing relationships, instant brand poison when treated as broadcast channels.

### When it works

- Your buyers congregate in named communities you can access without violating norms.
- You can contribute on topic — answer real questions — without your product mentioned.
- Your team has 5+ hours/week to participate (this is a person, not a campaign).
- The community has ≥ 1 named maintainer / mod whose trust you can earn.

### Discord vs Slack vs Reddit (2026)

- **Discord** has overtaken gaming as a non-gaming community platform. Best fit for technical / developer audiences. Server discovery, voice, low-friction. ReactiFlux (~200k engineers), niche dev/AI servers thrive here.
- **Slack** still dominant for B2B "work" communities (CMX, RevGenius, indie SaaS slacks). Limits social engagement vs Discord — feels like work to users.
- **Reddit** is the largest source of pain language and product feedback. Disproportionately cited by AI engines. Hard to promote on; great for problem mining and answering.

### First test

Pick **one** community. Spend 4 weeks contributing without product mention:

1. Answer 20 pain threads / questions in your domain. Save the language verbatim → feed to `message_miner.py`.
2. Track DMs received (a clean signal of interest).
3. Track community-driven signups (vanity URL or self-reported attribution).

Then ask one moderator: "Is it OK if I share what we built when it's relevant?" If yes, share carefully — once per genuine match, max.

**Pre-register:**

| Result after 4 weeks | Action |
|---|---|
| ≥ 3 inbound DMs that ask about you OR your space | promising; continue, slowly increase share frequency |
| 1–3 DMs | early; another 4-week window |
| 0 DMs after 20+ contributions | wrong community or wrong topics — switch |

### Kill rule

8 weeks of consistent contribution with no inbound DMs and no community-driven signups = the audience is wrong. Try a different community before tweaking your approach.

### What you optimize

- **Inbound DMs that mention your space or product** (not "great post" replies).
- **Community-attributed signups** with retention ≥ 1.5× org average. Community traffic that doesn't retain is worse than no traffic.

### Anti-patterns

- "Drive-by promotion" — posting your product in a thread once and leaving. Community managers ban this.
- Hiring SDRs to "engage" in communities. Pattern is detectable in 1–2 messages.
- Picking communities by member count. 50k members of the wrong audience converts at 0; 500 of the right audience can carry a quarter.
- Slack-vs-Discord by founder preference. Pick by where the *buyer* hangs out.

---

## Newsletter sponsorships

Underrated for B2B; cheaper than ads, higher trust than display, easier attribution than podcasts.

### When it works

- Your buyer reads ≥ 1 newsletter with a clear ICP overlap.
- The newsletter has ≥ 30% open rate and ≥ 2% click rate (ask before paying).
- The sponsor format is native (sponsored mention by author) not display-ad.
- ACV makes the math work — typical sponsorship $500–$5k flat for niche.

### First test

Sponsor **one** issue. Pre-compute the math:

```
expected_signups = subscribers × open_rate × click_rate × landing_CVR
expected_qualified = expected_signups × ICP_qualification_rate × activation_rate
```

If `expected_qualified < 1`, the math doesn't support the sponsorship — find a different newsletter, or a different format (e.g., guest post, take-over).

**Pre-register:** 1 qualified meeting per $1k spent at minimum, or proof the LTV from one customer pays back 5× the spend.

### Kill rule

3 newsletter sponsorships in the same niche, all below threshold = the niche or the offer is wrong. Reconsider before testing a 4th.

### What you optimize

- **Cost per qualified signup**, not impressions or clicks.
- **Author endorsement quality** — generic ad reads convert 3-5× worse than authentic ones.

### Anti-patterns

- Buying newsletter sponsorships before you have a working landing page. The newsletter exposes flaws you'd otherwise blame on traffic quality.
- Negotiating by CPM. Ask for total subscribers AND open rate AND historical sponsor results.
- Picking by aesthetic. Pick by audience overlap with your ICP.

---

## How these compose

For a typical small-team B2B in 2026, the natural sequence:

1. **Communities** (cheap, slow, also produces buyer language for everything else).
2. **AEO/GEO** rewrites of top traffic pages (cheap, medium speed, compounds).
3. **One newsletter sponsorship** (cheap, fast feedback on offer + landing).
4. **One podcast sponsorship** (mid-cost, slower feedback, learn audience quality).
5. Only after the above produce qualified-intent: **paid search / paid social** (highest cost, fastest signal — but only on a converting offer).

Anti-pattern: starting with paid because it's "fastest." Paid is fastest at burning money on a non-converting offer. Use cheap channels to find what converts, then buy more of the conversion.
