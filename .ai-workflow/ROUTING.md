# Workflow routing contract

## Priority

Resolve conflicts in this order:

1. Runtime constraints and explicit user authorization.
2. Root `AGENTS.md` permanent rules.
3. Current project facts, approved spec, plan, code, and fresh evidence.
4. One project-lifecycle Skill as the primary route.
5. Superpowers methods needed inside that route.
6. Templates, examples, and references.

Lower layers never authorize commits, external writes, destructive operations, deployments, or spending.

## Primary routes

| Work | Primary route |
| --- | --- |
| Conversation, knowledge question, read-only explanation or status lookup | Answer directly; inspect relevant facts if needed; no automatic lifecycle or method Skill |
| New project or first repository onboarding | `project-kickoff` |
| Feature, refactor, or approved-plan execution | `project-development` |
| Ordinary non-production bug or test failure | `project-development`; focused evidence gathering first; use `systematic-debugging` only if diagnosis remains unclear, recurs, spans components or is high risk |
| Fix with evidence-confirmed root cause and clear authorized boundaries | `project-development`; low-risk local fixes use inline regression checks; nontrivial/high-risk fixes may select `test-driven-development` |
| Dependency, runtime, CI, or toolchain change | `project-maintenance` |
| Security review, trust boundary, auth, or secrets | `project-security` |
| Acceptance, review, or evaluation | `project-verification` |
| Documentation truth or project documentation update | `maintaining-project-docs` |
| Release readiness, migration, rollback, or authorized launch | `project-release` |
| Production impact or active incident | `project-incident-response`, then authorized diagnosis/repair |
| Existing-task session recovery, task switch, pause, or handoff | `project-continuity` |
| Cluttered project root, file classification, or requested directory restructuring | `project-organization` |

The lifecycle route owns scope and project truth. Choose by change and risk, not project size: a clear authorized low-risk change following an existing pattern proceeds directly through implementation and verification; unresolved design choices need brainstorming; multi-step dependencies, migration or cross-module delivery need one plan. Reuse approved decisions instead of seeking approval for each step. Feature/fix regression tests, unknown-failure diagnosis and fresh completion evidence remain required.

For actions or explicitly requested specialist work (review, diagnosis, acceptance), load one applicable lifecycle Skill. Clear low-risk local work uses that Skill alone, including applicable regression checks and fresh evidence; it automatically loads no Superpowers methods, including TDD, completion verification, review, or discovery wrappers. Focused checks precede fixes even on the light path. If diagnosis remains unclear, failures recur, or complexity/risk is discovered, promote only the affected work and load the relevant method for its current stage. A task's file count or a request to hurry does not establish low risk.

Substantial work selects individual methods when their concrete triggers apply; it does not load the whole library. An explicit request to apply a named method also selects it. Merely discussing a Skill, beginning a conversation, or reading files does not. `using-superpowers` is optional help for method selection/integration troubleshooting, never a bootstrap. Nested `superpowers:<name>` references resolve to the project-local sibling Skill, not a global plugin, and remain conditional on stage relevance. Host-level requirements still apply; existing global/plugin metadata is independent and an already open session may retain its old catalog.

Simple work needs no execution wrapper, parallel agent, separate formal acceptance route or iteration log. Formal acceptance, important independent review and cross-system evaluation use project-verification; ordinary verification stays within the current task. Never create a second spec or plan.

## Recovery and handoff

When existing work needs recovery, follow recovery → one lifecycle route → applicable methods → implementation/verification → necessary facts. A fresh conversation with a clear new request starts at its matching lifecycle route; session freshness alone never selects `project-continuity`. `project-development` delegates actual recovery to `project-continuity`; it does not duplicate the task-state protocol. Prefer the user's explicit task ID, then unique worktree/branch matches. Never choose by modification time. Rebuild stale state from code and fresh evidence before continuing.

Ordinary non-production Bug work keeps `project-development` as scope owner. Investigate before fixing; a cause established by focused inspection may support a low-risk inline repair with regression checks. Use systematic-debugging when uncertainty persists, investigation is nontrivial or risk is high; reuse a root cause already established by evidence. A symptom or proposed fix alone is not root-cause proof. A user's existing repair request supplies repair authorization within its scope; do not ask again merely because diagnosis finished. Diagnosis-only requests do not authorize a fix, and material scope/contract/data changes require confirmation. For production incidents, stabilize first. Dependency maintenance enters security only for an actual relevant trust boundary or explicit security review.

Parallel workers own disjoint files and individual task records. A single integrator updates the shared index and rechecks results; an unstable shared contract requires serial work. No lifecycle or method route creates permission for external operations.

Human entry: root `README.md` or `README.en.md`. Facts and archive rules: `docs/README.md`. The human entry states the tested scope and compatibility limits. Development-only test fixtures, evaluation harnesses and build records are intentionally not part of this copyable project foundation.
