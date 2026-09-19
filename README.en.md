# Agentic Dev Workflow

[中文](README.md) | English

A long-term AI development workflow foundation that can be placed directly in a project root. It is designed for Codex by default, while also providing general rules, a standard Skill directory, and lightweight entry points for other tools.

It addresses *how to work with AI on development continuously and methodically*. It does not choose a framework for you or generate a business architecture. Small modules, small projects, existing products, and large systems can all use it: the workflow changes with the **risk and complexity of the current change**, not with the size of the project.

- For ordinary conversation, knowledge questions, and read-only explanations: answer directly, consulting only relevant files when project facts are needed.
- For simple, well-defined, low-risk changes: use the matching lifecycle Skill to implement and verify, without automatically loading Superpowers methods.
- When early requirements lack evidence needed for important decisions: explain the gaps, research after authorization, and have the user review each recommendation.
- When a critical feasibility assumption lacks evidence from the current real environment: propose a minimal PoC/Spike when warranted and test it within existing authorization before costly implementation.
- When delivering a business module or significant business flow: agree observable outcomes, samples, and a human reviewer first; technical verification still needs to be followed by human acceptance of the business result.
- For complex work or work with unresolved choices: clarify the design first, then proceed in stages using a single plan.
- When switching sessions or Agents: recover from project documentation, task state, and the actual workspace instead of relying on chat memory.
- When the project root is cluttered: classify the contents and propose a move plan first; after approval, reorganize the directories, update references, and verify the result.
- To control context: keep long-lived rules concise, and read Skill bodies and detailed references only when needed.

Current template version: `2.3.0`. It includes **11 project lifecycle Skills and 14 Superpowers method Skills, for 25 Skills in total**, with 27 managed adapter entry points and no sample application code, acceptance-test sample projects, or build history. Feasibility experiments and human business acceptance reuse `project-verification`; no Skill is added.

## 1. Get started in three minutes

### New project

1. Click **Use this template** on GitHub to create your own repository. Alternatively, download the ZIP and copy the extracted contents, including hidden directories, into an empty project root.
2. Open Codex—or another AI coding tool that can access project files—from that root directory.
3. Send the request below, replacing the bracketed text:

```text
First read AGENTS.md and use the in-project Skills as needed.
I want to build: [the goal and intended users].
First verifiable result: [one end-to-end business flow that can actually be demonstrated].
Business outcome and acceptance: [representative sanitized samples, observable expected results, and human reviewer; ask when unknown].
Constraints: [tech stack, runtime environment, data permissions, timeline, and so on; check unknowns read-only first and explain any gaps that need external research].
Please start with project-kickoff, clarify the boundaries first, and do not set up infrastructure that is not yet needed.
```

On first use, you can ask the Agent to perform a read-only check: where the project rules are, whether it can discover the 25 local Skills, and whether any global Skill with the same name or higher-level rule conflicts with them. **Discovering a name does not mean the Skill has already been run or verified.**

Kickoff starts by inspecting existing material read-only. If the project is still at the initial documentation stage or its requirements have weak supporting evidence, and a gap affects goals, feasibility, or an important design choice, the Agent explains the gap and asks whether to research it. A missing `docs/research/` directory alone is not a trigger; sufficient existing material, clear small tasks, and ordinary conversation do not need an added research step. An explicit research request already authorizes that scope and needs no repeated approval. If research is declined or the question is unanswered, the Agent does not browse externally or write research files without authorization.

### Existing project

Do not overwrite an existing project directly. First inspect the template in a separate directory, then ask the Agent to compare and merge `AGENTS.md`, same-named Skills, tool entry points, and documentation conventions. Preserve sound existing paths, the product README, the test system, and the project license whenever possible.

```text
Integrate this workflow into the existing project. Begin with a read-only inventory and list rule, Skill, and documentation conflicts together with the smallest viable merge plan.
Preserve the existing implementation, README, directory conventions, and uncommitted changes. Do not overwrite same-named files without confirmation.
```

You do not need to install every supported AI tool, and you do not need Python merely to use the Markdown rules. Only the optional helper scripts described below require Python.

## 2. Directory structure and purpose

```text
project-root/
├── README.md                    Chinese guide; replace it with your product homepage after project kickoff
├── README.en.md                 English guide
├── AGENTS.md                    Single entry point for foundational rules and task routing
├── CLAUDE.md                    Lightweight rule entry point for Claude
├── GEMINI.md                    Lightweight rule entry point for Gemini
├── .gitignore                   Ignore rules for caches, temporary files, and common local environment files
├── .gitattributes               Git conventions for cross-platform text and workflow fingerprints
├── .agents/skills/              Single source of truth for the 25 complete Skills
│   └── <skill-name>/
│       ├── SKILL.md             Trigger conditions and required steps
│       └── references/…         Detailed references or helper resources needed by only some Skills
├── .claude/skills/              Lightweight Skill entry points that forward to the source of truth; no duplicate bodies
├── .ai-workflow/
│   ├── ROUTING.md               Selection rules for lifecycle and method Skills
│   ├── superpowers-compat.md    How Superpowers fits this project's permissions and graduated workflow
│   ├── references/delivery-loop.md Conditional stage contracts; not required reading for every task
│   ├── templates/               Templates for project context, research, tasks, designs, and verification
│   │   ├── research-brief.md    Use when research needs a persistent record
│   │   ├── feasibility-check.md Record a minimal experiment's question, boundaries, and actual evidence as needed
│   │   └── business-acceptance.md Record business acceptance criteria, demonstration evidence, and human decisions
│   ├── scripts/                 Two day-to-day helper commands and three internal dependency modules
│   ├── third_party/             Upstream licenses, versions, file checksums, and patch records
│   ├── VERSION                  Workflow version
│   ├── SOURCES.lock.json        Locked research and third-party sources
│   ├── ADAPTERS.lock.json       Fingerprints of managed adapter files, preventing accidental overwrite of manual changes
│   ├── LICENSE                  MIT license for the original parts of this workflow
│   ├── LICENSE-SCOPE.md         Scope of the license
│   └── THIRD_PARTY_NOTICES.md   Third-party source notices
└── docs/
    └── README.md                Project documentation navigation and maintenance conventions
```

There are no pre-created `src/` or `apps/` directories, databases, containers, or CI configurations. Those should be determined by the actual product and technology stack. Skill subdirectories such as `references/` and `scripts/` exist only where they have a real purpose; required upstream resources are not sample application code.

Research, experiment, and business acceptance records are also created only when needed; the initial package does not create empty product directories. The [feasibility-check.md](.agents/skills/project-verification/references/feasibility-check.md) and [business-acceptance.md](.agents/skills/project-verification/references/business-acceptance.md) references under `project-verification/references/` provide execution guidance; the templates hold actual records.

Some optional Superpowers helpers require Git, Node.js, Bash, or host support for multiple agents or a browser. Check these only when needed; you do not have to install everything up front. Do not run Bash scripts as if they were PowerShell commands. When a capability is unavailable, use a supported serial or manual-check approach and state what was not run.

The development tests, evaluation scaffolding, historical logs, and packaging records for this template are not copied into the foundation. **This does not mean product projects can omit tests**; features and fixes should still add applicable tests and run verification.

## 3. Day-to-day use

Usually, you can simply describe what you need and let the Agent choose an entry point according to the rules; you do not have to memorize every Skill name. Tools that support explicit Skill selection may also accept syntax such as `$project-development`. The exact selection mechanism depends on the host.

| What you want to do | Entry point, as needed |
| --- | --- |
| Have an ordinary conversation, ask a knowledge question, or request a read-only explanation or status | Answer directly; read relevant files for project facts, without automatically loading method Skills |
| Start a project from scratch or integrate the workflow into an existing project for the first time | `project-kickoff` |
| Conduct explicitly requested or approved project research and compare evidence for options | `project-research` |
| Build a feature, refactor, fix an ordinary non-production bug, or execute an approved plan | `project-development` |
| Resume a task, switch sessions, pause, or hand off work | `project-continuity` |
| Organize scattered files or restructure directories | `project-organization` |
| Maintain dependencies, runtimes, or toolchains | `project-maintenance` |
| Run a minimal feasibility experiment, technical or human business acceptance, code review, or performance, AI, or UX evaluation | `project-verification` |
| Review security, identity, authorization, or tenant boundaries | `project-security` |
| Maintain project facts, usage instructions, or documentation | `maintaining-project-docs` |
| Prepare a release, migration, or rollback | `project-release` |
| Respond to a production incident or active security impact | `project-incident-response` |

### Route by risk, not project size

Assess five dimensions: requirement clarity; interaction uncertainty; technical/data/integration uncertainty; permissions, external writes, money, privacy and production exposure; blast radius and recovery cost. See [ROUTING.md](.ai-workflow/ROUTING.md).

| Path | Typical work | Minimum approach |
| --- | --- | --- |
| A Read-only | Progress, explanation, knowledge | Answer or inspect relevant facts; do not execute pending work |
| B Clear local change | Button wording, diagnosed low-risk bug | Scope/acceptance → impact check → small edit → regression → result; no mandatory PRD or prototype |
| C Unclear interaction | Review order, roles, rejection rules | Clarify, then preview if useful; prefer existing components and cover waiting/failure/cancel/reject/takeover |
| D Backend | APIs, data, retrieval, performance | Contracts, samples, tests, logs, performance and recovery evidence; no mandatory UI |
| E Core uncertainty | AI quality, algorithms, data/tool integration | Test the riskiest assumption first with samples, thresholds, budget and stop conditions |
| F High risk | Auto-publish, permissions, deletion, migration | Authority, audit, idempotency and compensation; isolated checks before controlled execution, even for a one-line change |
| G Production incident | Outage, severe degradation, data/security impact | Contain → authorized recovery → verify → record → retrospective |

Paths can combine, such as C + E, but one current lifecycle route owns scope. A prototype does not prove technical feasibility; a PoC does not prove business usability. MVP reduces scope, not basic quality.

### A loop from the problem to long-term maintenance

A larger business effort can use: problem/current process/baseline → requirements and acceptance → prototype or technical experiment → continue/adjust/reduce/stop → architecture/contracts and plan → small business increments → tests/Eval and human UAT → readiness → deployment and controlled exposure → operating feedback/value → another iteration or retirement. Activities can be trimmed, parallelized and revisited, not repeated as a fixed waterfall.

Security, tests, AI Eval, observability and recovery preparation start during design and each increment. Read [delivery-loop.md](.ai-workflow/references/delivery-loop.md) only when multi-stage coordination needs it; simple tasks skip it. The existing [spec.md](.ai-workflow/templates/spec.md) can contain the PRD; do not create duplicate requirements just to obtain a filename.

Each milestone can use the existing task/plan for requirements and scope/exclusions, greatest uncertainty and its check, operable artifact, acceptance and budget, dependencies/risks/rollback, owner and reviewer. Detail near-term work and keep later work adjustable. Prefer a usable vertical slice over completing every database layer before any usable result.

```text
Execute only the approved M1 in the existing spec/plan.
Deliver what changed, how to run or experience it, real versus Mock integrations,
actual checks and evidence, failures/unverified areas, what I must confirm,
and whether the next step may proceed.
If M1 acceptance fails, halt dependent M2; independent authorized work may continue.
```

Explicit approval of multiple milestones permits continuous work when prerequisites are met, without approval for every function. Stop affected work if a business assumption fails, acceptance is rejected, scope materially expands, a key dependency disappears, budget is exhausted or a new high-risk operation is needed. Design/implementation approval is not production authority; Agent or SDD controller rulings are not human business acceptance.

### Conditional AI/Agent extensions

Add these only when the product itself includes AI/Agent behavior. Using an AI coding assistant for ordinary software does not require a full AI document set. Extend the existing spec using the [Agent contract](.agents/skills/project-development/references/agent-contract.md) and [AI evaluation reference](.agents/skills/project-verification/references/ai-evaluation.md): tool IO/permissions/side effects, context and memory sources, budgets/retries/stops/takeover, and model, Prompt, Skill, tool, knowledge and configuration versions.

Distinguish software tests, AI quality evaluation, business UAT and post-release value. Fix permitted representative samples, development and independent acceptance sets, professional rubrics, baselines/thresholds, randomness and quality/latency/cost trade-offs. LLM judges assist domain reviewers, not replace them. Relevant Prompt, Skill, tool and knowledge changes trigger regression even without code changes.

Merge is not deployment, and deployment is not full exposure. Canary rollout usually already runs in production and requires corresponding authority. Code rollback cannot undo sent notifications or all external business actions. Verify and classify feedback, form an improvement hypothesis, test/Eval, then approve and release; never turn feedback directly into live production rules or persistent memory. An optional [Impact Log](.ai-workflow/templates/iteration.md) records actual baseline, window, sample/metric definitions, results, review/rework costs, limitations and business confirmation, not invented benefits.

### One illustrative example: reusing garment-image processing requirements

This is an example only, not actual company requirements, an implemented feature or an approval:

1. If the interaction is unclear, clarify “choose requirements—apply to one image—edit—review.” Prefer existing components; label Mock data and include cancellation, failure and human takeover.
2. If AI pattern preservation is unknown, use a bounded PoC with permitted samples, preset quality criteria and budget. Missing sample permission remains a gap; attractive UI is not feasibility evidence.
3. When evidence supports proceeding, deliver a real single-image-to-human-review loop with an exact candidate, experience steps and evidence. Do not advance dependent batch processing if core acceptance fails.
4. Human acceptance is not production authority. Check external writes, rollout cohorts, observation, idempotency/compensation and takeover. Measure actual review time/rework and limitations after release before deciding the next iteration.

### Research before deciding

When evidence is missing, the sequence is: **read-only inventory → confirm research scope → research and compare → user reviews each item → accepted items enter the existing design/plan and acceptance criteria → continue within the original authorization**. An explicit research request already authorizes its scope. Research approval does not approve a technology choice, implementation, or external writes; subsequent actions still depend on the authorization already given.

```text
Use project-research to investigate whether offline document retrieval suits this project.
Compare only offline availability, licensing, maintenance, and the cost of integrating with the existing Python service.
Consult official material, relevant papers, and closely matching GitHub projects. Give me sources, recommendation IDs, and unsuitable uses for review first.
```

Research compares fit, maintenance, licensing, reuse cost, and unsuitable uses against the bounded questions; it does not copy projects based on star rankings. Each recommendation gets a stable ID, such as `R-01`, linked to traceable sources. Facts, inferences, and unverified claims are identified separately. If browsing is unavailable, state the limitation without claiming to have consulted sources.

You can review the results with a response such as:

```text
Accept R-01, reject R-02, and leave R-03 pending.
Add only R-01 to the existing spec/plan and acceptance criteria, retaining sources and review decisions. Do not implement it yet.
```

Only accepted items may enter the existing authoritative spec/plan and acceptance criteria; rejected and pending items stay in the research record. Small research tasks can be completed in a table in the response. When a persistent record is needed, use [research-brief.md](.ai-workflow/templates/research-brief.md) at the project's existing location, or create `docs/research/<topic>.md` as needed. Keep only a link in the project facts entry point. Do not require a new directory or a second plan, and do not treat candidate recommendations as approved requirements in a later session.

### Test critical assumptions with a minimal experiment

The Agent judges whether a PoC/Spike is warranted by risk: propose the smallest experiment that answers a critical assumption when it lacks evidence from the current real environment and failure could change the approach, cause substantial rework, or incur significant cost. Use `project-research` first when the gap is missing information. Mature, low-risk reuse usually needs no PoC, and a routine test alone does not warrant an experiment workflow.

```text
Use project-verification to check whether the existing offline retrieval approach can handle our representative sanitized documents.
Inspect the current evidence first; if a critical assumption remains unverified, define a minimal PoC.
State the question, samples and environment, pass/fail criteria, time and cost limits, and stopping conditions.
Execute within the authorized local scope. Identify any additional authorization needed for external code execution, paid services, or a wider scope.
Report pass, fail, or insufficient evidence from actual results, then explain the impact on the existing design/plan.
```

An experiment proposal or inference from documentation cannot replace an actual execution result. Preserve the environment, samples, operations, and evidence; report failures and insufficient evidence honestly. A prototype is not automatically a production implementation. Research authorization does not authorize running external code or paid calls; explicit authorization already covering the same experiment scope needs no repeated approval. Use [feasibility-check.md](.ai-workflow/templates/feasibility-check.md) when a persistent record is needed, linking the existing task and single design/plan instead of creating another implementation plan.

### Require human acceptance before completing a business module

A business module is defined by a result a user can accomplish, so small modules also require acceptance. Internal adjustments or small copy edits may be exempt, but line counts cannot exempt changes to business outcomes. Before implementation, agree the business goal, representative sanitized samples, observable expected outcomes, and human reviewer; ask about unknowns instead of inventing them. Demonstrate a minimal end-to-end flow early to catch misunderstandings.

```text
Implement the expense-report bulk import module. First agree the business goal, representative sanitized samples, expected outcomes, and human reviewer with me.
Demonstrate a minimal flow from importing one sample batch to checking its results, then complete the agreed scope.
After technical verification passes, provide the candidate version, entry point and steps, expected versus actual results, evidence, limitations, and items for my confirmation.
Until I explicitly accept it, mark it as technically complete and awaiting human acceptance; do not mark the whole module complete.
```

Silence does not mean acceptance. A rejection, or conditional acceptance with outstanding conditions, remains returned or pending. Until a human explicitly accepts the result, do not automatically start costly steps or releases that depend on it; independent, already authorized work may continue. Fixes already authorized within the original task may proceed; requirement or scope changes still need confirmation. Relevant implementation or acceptance-criteria changes require review of the old acceptance, without restarting the entire process for every small function.

Use [business-acceptance.md](.ai-workflow/templates/business-acceptance.md) as needed to retain criteria, demonstration evidence, and human decisions; dynamic status stays in the original task record. Technical tests establish the technical behavior checked, while human acceptance confirms the business result. Neither substitutes for the other.

### Small changes

```text
Add an optional parameter to the existing function while preserving the old calling convention. Change only the relevant implementation and tests.
Acceptance criterion: [specific boundary behavior]. Complete the change and run the existing verification.
```

When the goal, acceptance criteria, and boundaries are clear and a low-risk local change follows an existing pattern, use only the matching lifecycle Skill, briefly explain the approach, then implement and verify. Do not automatically load any Superpowers method. Applicable regression tests, root-cause investigation, and fresh workspace evidence for completion claims still apply; these requirements do not require reading the full TDD, debugging, or completion-verification method. A new spec, plan, parallel task, or iteration log is not required.

### Complex work

```text
Implement bulk import and interrupted-run recovery. The existing API must remain compatible.
First investigate existing callers and data constraints, clarify unresolved design choices, then maintain one implementation plan and verify the work in stages.
Do not repeatedly ask about decisions that have already been approved. Confirm again only when materially changing data or an external contract.
```

For an unknown failure, identify the root cause first; a root cause supported by evidence can be used directly for an authorized fix. Parallelize only when there are genuinely independent tasks, stable boundaries, and host support. Committing, pushing, deploying, using paid services, and performing destructive actions each require their own authorization; permission for them cannot be inferred from approval of a design.

## 4. How to organize a cluttered directory

```text
Use project-organization to inventory the current project.
Identify scattered code, configuration, reference material, task briefs, and drafts. Start with a read-only mapping from each current path to its proposed destination.
Explain affected imports, run commands, documentation links, verification, and rollback. Do not move files yet.
```

After the plan is confirmed, explicitly approve the exact scope of the move. Before execution, the Skill rechecks the source files and destinations. It stops instead of proceeding blindly if a source file has changed, a destination already exists, a link would escape its allowed boundary, or a consumer is unclear.

It does not put every `.py` file into `src/` based solely on its extension, and it does not treat a draft as an approved task brief. Runtime entry points may remain where they are; same-named documents are not overwritten; secret configuration is classified by path without reading its values; and unknown files and user changes remain untouched. When moving code is approved, references must be updated and applicable tests rerun.

## 5. Documentation for both people and Agents

See [docs/README.md](docs/README.md) for the full conventions. Use the project's existing paths first. If the project has no convention, create entries from the table below as needed instead of copying every template at once.

| Document | What it records | When it is needed |
| --- | --- | --- |
| Product README | Project purpose, startup instructions, and documentation entry points | Maintain it after kickoff; do not let the template guide remain the permanent product homepage |
| `docs/project-context.md` | Current capabilities, tech stack, real commands, module map, milestones, and known limitations | On first integration and when project-level facts change; keep it concise |
| `docs/tasks/index.md` | Active task IDs, owners, worktrees, and links to task files | When there are active tasks that need ongoing tracking |
| `docs/tasks/<ID>.md` | Goal, completed work, technical verification, human acceptance state, risks, and next step | For cross-session or unfinished work; this is the source of truth for dynamic state |
| `docs/research/<topic>.md` | Research questions, sources, recommendation IDs, accepted/rejected/pending decisions, and where accepted items were incorporated | For authorized research that needs a persistent record; prefer existing paths, and keep small research tasks in the response when sufficient |
| Existing experiment location + `feasibility-check.md` template | Experiment question, samples/environment, criteria, resource limits, actual results, and evidence | When a critical assumption needs a minimal experiment and a persistent record; do not create empty directories |
| Existing acceptance location + `business-acceptance.md` template | Business goal, criteria, candidate version, demonstration material, human decision, and its basis | For delivery of a business module or significant flow; link the original task without duplicating dynamic state |
| `docs/specs/`, `docs/plans/` | Approved design and the single implementation plan | When a written design or complex sequence of steps is needed |
| `docs/adr/` | Long-lived architecture decisions, their reasoning, and successor decisions | For important decisions, not routine activity logs |
| `docs/iterations/` | Historical summaries, verification, and remaining items from significant iterations | When an iteration result is worth preserving |
| `docs/operations/` | Actual records of releases, migrations, rollbacks, and incidents | When real operational work requires them |

A completed small change may be reported only in the response. Even when unfinished work is small, preserve a minimal state record within the existing write authorization before pausing or handing off; for a read-only task, state that it “has not been persisted.” Completed tasks leave the active index, but their original records and evidence links remain.

Placeholders in templates such as `RAG-003` and `src/example.py` must be replaced with real identifiers. They must not be treated as facts about the project.

## 6. How to continue in a new session

Before ending the current session:

```text
I am going to switch sessions. Update the actual state, verification evidence, risks, and exact next step for task TEXT-001.
Keep a single task record and its readable snapshot; do not copy the entire chat.
```

In the new session:

```text
Continue task TEXT-001. First use project-continuity to check the task file against the actual workspace.
Summarize the goal, completed work, uncommitted contents, verification, risks, and exact next step, then continue within the approved scope.
```

The JSON on the first line of the task file is the only structured state. The human-readable snapshot below it is generated by a script. They are not two separately maintained progress records. The script is read-only and does not write changes back automatically: ask the Agent to update the marked region within the authorized scope while preserving manually written background and evidence notes.

Version `2.2.0` adds optional `human_acceptance` to the existing task state, separating human business acceptance from technical verification. Older records without it remain readable, but their human acceptance is `unknown`, not a business pass. Keep the task `active` while awaiting human acceptance. The verification item in the six-item snapshot shows both technical and human status.

An accepted record needs the reviewer, decision basis, timestamp, and independent fingerprints for the candidate version and acceptance criteria. Relevant code or criteria changes make the human acceptance evidence's freshness `stale`; rerunning technical tests does not renew human sign-off. A task that truly does not affect business outcomes may record `not_required`, but it needs a specific reason and the current `criteria_sha256` to remain `fresh`; a missing hash is `unknown`, and changed criteria make it `stale`. The script checks structure and fingerprints; it cannot authenticate a human sign-off or decide whether a business task should be exempt. Do not fabricate a reviewer's identity or consent. Follow [task-state.md](.ai-workflow/templates/task-state.md) for the exact fields.

```powershell
# Windows PowerShell; run from the product project root and replace the task ID with the real one.
py -3 -B .ai-workflow/scripts/project_status.py --root . --task TEXT-001
py -3 -B .ai-workflow/scripts/project_status.py --root . --task TEXT-001 --format json --require-fresh
py -3 -B .ai-workflow/scripts/project_status.py --root . --task TEXT-001 --require-complete --format json
py -3 -B .ai-workflow/scripts/project_status.py --root . --task TEXT-001 --format markdown
py -3 -B .ai-workflow/scripts/project_status.py --root . --task TEXT-001 --check-view
```

Read the current criteria hash from `snapshot.human_acceptance.current_criteria_sha256` in the JSON output. It binds the task's `goal`, `acceptance`, and `scope`. Follow [task-state.md](.ai-workflow/templates/task-state.md): copy it into `human_acceptance.criteria_sha256` only after genuine acceptance of the current candidate or an actual determination that acceptance is not required. Reading the hash does not establish human consent.

On macOS or Linux, replace `py -3 -B` with `python3 -B`. The script uses only the Python 3.10+ standard library. Version `2.0.0` was tested on Windows with Python 3.11.9; other systems need verification in their own projects.

If no task record exists, create a real record from the template first; do not fabricate a snapshot. When several tasks exist, do not guess based on the “latest date.” After relevant files change, old verification becomes stale or unknown and cannot continue to be treated as passing. A missing or stale view makes `--check-view` return 1; a structural error returns 2. If Python is unavailable, manually check the same six items and state that they were not automatically verified.

`--require-fresh` checks technical verification freshness only; it does not establish a technical pass or business acceptance. Use `--require-complete` for the completion gate: the task must be `done`, technical verification must be `pass` and `fresh` with nonblank `command` and result `evidence`, and human acceptance must be either `accepted` and `fresh` or `not_required` with a specific reason, the current `criteria_sha256`, and `fresh` evidence. For non-command checks, record actual inspection steps in `command`; the script does not execute or authenticate these records. Unmet conditions return 1; structural errors return 2. Retain the actual pending state until an explicit human decision is received; do not mark work complete merely to pass the check.

`--task <ID>` selects from the active index. For a completed task removed from that index, provide its exact file path; the tool does not scan all history:

```powershell
py -3 -B .ai-workflow/scripts/project_status.py --root . --task-file docs/tasks/TEXT-001.md --check-view --require-fresh
```

This is not real-time monitoring or permanent memory. Reliable continuation depends on saving the necessary facts before every pause and rechecking code, configuration, and evidence in the new session.

In `2.3.0`, automatic recovery selects only a uniquely matching active task in the current worktree/branch; no match does not fall back to an unrelated branch, and completed tasks are not automatically resumed. With Git but no recorded workspace identity, select the task explicitly. `--task` and `--task-file` still support deliberate historical queries. Without Git, the script can show a unique active record, but the Agent must verify its relevance and existing authority before continuing. State schema 1 is unchanged.

## 7. Why Skills are loaded on demand

`AGENTS.md` contains only long-lived constraints, grading rules, and entry points; Skill names and descriptions support discovery; bodies are read when used; and reference files are opened only when needed for the current step. Classify the current request before choosing what to read:

| Current request | Loading scope |
| --- | --- |
| Ordinary conversation, a knowledge question, or a read-only explanation or status query | No automatic method workflow; consult only relevant files when project facts are needed |
| A low-risk local task with clear goals, acceptance criteria, and boundaries that follows an existing pattern | One matching lifecycle Skill; no automatic Superpowers method loading |
| Non-simple or high-risk work, multi-step dependencies, or a complex unknown failure | One lifecycle Skill owns the scope and selects only the specific methods needed at the current stage |
| An explicit request to use a method | Use the requested method; merely naming it or asking what it means is not an invocation request |

Method loading is separate from basic quality requirements: simple tasks still need applicable tests, root-cause checks, and verified evidence. Add a method when risk or complexity increases. Starting a new conversation alone does not trigger Superpowers or imply resuming an old task.

The following methods remain available for automatic discovery when applicable, under the primary lifecycle route:

| Method | Purpose |
| --- | --- |
| `brainstorming`, `writing-plans` | Resolve open design choices and prepare complex implementation plans |
| `test-driven-development`, `systematic-debugging` | Design tests for non-simple or high-risk features and fixes, and systematically investigate complex unknown failures |
| `verification-before-completion` | Check verification gates for non-simple or high-risk delivery; simple tasks verify evidence within their primary route |
| `requesting-code-review`, `receiving-code-review` | Handle work needing in-depth or independent review and complex review feedback |
| `dispatching-parallel-agents`, `subagent-driven-development`, `executing-plans` | Coordinate independent work or execute an existing plan when needed |
| `using-git-worktrees`, `finishing-a-development-branch` | Isolate work and handle integration wrap-up when needed |
| `writing-skills` | Validate scenarios when creating a Skill or materially changing its behavior |
| `using-superpowers` | Optional guidance for method selection or integration troubleshooting; not a session startup entry point |

Version `2.0.1` adds project applicability boundaries to the descriptions and entry sections of all 14 methods, and removes the session-start, before-any-response, and “1% chance” mandatory chain from `using-superpowers`. See [PATCHES.md](.ai-workflow/third_party/superpowers/PATCHES.md) for the changes. This template aims to reduce duplication and irrelevant reading, but **does not promise a fixed percentage of token savings**.

## 8. AI tool adapters and actual boundaries

| Tool | Entry points provided by this template | Before use |
| --- | --- | --- |
| [Codex](https://learn.chatgpt.com/docs/customization/overview#skills) (default) | `AGENTS.md` + `.agents/skills/` | Open from the project root and confirm local discovery results |
| Claude Code | `CLAUDE.md` + forwarding entries in `.claude/skills/` | Bodies still come from `.agents/skills/`; check for global plugins with the same names |
| Gemini | `GEMINI.md` + the shared Skill directory | Verify the current version's support for importing rules and loading Skills |
| [GitHub Copilot](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills) | `AGENTS.md` + the shared Skill directory | IDE/CLI behavior may vary by version; `gh` is not a Copilot acceptance test |
| [Cursor](https://prod.cursor.com/docs/skills) | `AGENTS.md` + the shared Skill directory | Confirm current project entry points and Skill support; file presence is not proof of testing |
| [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md) | Shared rules and Skill directory | Depends on whether the actual version or preset enables rule loading, file-based Skill exposure, and Skill consumption; test it directly |

Other tools can also be pointed explicitly to these files if they can read project rules and Markdown Skills. An ordinary chat interface without file, terminal, and write access can only discuss or review the project; it cannot actually operate on local files. This template does not grant a host additional tools or permissions.

Do not maintain separate full copies of the same rules. The Claude and Gemini entry points only forward to the source of truth. No extra `.dsh/skills/` directory is created for DeepSeek Harness because it might take precedence over the shared entry point.

Project methods and a globally installed Superpowers plugin with the same names are independent sources. These patches affect only the canonical `.agents/skills/` files and their adapters; they do not modify global plugins. References between methods should continue to resolve to the project copies. A Skill catalog already injected into the current session may not refresh when files change; after updating, verify sources through the host's supported rediscovery mechanism or a new session. If the host still mandates a separate plugin, check its configuration and higher-priority rules. The template cannot guarantee that every host will suppress all loading.

## 9. Two helper scripts

### `project_status.py`: recover state

See Section 6 for its purpose and usage. It depends internally on `_taskstate.py` and `_workflowlib.py`; do not copy only the entry-point file. Git is optional. If Git is unavailable, the script will not initialize a repository automatically, and “unknown uncommitted state” must not be described as clean.

### `sync_adapters.py`: maintain tool entry points

After changing the rules or built-in Skills, inspect the generation plan before deciding whether to write changes. The default is a dry run. If manual edits cause a conflict, the original file is preserved rather than forcibly overwritten.

```powershell
py -3 -B .ai-workflow/scripts/sync_adapters.py --root . --json
py -3 -B .ai-workflow/scripts/sync_adapters.py --root . --check --json
py -3 -B .ai-workflow/scripts/sync_adapters.py --root . --apply --json
```

On POSIX systems, use `python3 -B` here as well. The script depends internally on `_skillmeta.py`, `_workflowlib.py`, and `ADAPTERS.lock.json`. Passing the adapter check proves only that generated files are consistent; it does not prove that any particular AI tool has successfully executed the workflow.

After adding project-specific Skills, you can use `--allow-extra-skills`. It maintains entry points for only the 25 built-in Skills while preserving additional Skills, their proxies, and their lock records. Other tool entry points for additional Skills remain the project's responsibility; this option does not generate proxies for them automatically.

```powershell
py -3 -B .ai-workflow/scripts/sync_adapters.py --root . --allow-extra-skills --check --json
```

## 10. Customization and upgrades

- Put a project-specific Skill in `.agents/skills/<clear-unique-name>/SKILL.md` and state when it applies. Put detailed material in its references directory instead of filling `AGENTS.md` with a long manual.
- Let product code follow the actual technology stack. Do not move every directory or replace the test framework for the sake of the template.
- Keep a copy of the original template version. When upgrading, compare upstream changes and merge them with your own rules and Skills; do not download a new template over the entire product root.
- Before modifying vendored Superpowers content, check its source and license, record the actual patch in `.ai-workflow/third_party/superpowers/PATCHES.md`, and verify affected behavior. A version upgrade does not mean every previous behavior still holds.
- After project kickoff, the root README should introduce your product. If the template guide still needs to be retained, keep the necessary links in the existing development documentation instead of maintaining two conflicting project homepages.

## 11. Verification scope and limitations

Limited `2.3.0` verification ran on Windows / Python 3.11.9 in the current Codex desktop conversation host. Historical results are not counted:

| Layer | Actual scope and result |
| --- | --- |
| Script behavior regression | Explicit delivery-root binding: 22 state unit tests, 24 status CLI tests, 18 human-acceptance-record tests and 12 adapter behavior tests; all 76 passed, none skipped |
| Structure and copy installation | 25 Skill metadata files, 27 adapters, 60 upstream file hashes and 14 patch hashes, 165 UTF-8 files, compilation of 5 Python files, 130 local document links and the task template passed; all 165 files retained bytes when copied to a path containing Chinese characters/spaces, and copied adapters passed checks |
| Implementation samples | Button wording changed only its target file, with 2 existing tests plus wording/byte checks passing; equivalent backend optimization and approved M1 implementation each passed 4 tests. The former includes a reproducible local benchmark, with no added UI; M2 was not implemented |
| Other host scenarios | Interaction clarification, unknown AI quality, auto-publish, failed core acceptance, status-only, incident, scope change, Mock acceptance and recovery: 9 read-only scenarios. Responses and file fingerprints were checked for scope; no unauthorized writes occurred. Together with the 3 implementation samples, this covers 12 scenario types |

The old-rule baseline already respected Mock, cost and human-acceptance boundaries; this release does not claim to fix every prior Agent judgment. Real task-selection defects were reproduced by failing tests before correction. Independent review also found a Windows path-case regression, subsequently covered by failing/passing verification. Interaction states and independent M3 authorization received clarification follow-ups. These are not 12 complete end-to-end product acceptance tests.

Scenarios used separate directories outside the template but reused subagent conversations under host task-count limits; they are not all independent blind trials. Shared host rules and Skill discovery can affect results. No repeated multi-model campaign was run, and underlying model version, randomness and billed tokens were not independently verified. Remote links and Markdown anchors were not individually fetched; 15 upstream documentation example links inside code fences were excluded from navigation checks. No real-production, cross-tool or cross-system certification is claimed.

Markdown and Skills are **soft behavioral constraints**. This template includes no task executor, authenticated approval service or automatic deployment gate. `project_status.py` checks declared records and bounded fingerprints; it cannot establish reviewer identity, evidence truth or production authority. Tool permissions, production credentials and spending budgets need their respective environment controls. Stronger gates are separate integrations.

This run uses no Codex CLI, dependency installation or external paid-model API calls. Fixtures, behavior scoring, logs and development harnesses stay outside the copyable template. There is no CI or one-click installer: installation is a complete directory copy or GitHub template use. Product projects still need their own tests and CI.

A single Agent scenario does not establish statistical reliability. Unchecked hosts/models, real business UAT, production operation and billed-token savings are not claimed as passing. A host may inject same-name global Skills, retain an older catalog or impose higher-priority rules. No files guarantee error-free results across every tool/model/project; the template supplies a maintainable starting point and explicit evidence boundaries.

## 12. Sources and licenses

The foundational rules were researched with reference to [Misayhuiyi/Rules](https://github.com/Misayhuiyi/Rules). They independently restate principles for investigation, reuse, simple solutions, precise changes, environment adaptation, and verification, without carrying over personalized assumptions such as “there are no existing users.”

The 14 method Skills are based on the locked [Superpowers 6.3.0](https://github.com/obra/superpowers/tree/b36e0829c6d0140e93cfef2ca599b1b07d4a7797) with this project's on-demand routing patches; their bodies are not all unchanged upstream copies. Version, license, upstream provenance, and separately identified UI metadata are documented in the [source lock](.ai-workflow/SOURCES.lock.json), [third-party notices](.ai-workflow/THIRD_PARTY_NOTICES.md), and [patch record](.ai-workflow/third_party/superpowers/PATCHES.md). This project is not an official distribution of any of these AI tools.

The original workflow is released under the [MIT License](.ai-workflow/LICENSE); see [License Scope](.ai-workflow/LICENSE-SCOPE.md) for details. This does not automatically select a license for your product code, data, images, or product documentation. Project owners should choose their own project license.
