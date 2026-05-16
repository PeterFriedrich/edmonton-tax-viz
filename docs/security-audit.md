# Security Audit: Edmonton Revenue Per Acre

Post-implementation review checklist for a Python data pipeline producing a static map from public data. Scope is appropriate for the threat model: a local analysis tool with no web exposure, no auth, and no private data.

---

## Threat Model

| Asset | Risk | Likelihood |
|-------|------|------------|
| Raw assessment CSV | Contains property owner info if not stripped | Medium |
| Output map | Aggregated by neighbourhood — low sensitivity | Low |
| Pipeline code | Runs locally, no network exposure | Low |
| Dependencies | Supply chain risk via PyPI | Medium |

This is not a web app. There is no auth surface, no database, and no user-supplied input at runtime. The main risks are data handling (what ends up in processed files or logs) and dependency integrity.

---

## Checklist

### Data Handling

- [ ] **No PII in processed outputs** — confirm `data/processed/` files contain only aggregated neighbourhood-level data, not individual property records or owner names
- [ ] **No PII logged to stdout** — check that flagging routines (unmatched names, tax-exempt properties) print counts and neighbourhood names only, not individual assessment records
- [ ] **`data/raw/` is in `.gitignore`** — raw assessment CSV must not be committed; it may contain owner names and addresses
- [ ] **`output/` is in `.gitignore`** — output map should not be committed unless intentional
- [ ] **`data/processed/` is in `.gitignore`** — intermediate files should not be committed unless intentional

### Dependency Integrity

- [ ] **`requirements.txt` pins exact versions** — e.g. `geopandas==0.14.3`, not `geopandas>=0.14`
- [ ] **Dependencies are from well-known maintainers** — pandas, geopandas, matplotlib, pyproj, shapely are all established; flag any unfamiliar additions
- [ ] **No `pip install` in code** — dependencies are declared in `requirements.txt` only, not called at runtime
- [ ] **Consider `pip-audit`** — run `pip-audit -r requirements.txt` to check for known CVEs in pinned versions

### File Path Handling

- [ ] **No path traversal risk** — input paths are constants in `main.py`, not derived from user input; confirm no `os.path.join` calls build paths from external strings
- [ ] **No shell execution** — confirm no `subprocess`, `os.system`, or `eval` calls anywhere in `src/`
- [ ] **Output directory is created safely** — `output/` creation uses `pathlib.Path.mkdir(exist_ok=True)`, not a shell command

### Code Quality (Security-Relevant)

- [ ] **No `pickle` usage** — if intermediate files are cached, confirm they use CSV/Parquet/GeoJSON, not pickle (which can execute arbitrary code on load)
- [ ] **No `eval` or `exec`** — grep the codebase: `grep -r "eval\|exec\|__import__" src/`
- [ ] **Exception handling doesn't swallow errors silently** — bare `except: pass` blocks can hide data corruption

---

## Audit Prompts for AI-Assisted Review

Use these prompts with Claude to get a focused security review after implementation is complete.

### Prompt 1: Data exposure check
```
Read all files in src/ and tests/. Identify any place where individual property 
records, owner names, or addresses could appear in stdout, log output, or 
processed files. The pipeline should only surface neighbourhood-level aggregates 
in its outputs — flag any deviation.
```

### Prompt 2: Dependency review
```
Read requirements.txt. For each dependency: confirm it is a well-known package 
with active maintenance, flag any unpinned versions, and note if any package has 
known CVEs. Suggest running pip-audit if not already in the workflow.
```

### Prompt 3: File path and shell safety
```
Read all files in src/ and main.py. Check for: path traversal risks (paths 
constructed from external input), any subprocess or os.system calls, any eval 
or exec calls, and any use of pickle for intermediate file storage. Report 
findings with file and line number.
```

### Prompt 4: Full pipeline audit
```
Read ARCHITECTURE.md, then read all files in src/. For each module, verify that 
its implementation matches its documented contract (inputs, outputs, 
responsibilities, "does not" boundaries). Flag any module that does something 
outside its documented scope, particularly any that touch the filesystem, 
network, or shell unexpectedly.
```

---

## Notes

- This checklist is scoped to Phase 1 (local static pipeline). A web-facing version would require a significantly expanded audit covering OWASP Top 10, content security policy, and rate limiting.
- Property assessment data from Edmonton Open Data is public, but the raw CSV may include fields not needed for this analysis (owner name, mailing address). Strip these columns in `load_assessment.py` and confirm they are absent from all downstream outputs.
