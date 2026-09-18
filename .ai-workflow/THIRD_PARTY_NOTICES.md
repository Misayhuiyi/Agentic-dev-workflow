# Third-party notices

## Superpowers

The 46 files identified as upstream content in `third_party/superpowers/FILES.sha256` are redistributed from `obra/superpowers` version 6.3.0, commit `b36e0829c6d0140e93cfef2ca599b1b07d4a7797`, under the MIT license preserved in `third_party/superpowers/LICENSE`. Five unreferenced development-only files are omitted as recorded in `SOURCES.lock.json` and `third_party/superpowers/PATCHES.md`.

## Codex packaging metadata

Fourteen `agents/openai.yaml` files are packaging metadata obtained from the `openai-curated-remote/superpowers` 6.3.0 distribution on 2026-09-17. Their source is that distribution, and their applicable license terms come from that source rather than from this workflow template. They are packaging payload, not GitHub upstream files and not files claimed to exist in the locked GitHub commit; their reconstruction identity is the distribution ID/version plus the hashes in `FILES.sha256`.

## Research-only sources

[`Misayhuiyi/Rules`](https://github.com/Misayhuiyi/Rules) commit `cf54b1309db3eb7651125d9e66de76417296ee31` was reviewed as research only. No upstream files or text are redistributed; it declares no license in the locked source record. The template independently expresses general principles concerning evidence and uncertainty, understanding/reuse, simplicity and root causes, scoped edits, environment awareness, and verification. They inform the compact root rules rather than a second ruleset. Project-specific premises such as having no legacy users are not adopted; compatibility depends on actual callers and data, and platform/style conventions follow the target project.

The Agent Skills specification and official tool documentation were used only as interoperability references. External documentation does not grant project authority.
