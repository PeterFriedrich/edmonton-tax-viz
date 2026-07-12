# Vendored front-end libraries

These are the third-party JS/CSS libraries the map runs on, committed to the repo
instead of loaded from a CDN at runtime (`web/index.html`). The whole page —
including every displayed dollar figure — executes through these libraries, so a
compromised CDN or a hijacked package release could silently alter the civic
numbers the site presents. Vendoring removes that runtime supply-chain surface
and makes the Pages site fully self-contained (security-audit.md **S1**).

| File | Package | Version | Upstream |
|---|---|---|---|
| `maplibre-gl-4.7.1.js`  | maplibre-gl | 4.7.1  | `https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js` |
| `maplibre-gl-4.7.1.css` | maplibre-gl | 4.7.1  | `https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.css` |
| `deck.gl-9.0.38.min.js` | deck.gl     | 9.0.38 | `https://unpkg.com/deck.gl@9.0.38/dist.min.js` |

## Provenance (SHA-256)

```
576b085fdd9487a65a19215328c1e086c07ce5bf6da09b666b3806d3d008dae9  maplibre-gl-4.7.1.css
be9633c4d870e26fb37f1cfe5c5a77181667114003ea16207ac7850d8da8add1  maplibre-gl-4.7.1.js
e0ec599ee202671085dfb418a11ca08f59bbc9c0168ecc47d84bdd04f22c7cf4  deck.gl-9.0.38.min.js
```

Downloaded 2026-07-12 from unpkg.com and **cross-verified byte-for-byte against
jsdelivr** (`cdn.jsdelivr.net/npm/<pkg>@<ver>/...`) — two independent CDNs served
identical bytes, confirming the genuine published artifacts.

## Updating a version

1. Download the new pinned version from unpkg into this directory (keep the
   `name-version.ext` filename convention).
2. Cross-verify the SHA-256 against a second CDN (jsdelivr), as above.
3. Update the filename references in `web/index.html`, the table + hashes here,
   and the pinned versions in `docs/security-audit.md` S1.
4. Re-run `node tools/profiling/verify-*.js` against a local server to confirm
   the map still renders.

Never point `web/index.html` back at a CDN `<script src>` without SRI — that
re-opens S1.
