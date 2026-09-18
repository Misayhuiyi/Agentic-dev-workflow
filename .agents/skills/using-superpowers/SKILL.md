---
name: using-superpowers
description: Use when explicitly configuring or troubleshooting this project's Superpowers method selection. Not for conversation startup, ordinary questions, status checks, or routine project tasks.
---

# Selecting Superpowers Methods

This optional guide supports an explicit method-selection or integration-troubleshooting request. It is not a session-start hook and is not required before answering, inspecting files, or using a project Skill. Mentioning a method in a question is not a request to execute it.

Use the root AGENTS.md routing first:

- Conversation and read-only explanation/status: answer or inspect only the relevant facts.
- Clear, low-risk local action: use the matching project Skill with applicable tests and fresh evidence.
- Substantial complexity, high risk, or a cause still unclear after focused inspection: select only the method needed for the current stage.
- Explicit request to apply a named method: read that local method within the authorized scope.

Load the chosen method directly; never load all methods or require this guide as a prerequisite. Method references named `superpowers:<name>` resolve to this project's sibling `../<name>/SKILL.md`. They do not select a global plugin copy.

Read a platform reference only when the selected method needs that host's tool mapping: [Codex](references/codex-tools.md), [Pi](references/pi-tools.md), [Antigravity](references/antigravity-tools.md), [Hermes](references/hermes-tools.md). Current host tools and higher-priority instructions remain authoritative. A duplicate global plugin has its own discovery rules; diagnose that separately instead of modifying its cache.
