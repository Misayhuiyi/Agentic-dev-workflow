# Superpowers patch record

## 2.0.1 — Conditional project method activation

The 14 `.agents/skills/<name>/SKILL.md` entrypoints are locally patched from Superpowers 6.3.0, commit `b36e0829c6d0140e93cfef2ca599b1b07d4a7797`. Exact paths, original Git blob IDs, original SHA-256 and distributed SHA-256 are recorded in `../../SOURCES.lock.json` under `sources.superpowers.local_patches`. `FILES.sha256` verifies the distributed bytes; it is not a claim that patched entrypoints equal upstream.

Reason: upstream startup/any-task descriptions selected methods for ordinary conversation and clear low-risk local work before the project lifecycle route could decide the appropriate depth. The old small-feature behavior test loaded TDD and completion-verification methods even though the scope was already clear.

Changes:
- All 14 descriptions identify concrete task conditions; ordinary conversation and routine work no longer match broad startup/any-task triggers.
- The 13 execution methods have a leading project activation boundary. Subsequent unconditional wording applies only within the selected method. Nested methods are selected for the current stage and `superpowers:<name>` references resolve to the project-local sibling source.
- `using-superpowers/SKILL.md` is replaced with an optional selection/integration guide. No startup, before-any-response, 1% relevance, or obligatory platform-reference bootstrap remains.
- TDD, debugging and completion-verification introductory triggers are scoped to the selected nontrivial/high-risk task. Their core technical procedures remain present.

Coverage: conversation/Skill-explanation routing, an actual low-risk feature with regression tests, known-fix and nontrivial/risk routing, generated-adapter consistency, and original/distributed hash checks. Test artifacts belong to the development workspace, not the copyable template; the README reports the verified scope and its limitations.

## Distribution boundaries

- Of the 46 included upstream-derived files, the 14 entrypoints above are patched; 32 supporting resources retain exact upstream bytes.
- Five unreferenced development-only files under `skills/systematic-debugging/` are omitted: `CREATION-LOG.md`, `test-academic.md`, and `test-pressure-1.md` through `test-pressure-3.md`.
- The 14 `agents/openai.yaml` files are unchanged Codex distribution packaging metadata, not GitHub upstream files.
- Lifecycle routing and project authorization live in `AGENTS.md` and `.ai-workflow/superpowers-compat.md`. Installed global plugins are separate sources and are not patched by this template.

Future upgrades must compare against the original commit, reapply/review these local patches, preserve the upstream identity, and rerun affected behavior and integrity checks.
