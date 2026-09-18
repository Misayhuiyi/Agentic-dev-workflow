# Superpowers patch record

- The 46 included upstream files have no content patches and retain their exact Git blob bytes.
- The lean distribution omits five unreferenced development-only files under `skills/systematic-debugging/`: `CREATION-LOG.md`, `test-academic.md`, and `test-pressure-1.md` through `test-pressure-3.md`. Exact omitted paths are recorded in `SOURCES.lock.json`. All 14 Skill entry points and their required supporting resources remain included.
- The 14 `agents/openai.yaml` files are Codex distribution packaging metadata, not GitHub upstream files.
- Project-specific constraints live outside the vendored payload in `.ai-workflow/superpowers-compat.md`.

Any future patch must identify the original path, reason, concise diff summary, and tests that cover the changed behavior.
