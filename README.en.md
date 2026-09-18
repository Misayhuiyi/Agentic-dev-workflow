# Agentic Dev Workflow

[中文](README.md) | English

A long-term AI development workflow foundation that can be placed directly in a project root. It is designed for Codex by default, while also providing general rules, a standard Skill directory, and lightweight entry points for other tools.

It addresses *how to work with AI on development continuously and methodically*. It does not choose a framework for you or generate a business architecture. Small modules, small projects, existing products, and large systems can all use it: the workflow changes with the **risk and complexity of the current change**, not with the size of the project.

- For ordinary conversation, knowledge questions, and read-only explanations: answer directly, consulting only relevant files when project facts are needed.
- For simple, well-defined, low-risk changes: use the matching lifecycle Skill to implement and verify, without automatically loading Superpowers methods.
- For complex work or work with unresolved choices: clarify the design first, then proceed in stages using a single plan.
- When switching sessions or Agents: recover from project documentation, task state, and the actual workspace instead of relying on chat memory.
- When the project root is cluttered: classify the contents and propose a move plan first; after approval, reorganize the directories, update references, and verify the result.
- To control context: keep long-lived rules concise, and read Skill bodies and detailed references only when needed.

Current template version: `2.0.1`. It includes **10 project lifecycle Skills and 14 Superpowers method Skills**, with no sample application code, acceptance-test sample projects, or build history.

## 1. Get started in three minutes

### New project

1. Click **Use this template** on GitHub to create your own repository. Alternatively, download the ZIP and copy the extracted contents, including hidden directories, into an empty project root.
2. Open Codex—or another AI coding tool that can access project files—from that root directory.
3. Send the request below, replacing the bracketed text:

```text
First read AGENTS.md and use the in-project Skills as needed.
I want to build: [the goal and intended users].
First verifiable result: [one end-to-end business flow that can actually be demonstrated].
Constraints: [tech stack, runtime environment, data permissions, timeline, and so on; investigate any unknowns first].
Please start with project-kickoff, clarify the boundaries first, and do not set up infrastructure that is not yet needed.
```

On first use, you can ask the Agent to perform a read-only check: where the project rules are, whether it can discover the 24 local Skills, and whether any global Skill with the same name or higher-level rule conflicts with them. **Discovering a name does not mean the Skill has already been run or verified.**

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
├── .agents/skills/              Single source of truth for the 24 complete Skills
│   └── <skill-name>/
│       ├── SKILL.md             Trigger conditions and required steps
│       └── references/…         Detailed references or helper resources needed by only some Skills
├── .claude/skills/              Lightweight Skill entry points that forward to the source of truth; no duplicate bodies
├── .ai-workflow/
│   ├── ROUTING.md               Selection rules for lifecycle and method Skills
│   ├── superpowers-compat.md    How Superpowers fits this project's permissions and graduated workflow
│   ├── templates/               Templates for project context, tasks, designs, verification, and other documents
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

Some optional Superpowers helpers require Git, Node.js, Bash, or host support for multiple agents or a browser. Check these only when needed; you do not have to install everything up front. Do not run Bash scripts as if they were PowerShell commands. When a capability is unavailable, use a supported serial or manual-check approach and state what was not run.

The development tests, evaluation scaffolding, historical logs, and packaging records for this template are not copied into the foundation. **This does not mean product projects can omit tests**; features and fixes should still add applicable tests and run verification.

## 3. Day-to-day use

Usually, you can simply describe what you need and let the Agent choose an entry point according to the rules; you do not have to memorize every Skill name. Tools that support explicit Skill selection may also accept syntax such as `$project-development`. The exact selection mechanism depends on the host.

| What you want to do | Entry point, as needed |
| --- | --- |
| Have an ordinary conversation, ask a knowledge question, or request a read-only explanation or status | Answer directly; read relevant files for project facts, without automatically loading method Skills |
| Start a project from scratch or integrate the workflow into an existing project for the first time | `project-kickoff` |
| Build a feature, refactor, fix an ordinary non-production bug, or execute an approved plan | `project-development` |
| Resume a task, switch sessions, pause, or hand off work | `project-continuity` |
| Organize scattered files or restructure directories | `project-organization` |
| Maintain dependencies, runtimes, or toolchains | `project-maintenance` |
| Perform acceptance testing, code review, or performance, AI, or UX evaluation | `project-verification` |
| Review security, identity, authorization, or tenant boundaries | `project-security` |
| Maintain project facts, usage instructions, or documentation | `maintaining-project-docs` |
| Prepare a release, migration, or rollback | `project-release` |
| Respond to a production incident or active security impact | `project-incident-response` |

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
| `docs/tasks/<ID>.md` | Goal, completed work, verification, risks, and next step | For cross-session or unfinished work; this is the source of truth for dynamic state |
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

```powershell
# Windows PowerShell; run from the product project root and replace the task ID with the real one.
py -3 -B .ai-workflow/scripts/project_status.py --root . --task TEXT-001
py -3 -B .ai-workflow/scripts/project_status.py --root . --task TEXT-001 --format json --require-fresh
py -3 -B .ai-workflow/scripts/project_status.py --root . --task TEXT-001 --format markdown
py -3 -B .ai-workflow/scripts/project_status.py --root . --task TEXT-001 --check-view
```

On macOS or Linux, replace `py -3 -B` with `python3 -B`. The script uses only the Python 3.10+ standard library. Version `2.0.0` was tested on Windows with Python 3.11.9; other systems need verification in their own projects.

If no task record exists, create a real record from the template first; do not fabricate a snapshot. When several tasks exist, do not guess based on the “latest date.” After relevant files change, old verification becomes stale or unknown and cannot continue to be treated as passing. A missing or stale view makes `--check-view` return 1; a structural error returns 2. If Python is unavailable, manually check the same six items and state that they were not automatically verified.

`--task <ID>` selects from the active index. For a completed task removed from that index, provide its exact file path; the tool does not scan all history:

```powershell
py -3 -B .ai-workflow/scripts/project_status.py --root . --task-file docs/tasks/TEXT-001.md --check-view --require-fresh
```

This is not real-time monitoring or permanent memory. Reliable continuation depends on saving the necessary facts before every pause and rechecking code, configuration, and evidence in the new session.

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

After adding project-specific Skills, you can use `--allow-extra-skills`. It maintains entry points for only the 24 built-in Skills while preserving additional Skills, their proxies, and their lock records. Other tool entry points for additional Skills remain the project's responsibility; this option does not generate proxies for them automatically.

```powershell
py -3 -B .ai-workflow/scripts/sync_adapters.py --root . --allow-extra-skills --check --json
```

## 10. Customization and upgrades

- Put a project-specific Skill in `.agents/skills/<clear-unique-name>/SKILL.md` and state when it applies. Put detailed material in its references directory instead of filling `AGENTS.md` with a long manual.
- Let product code follow the actual technology stack. Do not move every directory or replace the test framework for the sake of the template.
- Keep a copy of the original template version. When upgrading, compare upstream changes and merge them with your own rules and Skills; do not download a new template over the entire product root.
- Before modifying vendored Superpowers content, check its source and license, record the actual patch in `.ai-workflow/third_party/superpowers/PATCHES.md`, and verify affected behavior. A version upgrade does not mean every previous behavior still holds.
- After project kickoff, the root README should introduce your product. If the template guide still needs to be retained, keep the necessary links in the existing development documentation instead of maintaining two conflicting project homepages.

## 11. Verification scope and what this template cannot guarantee

Targeted `2.0.1` verification in the current session host compared the same small feature under the old and revised rules. The old route read TDD, completion verification and method references; the revised route read only `AGENTS.md` and `project-development`, with 2/2 feature regression tests passing. A separate simple bug fix also loaded no Superpowers method, reproduced the failure before fixing it, and passed 3/3 tests. Five read-only routing scenarios covered conversation, Skill explanation, a small documentation edit, substantial design and production diagnosis; these are routing checks, not five end-to-end product tests. All 24 Skills passed UTF-8 format validation; the development workspace passed 11/11 adapter tests and 9/9 source-patch checks. The delivery's 26 adapters and 60 third-party files passed consistency checks. Billed tokens and other hosts' automatic discovery behavior were not measured.

The following are historical, limited `2.0.0` scenarios run with native subtasks and real temporary projects within the current session host, without calling the Codex CLI. Independent subtasks do not inherit the parent chat history, but they still share host rules, tools, and discoverable Skill directories. This is not fully isolated, cross-product certification, and those historical results alone do not establish that the `2.0.1` trigger boundaries pass runtime verification.

Limited scenarios and independent rechecks on 2026-09-18 produced these results:

- Helper tools: 56/56 regression tests passed, covering task selection, stale fingerprints, derived views, path boundaries, adapter conflicts, and rollback after write failures. This includes regressions added after testing exposed completed-task file lookup and Windows path-case alias issues.
- Small feature: 9/9 application-fixture tests passed, changing only the implementation and test files. Running the new tests against the original implementation detected the missing feature.
- A/B handoff: the continuation Agent received no parent chat history, recovered from persisted files, and completed the work with 5/5 tests passing. The candidate tool independently rechecked the final record's freshness and view consistency.
- Directory organization: approved document and code-module moves updated links and imports. The original entry-point output was unchanged, 1/1 test passed, and moved-file fingerprints matched.
- Additional scenarios covered planning without implementation, read-only recovery of ambiguous/stale tasks, diagnosis without repair, a single-link documentation fix, and a read-only tenant-boundary review. Actual file differences were checked; these scenarios did not expand their authorized scope.

Test projects, logs, scoring tools, and build history remain outside the template. The requested model setting for those historical scenarios was GPT-5.6 / high; the host's actual model version, randomness, and billed tokens were not independently verified. At that time, the general-knowledge scenario still loaded a general Skill; this helped motivate the `2.0.1` trigger correction and cannot be counted as a passing test of the new boundaries. No end-to-end certification was performed on other AI products, macOS/Linux, or production environments. Static adapter consistency is not proof of cross-tool runtime success.

No set of rules can guarantee that every model on every project will be error-free. Model capabilities, context, tool permissions, and product-specific tests still determine the outcome. High-risk work such as security changes, data migrations, and production releases requires the corresponding review and authorization. This template is a maintainable starting point, not a substitute for quality or security responsibility.

## 12. Sources and licenses

The foundational rules were researched with reference to [Misayhuiyi/Rules](https://github.com/Misayhuiyi/Rules). They independently restate principles for investigation, reuse, simple solutions, precise changes, environment adaptation, and verification, without carrying over personalized assumptions such as “there are no existing users.”

The 14 method Skills are based on the locked [Superpowers 6.3.0](https://github.com/obra/superpowers/tree/b36e0829c6d0140e93cfef2ca599b1b07d4a7797) with this project's on-demand routing patches; their bodies are not all unchanged upstream copies. Version, license, upstream provenance, and separately identified UI metadata are documented in the [source lock](.ai-workflow/SOURCES.lock.json), [third-party notices](.ai-workflow/THIRD_PARTY_NOTICES.md), and [patch record](.ai-workflow/third_party/superpowers/PATCHES.md). This project is not an official distribution of any of these AI tools.

The original workflow is released under the [MIT License](.ai-workflow/LICENSE); see [License Scope](.ai-workflow/LICENSE-SCOPE.md) for details. This does not automatically select a license for your product code, data, images, or product documentation. Project owners should choose their own project license.
