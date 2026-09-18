# Superpowers compatibility contract

Project authorization, `AGENTS.md`, current facts, and approved project documents take precedence over method Skills.

- Superpowers never grants permission to commit, push, open a PR, merge, deploy, delete data or worktrees, modify production, or use paid services.
- Preserve user and other-agent changes. Stop before an overlapping or destructive write whose target is not proven safe.
- Reuse the project's authoritative spec and plan; do not generate a second pair for the same task.
- Apply root task sizing before choosing methods. A clear, authorized, low-risk local change following an existing pattern needs implementation and verification, not an additional design approval or written plan. Unresolved product/interface/data/architecture decisions trigger brainstorming; once applicable, honor its approval gates.
- When the lifecycle route is already clear, no extra `using-superpowers` preamble is required. Its broad “always/1%” discovery language does not expand this project's task triggers; higher-priority host instructions still apply. Read only references needed for the current step; general knowledge answers need no project workflow.
- Simple work stays in the current task without an execution wrapper. Plan orchestration, parallel agents and independent formal review are chosen for actual dependency, risk and review needs, not because the tools exist.
- Multi-agent work, worktrees, local servers, browsers, and network access are conditional on host support, task fit, and authorization.
- Treat Bash examples as Bash; on Windows, translate only after confirming the actual shell rather than presenting them as native PowerShell.
- Resolve relative resources from the canonical Skill directory. `.agents/skills/` remains the complete source; adapters are generated proxies.
- The brainstorming visual companion is optional. Network access, remote resources, and telemetry are disabled by default unless explicitly enabled in scope.

The bundled runtime resources are from Superpowers 6.3.0 at commit `b36e0829c6d0140e93cfef2ca599b1b07d4a7797`: 46 upstream files plus 14 separately identified UI metadata files. Five unreferenced development-only files are omitted; see the source lock and patch record. Installed plugins with similar names do not replace these pinned project sources. Source updates require review of file additions/removals, executable modes, network endpoints, hooks, default writes and local patches.

On hosts without multi-agent or worktree capabilities, execute the same authorized plan serially. Non-Git projects remain non-Git unless explicitly authorized otherwise. Generated Claude proxies and Gemini imports are discovery adapters, not copies of method rules; static generation is not runtime acceptance. See the root README for the actual tested scope and limitations. Template-development tests and historical runtime experiments are kept outside this project foundation.
