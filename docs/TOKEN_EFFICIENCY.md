# Token Efficiency

Practices for keeping context/token usage low as the codebase grows. This is a
living doc — add to it whenever a new "don't read that raw" or "that directory is
growing" lesson comes up.

## Baseline (measured 2026-07-01)

Rough tokens ≈ bytes ÷ 4.

| Category | Size | ~tokens | Notes |
|---|---|---|---|
| `src/` (7 modules) | 32 KB | ~8k | largest: `join_and_calculate.py` (255 ln), `load_zoning.py` (244 ln) |
| `tests/` | 31 KB | ~8k | mirrors `src/` |
| `docs/` | 78 KB | ~19k | largest: `ARCHITECTURE.md` (315 ln) |
| `web/index.html` | 15 KB | ~4k | single hand-edited file (365 ln) |
| root docs (TODO/DATA/README/…) | ~21 KB | ~5k | |
| `session-summary/` | 125 KB | ~31k | ⅓ of the corpus — the fastest grower |
| **whole tracked text corpus** | 376 KB | **~94k if you read *everything*** | nobody should |

**Verdict:** code + docs are nowhere near a problem. Reading every source, test,
doc, and the web file at once is ~44k tokens; a typical task touches a handful and
costs single-digit thousands. No file is large enough to warrant splitting (biggest
source module is 255 lines). The only unbounded grower is `session-summary/`.

Re-measure anytime with:

```bash
git ls-files | grep -vE '\.(geojson|png|csv)$' | xargs wc -l | sort -n | tail -30
```

## Rules

1. **Never `Read` raw data files.** `data/raw/zoning.geojson` is 9.2 MB ≈ **2.3M
   tokens** — one raw read blows the entire context window. `neighbourhoods.geojson`
   (2.8 MB) and the exported `web/data/*.geojson` (535 KB ≈ ~130k tokens) are the
   same hazard. Always inspect via a small python/geopandas snippet that prints a
   *summary* (shape, columns, `head`, value counts, a few rows) — never the raw
   bytes. The same goes for the assessment CSV.

2. **Read only the latest session summary.** Per `CLAUDE.md`, start work from the
   newest handoff. Do NOT bulk-read or glob-grep across the whole directory ("when
   did we decide X" over `session-summary/*.md` pulls tens of thousands of tokens).
   Keep the **3 most recent** handoffs at the top level; older ones live in
   `session-summary/archive/` so a `session-summary/*.md` glob doesn't reach them.
   Move the oldest out when a 4th accumulates.

3. **Prefer targeted reads over whole-file reads for anything large.** Use `Read`
   with `offset`/`limit`, or `grep`/`Grep` to locate the lines first, when a file is
   more than a couple hundred lines. Read the section you need, not the whole file.

4. **Keep modules small and single-purpose.** The existing `src/` boundary (one
   processing step per file, ≤~250 lines) is what keeps per-task reads cheap. If a
   module crosses ~400 lines, that's the signal to split — not a hard rule, but the
   point where a reader pays for lines they don't need.

## Files to watch

- `session-summary/` — growing every `/handoff`; archive policy above keeps it bounded.
- `docs/` — largest doc category; fine today, but if any single doc passes ~400 lines
  consider whether it should be sectioned or split.
- `web/index.html` (~3,600 lines, markup + JS) + `web/styles.css` (~400 lines). The
  CSS was extracted 2026-07-29; the remaining JS block is ~3,300 lines.
  **⚠️ Splitting it further is NOT a token lever — this was measured, and the
  intuition here was wrong.** The whole file is ~57k tokens, but it is read in
  grep-located windows of 100–400 lines (~2–6k), not end-to-end, so a split saves
  almost nothing. Worse, the common change touches CSS + DOM node + JS handler
  *together* (see almost any `DECISIONS.md` row), which post-split is three **file**
  opens instead of three offsets into one file — marginally *more* expensive.
  Split it for navigability, grep precision and blast radius if you like; do not
  expect context savings. (`DECISIONS.md` 2026-07-29.)

## Going forward

When you learn a new efficiency lesson (a file that shouldn't be read raw, a
directory that's ballooning, a read pattern that wasted tokens), record it here.
