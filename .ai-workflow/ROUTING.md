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

First assess five dimensions: requirement clarity; interaction uncertainty; technical/data/integration uncertainty; authority, external writes, money, privacy and production exposure; blast radius and recovery cost. These are reasoning inputs, not five compulsory documents. A small diff is not evidence of low risk.

| Change path | Entry and minimum evidence | Advance / stop |
| --- | --- | --- |
| A: knowledge, explanation, progress | Direct answer or relevant read-only inspection; no lifecycle, repository writes or unrelated records | Return answer; a new action needs its own scope |
| B: clear low-risk local change | Applicable project Skill; scope/acceptance → impact check → small edit → regression → result | Fresh relevant evidence; no compulsory PRD, PoC, prototype or Superpowers |
| C: unclear interaction/business flow | Development, or kickoff for undefined project scope; clarify users, sequence, rules and acceptance; preview only if it resolves uncertainty | Review key states, including waiting/failure/cancel/reject/takeover; reuse existing components before separate HTML |
| D: backend/API/data/performance | Development/maintenance as appropriate; contracts, samples, tests, logs, comparative performance, consistency/recovery evidence | Sync changed behavior and consumers; UI is not required; uncertain integration adds E |
| E: uncertain core AI/algorithm/data/tool capability | Current route proposes the riskiest hypothesis; authorized bounded experiment uses verification | Approved representative samples, thresholds, budget, actual results; continue/adjust/reduce/stop decision, not a platform built on an untested assumption |
| F: high-risk change, even one line | Current action route owns scope; consult security/release only for applicable boundary | Establish business rules, precise authority, audit, idempotency and recovery/compensation; isolate validation before controlled release |
| G: active production incident | Incident response: contain → authorized recovery → verify → record → retrospective | Do not delay essential authorized response for full documentation; urgency grants no extra permission |

Paths may combine: C + E allows interaction exploration and technical experiments in parallel when independent; neither substitutes for the other. G takes priority for active production impact. A remains read-only regardless of a pending plan. For actions choose one primary lifecycle owner by the current request; supporting references/methods return control to it. Use the [conditional delivery loop](references/delivery-loop.md) only when a multi-stage business effort needs stage contracts; do not load it for every change.

| Work | Primary route |
| --- | --- |
| Conversation, knowledge question, read-only explanation or status lookup | Answer directly; inspect relevant facts if needed; no automatic lifecycle or method Skill |
| New project or first repository onboarding | `project-kickoff` |
| Explicitly requested requirements, feasibility or comparable-project research; or an accepted proposal to investigate an evidence gap | `project-research` |
| Feature, refactor, or approved-plan execution | `project-development` |
| Ordinary non-production bug or test failure | `project-development`; focused evidence gathering first; use `systematic-debugging` only if diagnosis remains unclear, recurs, spans components or is high risk |
| Fix with evidence-confirmed root cause and clear authorized boundaries | `project-development`; low-risk local fixes use inline regression checks; nontrivial/high-risk fixes may select `test-driven-development` |
| Dependency, runtime, CI, or toolchain change | `project-maintenance` |
| Security review, trust boundary, auth, or secrets | `project-security` |
| Acceptance, review, or evaluation | `project-verification` |
| Authorized bounded experiment for a decision-critical feasibility assumption | `project-verification` → feasibility-check reference |
| Business-module delivery and human review of actual effects | `project-verification` → business-acceptance reference |
| Documentation truth or project documentation update | `maintaining-project-docs` |
| Release readiness, migration, rollback, or authorized launch | `project-release` |
| Production impact or active incident | `project-incident-response`, then authorized diagnosis/repair |
| Existing-task session recovery, task switch, pause, or handoff | `project-continuity` |
| Cluttered project root, file classification, or requested directory restructuring | `project-organization` |

The lifecycle route owns scope and project truth. Choose by change and risk, not project size: a clear authorized low-risk change following an existing pattern proceeds directly through implementation and verification; unresolved design choices need brainstorming; multi-step dependencies, migration or cross-module delivery need one plan. Reuse approved decisions instead of seeking approval for each step. Feature/fix regression tests, unknown-failure diagnosis and fresh completion evidence remain required.

For actions or explicitly requested specialist work (review, diagnosis, acceptance), load one applicable lifecycle Skill. Clear low-risk local work uses that Skill alone, including applicable regression checks and fresh evidence; it automatically loads no Superpowers methods, including TDD, completion verification, review, or discovery wrappers. Focused checks precede fixes even on the light path. If diagnosis remains unclear, failures recur, or complexity/risk is discovered, promote only the affected work and load the relevant method for its current stage. A task's file count or a request to hurry does not establish low risk.

Substantial work selects individual methods when their concrete triggers apply; it does not load the whole library. An explicit request to apply a named method also selects it. Merely discussing a Skill, beginning a conversation, or reading files does not. `using-superpowers` is optional help for method selection/integration troubleshooting, never a bootstrap. Nested `superpowers:<name>` references resolve to the project-local sibling Skill, not a global plugin, and remain conditional on stage relevance. Host-level requirements still apply; existing global/plugin metadata is independent and an already open session may retain its old catalog.

Simple work needs no execution wrapper, parallel agent, separate formal acceptance route or iteration log. Formal acceptance, important independent review and cross-system evaluation use project-verification; ordinary verification stays within the current task. Never create a second spec or plan.

## Research before design, when needed

During kickoff, inspect the substance of existing requirements and sources, including document-only projects. If missing evidence affects a goal, feasibility or important design decision, describe the gap and proposed investigation, then ask whether the user wants research. A missing research directory or absent code is not a trigger. An explicit research request already supplies consent; a declined or unanswered proposal does not. Continue authorized work independent of the gap without repeatedly prompting.

After consent, project-research owns the bounded investigation and reviewable recommendations. User acceptance is a separate gate from permission to research. Only accepted items, with source and approval references, enter the existing spec/plan or lightweight task; pending and rejected ideas do not become executable requirements. Research does not authorize implementation or external mutations. Use brainstorming or writing-plans only if remaining design choices or delivery complexity warrant them; do not turn research into a mandatory method chain.

Persist useful evidence and review decisions only within document-write authority, preferably at existing project paths. Link them from the project context; retain task progress in its original state record. Read-only research returns a reviewable brief without writing files. Ordinary questions, clear local changes and already sufficient evidence do not require a research phase.

## Feasibility and business acceptance

These are conditional stages, not two more always-loaded Skills. If a critical assumption lacks current-environment evidence and failure would change the design or cause significant rework/cost, propose the smallest experiment with a hypothesis, representative inputs, success/failure criteria and time/cost limits. Information gaps may only need research; established low-risk patterns need ordinary tests, not a PoC. Reuse explicit experiment authorization; research permission alone does not authorize execution, spending or sensitive-data use. A probe's result is pass, fail or inconclusive within its tested scope, never automatic production readiness. Reuse an existing approved Spike contract rather than starting a second process.

Define a business module by a usable user outcome, including small modules. Agree on scenarios, samples, expected effects and the human reviewer before substantial implementation, and demonstrate the smallest end-to-end flow early. Technical pass is not human acceptance. Submit an actionable review package for the precise candidate, then keep the original task active with human_acceptance=pending until the user/designated reviewer explicitly accepts. Rejection or unresolved conditions require follow-up; silence, design approval and Agent self-review are not acceptance. Internal micro-changes without business-effect changes may be not_required with a concrete reason, not a loophole based on task size.

Store technical verification and human_acceptance separately in the same task record. Human acceptance binds its own candidate fingerprint and acceptance-criteria hash. Re-running tests does not refresh a human decision. Changed inputs/criteria require affected-item re-review; old records without human information remain unknown. Only current technical pass and current human acceptance (or genuinely inapplicable review) support done; pending work stays in the active index. Do not advance expensive dependent work or release on an unaccepted module; unrelated authorized tasks may continue. Completion, human acceptance and deployment authorization are separate.

## Recovery and handoff

When existing work needs recovery, follow recovery → one lifecycle route → applicable methods → implementation/verification → necessary facts. A fresh conversation with a clear new request starts at its matching lifecycle route; session freshness alone never selects `project-continuity`. `project-development` delegates actual recovery to `project-continuity`; it does not duplicate the task-state protocol. Prefer explicit task ID/file; automatic selection must be a unique active match to the current worktree/branch, never a fallback to an unrelated task or done record. Explicit historical lookup remains available. Without Git, verify the user pointer or a unique eligible record rather than guessing. Never choose by modification time. Rebuild stale state from code and fresh evidence before continuing.

Ordinary non-production Bug work keeps `project-development` as scope owner. Investigate before fixing; a cause established by focused inspection may support a low-risk inline repair with regression checks. Use systematic-debugging when uncertainty persists, investigation is nontrivial or risk is high; reuse a root cause already established by evidence. A symptom or proposed fix alone is not root-cause proof. A user's existing repair request supplies repair authorization within its scope; do not ask again merely because diagnosis finished. Diagnosis-only requests do not authorize a fix, and material scope/contract/data changes require confirmation. For production incidents, stabilize first. Dependency maintenance enters security only for an actual relevant trust boundary or explicit security review.

Parallel workers own disjoint files and individual task records. A single integrator updates the shared index and rechecks results; an unstable shared contract requires serial work. No lifecycle or method route creates permission for external operations.

Human entry: root `README.md` or `README.en.md`. Facts and archive rules: `docs/README.md`. The human entry states the tested scope and compatibility limits. Development-only test fixtures, evaluation harnesses and build records are intentionally not part of this copyable project foundation.

## Milestone control is a soft protocol

Pass an execution method only the currently approved milestone/task IDs and applicable spec/plan revision, with acceptance evidence, exclusions, budget, allowed tools and stopping conditions. Explicit approval of several milestones permits progression only when each dependency and human gate is satisfied. Nearby tasks are detailed, distant work stays adjustable. Reuse prior applicable approvals; material scope/contract/candidate changes reopen only affected decisions. Do not make every function a new approval request.

Halt affected dependents when a business assumption fails, acceptance is rejected, scope materially expands, a key dependency is unavailable, budget is exhausted or a new high-risk action is needed. Other independent authorized work may continue. Completion packages identify what changed, how to run/experience it, real integrations versus Mock, fresh checks/evidence, failures/unverified areas, the human decision needed and whether the next step may start.

Project Markdown and method prompts constrain behavior, not tool execution. `project_status.py` reads declared state/fingerprints; it is not a task allocator, authenticated approval system, deployment lock or spending limit. A host/CI may enforce separately configured controls, but this template installs none. Production credentials, tool permissions and paid-call budgets require their respective environment controls. Implementation approval, technical pass, human UAT and release authority remain separate.
