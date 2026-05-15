// ═══════════════════════════════════════════════════════════════════════════
//  teardown.typ — "Safe / Editorial Research-House" report template
//
//  A Typst port of report-safe.html (Claude Design handoff, project
//  "marketing-may"). Recreates the editorial look as proper paged
//  typesetting: paper-white stock, ink black, one hot accent, sans display
//  + serif body, mono numerals, hairline tables.
//
//  Content is data-driven (mirrors report-data.js): a caller passes meta,
//  priorities, sections and appendices; this file owns all styling. To
//  produce a new teardown, swap the data — same render.
//
//  Compile:  typst compile --font-path fonts report.typ report.pdf
// ═══════════════════════════════════════════════════════════════════════════

// ---------- Tokens (1:1 with the CSS :root custom properties) --------------
#let paper      = rgb("#f6f4ee")
#let ink        = rgb("#14110d")
#let ink-soft   = rgb("#4a443a")
#let rule       = rgb("#d9d3c4")
#let rule-soft  = rgb("#ece7d8")
#let tint       = rgb("#efeadb")
#let accent     = rgb("#c8341a")
#let accent-ink = rgb("#f6f4ee")

#let serif = "Source Serif 4"
#let sans  = "Geist"
#let mono  = "JetBrains Mono"

// rem→pt at the CSS root (16px) ; px→pt at 96dpi.  1rem = 12pt, 1px = .75pt
#let rem = 12pt
#let px  = 0.75pt

// Type scale. The source's own print stylesheet drops the body to 10.5pt;
// at 12pt on Letter the lines ran ~80+ chars (too long). 10.5pt body + a
// capped prose measure gives a refined ~66-char column.
#let fs-body    = 10.5pt
#let lh-body    = 0.52em      // ≈ CSS print line-height 1.45 for this serif

// Prose measure (CSS --body-col). Capped well below the full text width so
// running text holds a comfortable line length; tables still get full width.
#let body-col   = 31 * rem

// ---------- Layout geometry ------------------------------------------------
// The § number sits in a margin gutter; kicker, title, rule, body and the
// appendices all share ONE left edge (the source CSS hung body left of its
// own title — fixed here). Tables break out to the full body width.
#let _gutter    = 4 * rem
#let _head-gap  = 1.5 * rem
#let _col-left  = _gutter + _head-gap          // shared text-column left edge
#let _content-w = 8.5in - 2 * 16mm             // text area between margins
#let _body-w    = _content-w - _col-left       // full column width (tables)

// ---------- Small inline helpers (for use inside content) ------------------

// Accent-colored run.
#let acc(body) = text(fill: accent)[#body]

// Inline code: tinted chip with a hairline border (CSS `code`).
#let ic(body) = box(
  fill: tint,
  inset: (x: 3pt, y: 0pt),
  outset: (y: 2.5pt),
  stroke: 0.5pt + rule,
  text(font: mono, size: 0.9em)[#body],
)

// "PRECONDITION" tag — solid accent block, mono, on accent-ink (CSS .precondition).
#let precondition = box(
  fill: accent,
  inset: (x: 3.5pt, y: 1.5pt),
  outset: (y: 1pt),
  baseline: 0.5pt,
  text(
    font: mono, size: 7.5pt, fill: accent-ink,
    tracking: 0.12em, weight: 500,
  )[PRECONDITION],
)
#h(0pt)  // keep parser happy after raw block

// Cross-reference to an appendix — accent + hairline underline, matching
// CSS `.section__body a` (only body/appendix links are styled, not the TOC).
#let xref(target, body) = link(label(target), text(fill: accent, underline(offset: 2.5pt, stroke: 0.6pt, body)))

// ---------- Block constructors (mirror report-data.js block "kinds") -------
// Each returns a (kind: ..) dictionary; the renderer below dispatches on it.

#let p(body)                     = (kind: "p", body: body)
#let h3(body)                    = (kind: "h3", body: body)
#let ul(..items)                 = (kind: "ul", items: items.pos())
#let ol(..items)                 = (kind: "ol", items: items.pos())
#let kv(..pairs)                 = (kind: "kv", pairs: pairs.pos())
#let dl(..pairs)                 = (kind: "dl", pairs: pairs.pos())
#let rule-def(term, body)        = (kind: "definition", term: term, body: body)
#let quote-pull(body, cite: none) = (kind: "quote", body: body, cite: cite)
#let callout(title, body, warn: false) = (
  kind: "callout", title: title, body: body, warn: warn,
)
#let etable(columns: (), head: (), rows: ()) = (
  kind: "table", columns: columns, head: head, rows: rows,
)

// ---------- Section / appendix constructors --------------------------------
#let section(n, title, kicker: none, ..blocks) = (
  n: n, title: title, kicker: kicker, blocks: blocks.pos(),
)
#let appendix(id, label, title, ..blocks, meta: none) = (
  id: id, label: label, title: title, meta: meta, blocks: blocks.pos(),
)

// ═══════════════════════════════════════════════════════════════════════════
//  Internal renderers
// ═══════════════════════════════════════════════════════════════════════════

// uppercase sans label (cover meta / kickers / table heads / colophon)
#let _label(body, size: 8.25pt, color: ink-soft, track: 0.18em, weight: 500) = (
  text(font: sans, size: size, fill: color, tracking: track, weight: weight)[
    #upper(body)
  ]
)

// 01, 02, … zero-padded mono accent numeral for ordered lists
#let _ol-num(n) = {
  let s = if n < 10 { "0" + str(n) } else { str(n) }
  text(font: mono, size: 9pt, fill: accent, features: ("tnum",))[#s]
}

// numeric / accent table cell (CSS td.col-num)
#let nc(body) = text(font: mono, fill: accent, features: ("tnum",))[#body]

// ---- editorial hairline table --------------------------------------------
#let _render-table(b) = {
  let nrows = b.rows.len() + 1  // + header

  // full body width — breaks out of the narrower prose measure
  block(above: 1.5 * rem, below: 1.5 * rem, width: _body-w,
    // wrapper top + bottom ink hairline (CSS .table-wrap)
    stroke: (top: 0.75pt + ink, bottom: 0.75pt + ink),
    {
      set text(size: 9pt)
      set par(leading: 0.4em)
      table(
        columns: b.columns,
        inset: (left: 0pt, right: 1 * rem, top: 8.5pt, bottom: 8.5pt),
        align: (x, y) => if y == 0 { left + bottom } else { left + top },
        // header underline = ink; inter-row = rule; last row = none
        stroke: (x, y) => (
          bottom: if y == 0 { 0.75pt + ink }
                  else if y < nrows - 1 { 0.6pt + rule }
                  else { none },
        ),
        // header
        ..b.head.map(h => table.cell(
          text(font: sans, size: 7.9pt, fill: ink-soft,
            tracking: 0.18em, weight: 600)[#upper(h)],
        )),
        // body
        ..b.rows.flatten()
      )
    },
  )
}

// ---- block dispatch -------------------------------------------------------
#let _render-block(b) = {
  let k = b.kind

  if k == "p" {
    block(below: 1.1 * rem, b.body)

  } else if k == "h3" {
    block(above: 2 * rem, below: 0.5 * rem, sticky: true,
      text(font: sans, size: 1.05 * rem, weight: 600, tracking: -0.005em)[
        #b.body
      ],
    )

  } else if k == "ul" {
    block(above: 1.1 * rem, below: 1.1 * rem,
      list(
        marker: text(fill: accent)[—],
        indent: 0pt, body-indent: 8pt, spacing: 0.4 * rem,
        ..b.items.map(i => [#i]),
      ),
    )

  } else if k == "ol" {
    block(above: 1.1 * rem, below: 1.1 * rem,
      enum(
        numbering: _ol-num,
        indent: 0pt, body-indent: 13pt, spacing: 0.4 * rem,
        ..b.items.map(i => [#i]),
      ),
    )

  } else if k == "kv" {
    // CSS .kv — grid 9rem | 1fr, row gap .75rem, col gap 2rem. Like a table,
    // this ledger breaks out to the full width (not the narrow prose measure).
    // The small uppercase label is nudged down so its baseline lands on the
    // value's first line (CSS used dt{padding-top:.2rem}; the larger size gap
    // here needs ~3pt to truly align).
    block(above: 1.1 * rem, below: 1.1 * rem, width: _body-w,
      grid(
        columns: (9 * rem, 1fr),
        column-gutter: 2 * rem,
        row-gutter: 0.75 * rem,
        align: top,
        ..b.pairs.map(((dt, dd)) => (
          grid.cell(pad(top: 3pt, _label(dt, track: 0.18em))),
          grid.cell(dd),
        )).flatten()
      ),
    )

  } else if k == "dl" {
    // CSS .def — bold sans term (margin-top 1rem), serif body 0.2rem under it
    block(above: 1.1 * rem, below: 1.1 * rem,
      b.pairs.map(((dt, dd)) => block(above: 1 * rem, below: 0pt, {
        block(below: 0.2 * rem,
          text(font: sans, size: 0.95 * rem, weight: 600)[#dt])
        block(dd)
      })).join()
    )

  } else if k == "definition" {
    // CSS .rule — left accent bar, sans-bold term ending in a period
    block(above: 1.25 * rem, below: 1.25 * rem, width: 100%,
      stroke: (left: 2pt + accent),
      inset: (left: 1.5 * rem, top: 1.25 * rem, bottom: 1.25 * rem),
      {
        block(below: 0.3 * rem,
          text(font: sans, size: 1 * rem, weight: 600, tracking: -0.005em)[
            #b.term.
          ],
        )
        b.body
      },
    )

  } else if k == "quote" {
    // CSS blockquote.pull — left accent bar, large serif italic
    block(above: 2 * rem, below: 2 * rem, width: 100%,
      stroke: (left: 3pt + accent),
      inset: (left: 1.5 * rem, top: 1.5 * rem, bottom: 1.5 * rem),
      {
        set par(leading: 0.4em)
        text(font: serif, style: "italic", size: 1.3 * rem)[#b.body]
        if b.cite != none {
          block(above: 0.75 * rem, below: 0pt,
            _label[— #b.cite],
          )
        }
      },
    )

  } else if k == "callout" {
    // CSS .callout / .callout--warn — boxed, tinted
    block(above: 1.25 * rem, below: 1.25 * rem, width: 100%,
      fill: tint,
      stroke: 1pt + (if b.warn { accent } else { ink }),
      inset: (x: 1.25 * rem, y: 1 * rem),
      {
        block(below: 0.4 * rem,
          text(font: sans, size: 8.25pt, fill: accent,
            tracking: 0.22em, weight: 600)[#upper(b.title)],
        )
        b.body
      },
    )

  } else if k == "table" {
    _render-table(b)
  }
}

// ---- one § section --------------------------------------------------------
// Improvement over the source CSS: the original put the title at 6.5rem but
// the body at 4rem, so body text hung left of its own heading. Here the §
// number lives in a 4rem margin gutter and the kicker, title, rule AND body
// all share ONE left edge (5.5rem) — a single clean text column.

#let _render-section(s) = {
  block(breakable: true, above: 2.5 * rem, below: 2.5 * rem, {
    // head — § number in the gutter, kicker + title in the text column
    block(breakable: false, below: 2 * rem, sticky: true, {
      block(
        below: 1.25 * rem,
        grid(
          columns: (_gutter, 1fr),
          column-gutter: _head-gap,
          align: bottom,
          // bottom-aligned, then lifted by the title/number descender
          // difference so the § sits on the *title baseline* (CSS
          // `align-items: baseline`), not the line-box floor.
          grid.cell(pad(bottom: 3pt,
            text(font: mono, size: 10.5pt, tracking: 0.05em)[
              #text(fill: ink-soft)[§ ]#text(fill: accent)[#s.n]
            ])),
          grid.cell({
            if s.kicker != none {
              block(below: 0.7 * rem,
                text(font: sans, size: 8.25pt, fill: ink-soft,
                  tracking: 0.22em, weight: 500)[#upper(s.kicker)],
              )
            }
            text(font: sans, size: 2.05 * rem, weight: 500,
              tracking: -0.022em)[#s.title]
          }),
        ),
      )
      line(length: 100%, stroke: 0.75pt + ink)
    })
    // body — aligned with the title's left edge; prose held to body-col,
    // tables break out to the full width inside _render-table
    pad(left: _col-left, block(width: body-col,
      s.blocks.map(_render-block).join()))
  })
}

// ---- one appendix ---------------------------------------------------------
#let _render-appendix(a) = {
  pagebreak(weak: true)
  block(breakable: true, {
    // full-width hairline marks the back-matter zone …
    line(length: 100%, stroke: 0.75pt + ink)
    v(2.5 * rem)
    // … but label, title, meta and body share the body text spine (CSS hung
    // these flush-left; aligning them keeps one column for the whole report)
    pad(left: _col-left, block(width: body-col, {
      block(below: 2 * rem, {
        block(below: 0.4 * rem,
          text(font: sans, size: 8.25pt, fill: accent,
            tracking: 0.25em, weight: 500)[#upper(a.label)])
        text(font: sans, size: 1.95 * rem, weight: 500, tracking: -0.02em)[
          #a.title
        ]
        if a.meta != none {
          block(above: 0.4 * rem,
            text(font: serif, style: "italic", fill: ink-soft,
              size: 0.92 * rem)[#a.meta])
        }
      })
      a.blocks.map(_render-block).join()
    }))
  })
  // anchor for xref()
  [#metadata(a.id) #label(a.id)]
}

// ═══════════════════════════════════════════════════════════════════════════
//  report() — the document template
// ═══════════════════════════════════════════════════════════════════════════
#let report(
  meta: (:),
  priorities: (),
  tldr-label: "TL;DR for the founder",
  tldr-lede: [],
  tldr-closer: [],
  sections: (),
  appendices: (),
) = {
  set document(
    title: meta.at("title", default: "Report"),
    author: meta.at("author", default: ""),
  )

  set page(
    width: 8.5in, height: 11in,        // US Letter
    margin: (x: 16mm, y: 18mm),
    fill: paper,
  )

  // Base type — serif body, oldstyle figures, ragged right (CSS text-wrap)
  set text(
    font: serif, size: fs-body, fill: ink,
    number-type: "old-style", number-width: "proportional",
    features: ("kern", "liga"),
    hyphenate: false,
  )
  set par(leading: lh-body, justify: false, spacing: 1.1 * rem)
  set block(spacing: 1.1 * rem)

  // strong = weight 600 (CSS .section__body strong) ; em = italic
  show strong: set text(weight: 600)
  show emph: set text(style: "italic")
  // headings carry Geist stylistic sets
  show heading: set text(font: sans, features: ("ss01", "ss02"))
  // NB: no global `show link` — only xref() styles links (see CSS .toc a
  // = text-decoration:none; .section__body a = accent + underline).

  // ───────────────────────── COVER — title page ───────────────────────────
  // The masthead bleeds toward the trim with a tighter top margin than the
  // body (a standard title-page device); the colophon mirrors it at the
  // foot of the last page. Body pages keep the normal 18mm block.
  page(margin: (x: 16mm, top: 12mm, bottom: 18mm), {
    block(width: 100%,
      stroke: (top: 0.6pt + ink),     // bottom rule drawn at text width below
      inset: (top: 1.1 * rem, bottom: 0pt),
      {
        // masthead — small caps strip: author left, report meta right
        block(below: 2 * rem, {
          block(below: 0.55 * rem,
            grid(
              columns: (1fr, auto, auto, auto),
              column-gutter: 2 * rem,
              align: bottom,
              grid.cell(_label(size: 6.75pt, track: 0.16em)[
                #text(fill: ink, weight: 600)[#meta.author]]),
              grid.cell(_label(size: 6.75pt, track: 0.16em)[
                Report #text(fill: ink, weight: 500)[№ #meta.reportNumber]]),
              grid.cell(_label(size: 6.75pt, track: 0.16em)[#meta.dateline]),
              grid.cell(_label(size: 6.75pt, track: 0.16em)[#meta.readTime]),
            ),
          )
          line(length: 100%, stroke: 0.5pt + rule)
        })

        // kicker — hugs the title it labels
        block(below: 0.6 * rem,
          text(font: sans, size: 9pt, fill: accent,
            tracking: 0.25em, weight: 500)[#upper(meta.kicker)])

        // title — Geist 500, huge, tight ; ".me" in accent
        block(below: 1.9 * rem, {
          set par(leading: 0pt)
          text(font: sans, size: 60pt, weight: 500, tracking: -0.035em)[
            #meta.titleMain#text(fill: accent)[#meta.titleAccent]
          ]
        })

        // sub — serif italic tagline, one line (not the prose measure)
        block(below: 1.5 * rem,
          text(font: serif, style: "italic", size: 1.3 * rem,
            fill: ink-soft)[#meta.subtitle])

        // dek
        block(below: 1.75 * rem, block(width: body-col,
          text(size: 1.05 * rem)[#meta.dek]))

        // basis — sans, ink-soft, rule above
        block(width: body-col, {
          line(length: 100%, stroke: 0.5pt + rule)
          v(1 * rem, weak: true)
          text(font: sans, size: 8.5pt, fill: ink-soft)[#meta.basis]
        })

        // closing rule — matches the text column, not full bleed
        v(2.5 * rem)
        block(width: body-col, line(length: 100%, stroke: 0.6pt + ink))
      },
    )
  })

  // ───────────── FRONT MATTER — TL;DR + Contents share one page ────────────
  // The source HTML force-broke the page after the TL;DR *and* after the TOC,
  // leaving two ~half-empty pages. They are both front matter and the
  // TL;DR's bottom hairline is literally the TOC strip's top hairline in the
  // CSS — so they belong together on one well-filled page.
  // One atomic block: the TL;DR + Contents always sit together on a single
  // page and the TOC's closing rule can never strand on a sheet of its own.
  // Spacing is condensed so a full-length report (≈9 sections + appendices)
  // still fits this one page.
  block(breakable: false, {
    block(below: 1.3 * rem,
      text(font: sans, size: 8.25pt, fill: ink-soft,
        tracking: 0.25em, weight: 500)[#upper(tldr-label)])

    // lede — large serif, full measure ; strong → accent 700
    block(below: 1.6 * rem, {
      set par(leading: 0.3em)
      show strong: set text(fill: accent, weight: 700)
      text(font: serif, size: 1.6 * rem)[#tldr-lede]
    })

    // priorities — 3 columns, 2px ink top rule, 2-line title reserve so the
    // bodies align across columns (the subgrid fix the user asked for)
    block(below: 1.6 * rem,
      grid(
        columns: (1fr, 1fr, 1fr),
        column-gutter: 2 * rem,
        ..priorities.map(pr => grid.cell({
          line(length: 100%, stroke: 1.5pt + ink)
          v(1.25 * rem, weak: true)
          block(below: 0.5 * rem,
            text(font: mono, size: 9pt, fill: accent,
              tracking: 0.05em, features: ("tnum",))[#pr.n])
          // reserve two lines of title height
          block(below: 0.5 * rem, height: 2 * 1.05 * rem * 1.25,
            text(font: sans, size: 1.05 * rem, weight: 600,
              tracking: -0.01em)[
              #set par(leading: 0.25em); #pr.title
            ])
          block(
            text(font: serif, size: 0.95 * rem, fill: ink-soft)[
              #set par(leading: 0.42em); #pr.body
            ])
        }))
      ))

    block(below: 1.6 * rem, width: 42 * rem,
      text(font: serif, style: "italic", fill: ink-soft,
        size: 0.95 * rem)[#tldr-closer])

    // Contents strip — top rule is the TL;DR's closing rule (CSS shares it)
    line(length: 100%, stroke: 0.75pt + ink)
    v(1.1 * rem, weak: true)
    block(below: 0.8 * rem,
      text(font: sans, size: 8.25pt, fill: ink-soft,
        tracking: 0.25em, weight: 500)[CONTENTS])

    let entry(n, title, target) = link(target, grid(
      columns: (2.5 * rem, 1fr),
      column-gutter: 0.5 * rem,
      grid.cell(text(font: mono, size: 8.25pt, fill: accent,
        features: ("tnum",))[#n]),
      grid.cell(text(font: sans, size: 0.92 * rem, fill: ink)[#title]),
    ))

    let toc-items = (
      sections.map(s => entry(s.n, s.title, label("s-" + s.n)))
        + appendices.map(a => entry(
            a.label.replace("Appendix ", ""), a.title, label(a.id)))
    )
    // Column-major fill: first half runs DOWN column 1, the rest DOWN
    // column 2 (01 07 / 02 08 / 03 09 / 04 A / 05 B), not 01 02 / 03 04.
    let half = calc.ceil(toc-items.len() / 2)
    let toc-col(items) = grid(columns: (1fr,), row-gutter: 0.42 * rem, ..items)
    grid(
      columns: (1fr, 1fr),
      column-gutter: 2 * rem,
      align: top,
      toc-col(toc-items.slice(0, half)),
      toc-col(toc-items.slice(half)),
    )
    v(1.1 * rem, weak: true)
    line(length: 100%, stroke: 0.75pt + ink)
  })

  pagebreak(weak: true)

  // ─────────────────────────── BODY ───────────────────────────────────────
  for s in sections {
    [#metadata(s.n) #label("s-" + s.n)]
    _render-section(s)
  }

  // ─────────────────────────── APPENDICES ─────────────────────────────────
  for a in appendices { _render-appendix(a) }

  // ────────────────── COLOPHON — foot of the last page ────────────────────
  // No dedicated sheet (paper economy). `place(bottom, dy:)` pins it to the
  // foot of whatever page the appendices end on and nudges it into the
  // bottom margin so it still sits tight to the trim — the bookend look
  // without its own near-empty page. (Out of flow: it does not add a page.)
  place(bottom, dy: 8mm, block(width: 100%, breakable: false,
    stroke: (top: 1pt + ink),
    inset: (top: 1.1 * rem),
    grid(
      columns: (auto, 1fr, auto),
      column-gutter: 2 * rem,
      align: (left + horizon, center + horizon, right + horizon),
      grid.cell(_label(size: 6.75pt, track: 0.2em)[#meta.colophonLeft]),
      grid.cell(_label(size: 6.75pt, track: 0.2em)[#meta.colophonMid]),
      grid.cell(_label(size: 6.75pt, track: 0.2em)[
        #text(fill: ink, weight: 600)[#meta.author] · #meta.year]),
    ),
  ))
}
