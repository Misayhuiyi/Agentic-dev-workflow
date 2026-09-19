---
name: project-continuity
description: Use when a session resumes existing work, changes tasks or worktrees, loses task context through compaction, pauses, or hands work over.
---

# 任务恢复与交接

只在确实续接已有任务、切换任务/工作树、压缩失忆、暂停或交接时恢复事实与控制权；新会话本身不触发，清晰的新请求使用其生命周期入口。不另起设计、计划或实施。按[恢复协议](references/recovery-protocol.md)执行七步，按[新鲜度](references/state-freshness.md)核对状态。

用户明确的 task ID、文件或工作树选择优先，并核对当前目录；显式历史查询可读取 done，但不自动恢复实施。未指定时只自动选择当前工作树/分支唯一匹配的 active，不能回退到其他分支唯一任务，也不能自动续接 done。无 Git 用用户指针或唯一可核实记录；歧义不按 mtime 猜测。

业务模块恢复时分别核对技术 verification 与 human_acceptance 的人类依据、候选和准则新鲜度。技术通过但人工 pending/changes_requested/unknown 的任务仍未完成；相关变更使旧接受失效，不能因旧 done 或历史通过跳过复核。待人工任务保持 active 和原索引指针。

恢复当前获准里程碑、依赖结论、预算/停止条件及未决业务确认；不能把历史总计划视为全部可执行。SDD progress 只作执行证据，先核对任务/完整计划路径与版本/工作树，再与唯一 task-state 协调，不凭 basename 日志接管当前任务。

输出六项短快照：目标、完成项、未提交内容、验证、风险、精确下一步。多任务待选时每个字段合并列出候选差异与未知；“精确下一步”说明等待选择后的核对动作及停止条件。随后用最后一行的单一问句请求选择，格式为“<候选 task ID> 还是 <候选 task ID>？”；问题之后不追加说明。六项字段都不得省略。只加载该下一步所需资料，再把控制权还给原已批准方法链。

[任务状态](../../../.ai-workflow/templates/task-state.md)首行 JSON 是动态状态的唯一结构化正本；人类快照由 project_status.py 生成并检查，正文保留背景、证据、风险与交接。未完成任务即使很小，暂停/交接前也在已有写入授权内维护最小记录；无写入授权则输出六项快照和建议路径，注明尚未持久化。不能从聊天推断已验证事实。

[活动索引](../../../.ai-workflow/templates/task-index.md)只存指针，由当前任务整合者显式更新；本 Skill 不自动更新公共索引，也不调用 brainstorming、writing-plans 或实现。
