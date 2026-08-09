# Remote VM sessions (Claude Code on the web) — read FIRST in one of these

How to be productive in a cloud/remote Claude Code session on this repo.
Written after Session 16 (2026-07-06), the first such session, which burned
time rediscovering all of this. A remote session is recognizable by: repo
cloned at `/home/user/edmonton-tax-viz` (not `/home/peter/data-projects/…`),
no conda, empty `data/raw/`, and a session-specific branch name like
`claude/<something>`.

## The rules that differ from local sessions

- **Push proactively at every checkpoint** — see CLAUDE.md "Session
  Management". The container is ephemeral; unpushed work is lost when it
  idles out. Never wait for Peter's "push it".
- **Work on the session's designated branch** (the harness names it).
  The summaries-live-on-master convention does NOT apply — the handoff
  commit goes on the branch too; the merge carries it over.
- **No PR unless Peter asks.**

## Network policy — the big constraint

The VM's outbound HTTPS goes through an allowlist proxy. As of 2026-07-06
the policy ALLOWS registry.npmjs.org, pypi.org, GitHub — and **BLOCKS
data.edmonton.ca** (and dev.socrata.com, api.us.socrata.com, unpkg.com,
and most of the web). That means: **no raw data downloads, no Socrata
probing, no CDN scripts** unless the policy is changed.

- Diagnose: `curl -sS "$HTTPS_PROXY/__agentproxy/status"` — a
  `connect_rejected` / "gateway answered 403 to CONNECT" entry for a host
  means policy denial, not a transient failure. Don't retry; don't
  disable TLS or unset HTTPS_PROXY.
- **The fix is Peter's, not the session's**: claude.ai/code → this
  environment's settings → network access → add `data.edmonton.ca`
  (+ `unpkg.com` for headless browser verification) to the allowed
  domains, or switch to unrestricted. Applies to NEW sessions.
  Docs: https://code.claude.com/docs/en/claude-code-on-the-web
- WebFetch obeys the same proxy (also blocked). WebSearch works
  (Anthropic-side) but can't fetch blocked pages, only search.
- Until the policy is fixed: build with synthetic tests (the project's
  standard pattern anyway), guard frontends on missing columns (the
  established pattern — see the stormwater/fire rows in
  `web/index.html`), and let the weekly CI refresh (GitHub runners, open
  network) populate real data after merge. Session 16 shipped the whole
  fire lens this way.

## Environment setup (fresh container)

```bash
pip install -r requirements-ci.txt   # geopandas etc.; there is NO conda here
git config core.hooksPath .githooks  # ⚠️ HOOKS ARE NOT CLONED — see below
python3 -m pytest tests/ -q          # from repo root; all-synthetic, no data needed
# data/raw/ is EMPTY. scripts/download_data.py only works if the network
# policy allows data.edmonton.ca (see above).
```

⚠️ **`core.hooksPath` matters MOST here.** `.githooks/pre-push` blocks a push to
a branch whose PR is already merged — the failure that has stranded work 9×. Git
does not clone hooks, so in a fresh container it is **OFF until you set it**, and
this is exactly the environment where a stranded commit is unrecoverable (the box
gets reclaimed). The hook **fails open** — no `gh`, no auth, no network → the
push proceeds — so it can never be the reason work goes unsaved. It is a
backstop, not a substitute for `git merge-base --is-ancestor <sha> origin/master`
after any merge.

## Headless browser verification (verify-*.js / shot-*.js)

Two blockers, two workarounds (scratchpad-only — commit neither):

1. **Playwright browser build mismatch.** `tools/profiling`'s Playwright
   wants a newer browser build than `/opt/pw-browsers` ships. Do NOT run
   `playwright install` (blocked/pointless). Symlink instead — adjust the
   build numbers to what the error message asks for vs what `ls
   /opt/pw-browsers` has:
   ```bash
   ln -s /opt/pw-browsers/chromium_headless_shell-<HAVE> /opt/pw-browsers/chromium_headless_shell-<WANT>
   ln -s /opt/pw-browsers/chromium_headless_shell-<HAVE>/chrome-linux \
         /opt/pw-browsers/chromium_headless_shell-<HAVE>/chrome-headless-shell-linux64
   ln -s /opt/pw-browsers/chromium_headless_shell-<HAVE>/chrome-linux/headless_shell \
         /opt/pw-browsers/chromium_headless_shell-<HAVE>/chrome-linux/chrome-headless-shell
   ```
2. **The page's unpkg CDN scripts are blocked.** Fetch the same dists via
   npm (allowed) and point a COPY of web/ at them:
   ```bash
   cd $SCRATCHPAD && mkdir cdn && cd cdn
   npm pack maplibre-gl@4.7.1 deck.gl@9.0.38 && tar xzf maplibre-gl-*.tgz && mv package maplibre && tar xzf deck.gl-*.tgz && mv package deckgl
   cp -r /home/user/edmonton-tax-viz/web $SCRATCHPAD/mockweb
   mkdir $SCRATCHPAD/mockweb/vendor
   cp maplibre/dist/maplibre-gl.{js,css} deckgl/dist.min.js $SCRATCHPAD/mockweb/vendor/
   # then sed the three unpkg URLs in mockweb/index.html to ./vendor/…
   # (versions above match web/index.html's script tags — check them first)
   cd $SCRATCHPAD/mockweb && python3 -m http.server 8799
   ```
   For features whose data column doesn't exist yet, inject synthetic
   values into the mockweb geojson copy (Session 16 pattern) — label any
   screenshots SYNTHETIC when showing Peter.

## What still needs a network-enabled run

Anything that touches real data: `scripts/download_data.py`, `main.py`
regeneration, real-data validation/skew checks, live-site verification of
new data columns. Options: Peter's machine, the CI refresh workflow
(`gh workflow run "Refresh map data"` after merge), or a remote session
after the policy fix.
