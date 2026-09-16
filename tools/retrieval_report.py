#!/usr/bin/env python3
"""Per-doc read-frequency table from the PostToolUse retrieval log.

The log is written by the `Read|Grep|Glob` hook in `.claude/settings.json`
(added 2026-09-16) — one JSON line per tool call, with the path, the session id
and a timestamp. This turns it into the table the doc-apparatus audit needs
(`docs/FABLE_AUDIT_doc_apparatus.md`, rec #1): which docs a session actually
opens, how many distinct sessions opened each, and which were never opened.

⚠️ A doc with zero reads is a PRUNE CANDIDATE, not a verdict. Three things make a
zero honest-but-misleading: a doc read in a session that predates the hook, a doc
whose content reached the model through CLAUDE.md, and — the big one — **a doc
read through Bash.** The hook matches the `Read`, `Grep` and `Glob` TOOLS, so
`bash grep`, `sed`, `cat`, `head` and `python` reads are invisible to it.
Measured 2026-09-16: the session that audited this instrument logged **4 reads
while consulting ~14 docs**; `DECISIONS.md` and `AUDIT_LEDGER.md` both read via
Bash, both scored zero. The undercount is not uniform — it falls hardest on the
big files a session greps rather than opens, which are the ones a prune would
target. The never-read list is where to look, not what to conclude.

⚠️ Read the DATE RANGE before the counts. Under ~2 weeks of normal sessions the
table settles nothing, and the report says so at the top rather than leaving the
reader to notice.

Usage::

    python tools/retrieval_report.py                    # docs/ + *.md at root
    python tools/retrieval_report.py --all              # every path logged
    python tools/retrieval_report.py --log ~/other.jsonl
"""
import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_LOG = Path.home() / ".claude" / "retrieval-log.jsonl"
# Below this the table cannot settle the question it was built for; the report
# leads with the warning rather than printing counts that look like evidence.
MIN_DAYS = 14


def load(log_path: Path) -> list[dict]:
    if not log_path.exists():
        raise SystemExit(f"No retrieval log at {log_path} — is the hook installed?")
    rows = []
    for line in log_path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue  # a truncated final line mid-write is expected, not a fault
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", type=Path, default=DEFAULT_LOG)
    ap.add_argument("--all", action="store_true", help="include non-doc paths")
    ap.add_argument("--project", default=str(ROOT), help="filter by cwd prefix")
    args = ap.parse_args()

    rows = [r for r in load(args.log) if str(r.get("cwd", "")).startswith(args.project)]
    if not rows:
        raise SystemExit("Log has no entries for this project yet.")

    stamps = sorted(r["t"] for r in rows if r.get("t"))
    first, last = stamps[0], stamps[-1]
    days = (datetime.fromisoformat(last.replace("Z", "+00:00"))
            - datetime.fromisoformat(first.replace("Z", "+00:00"))).days
    sessions = {r.get("sid") for r in rows}

    print(f"Retrieval log: {len(rows)} calls, {len(sessions)} sessions, "
          f"{first[:10]} → {last[:10]} ({days}d)")
    if days < MIN_DAYS:
        print(f"⚠️  ONLY {days} DAYS — under {MIN_DAYS} this table settles nothing. "
              f"Report it as MEASUREMENT-PENDING.")
    print()

    reads = defaultdict(set)   # path -> session ids
    counts = defaultdict(int)
    for r in rows:
        p = r.get("path")
        if not p:
            continue
        rel = p[len(args.project):].lstrip("/") if p.startswith(args.project) else p
        if not args.all and not (rel.startswith("docs/") or
                                 (rel.endswith(".md") and "/" not in rel)):
            continue
        reads[rel].add(r.get("sid"))
        counts[rel] += 1

    print(f"{'reads':>6} {'sessions':>9}  path")
    for path in sorted(counts, key=lambda p: (-len(reads[p]), -counts[p], p)):
        print(f"{counts[path]:>6} {len(reads[path]):>9}  {path}")

    if not args.all:
        tracked = {str(p.relative_to(ROOT)) for p in ROOT.glob("docs/*.md")}
        tracked |= {str(p.relative_to(ROOT)) for p in ROOT.glob("*.md")}
        never = sorted(tracked - set(counts))
        # The warning lives here, not only in the docstring: this list is the one
        # a prune would act on, and a caveat the actor does not see is the defect
        # this project keeps re-learning (`_classify`, ~70 days into a log).
        print(f"\n⚠️  A ZERO BELOW MAY MEAN 'READ THROUGH BASH', NOT 'NEVER READ'.")
        print(f"    The hook sees the Read/Grep/Glob TOOLS only — `bash grep`, `sed`,")
        print(f"    `cat` and `python` reads are invisible. The audit session itself")
        print(f"    logged 4 reads while consulting ~14 docs (2026-09-16). Confirm a")
        print(f"    zero against transcripts before treating it as evidence.")
        print(f"\nNEVER OPENED in this window — {len(never)} of {len(tracked)}:")
        for path in never:
            print(f"       .         {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
