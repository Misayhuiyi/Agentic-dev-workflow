---
name: maintaining-project-docs
description: Use when a documentation-only fact review or edit is requested, or project interfaces, configuration, architecture, usage, operations, or important iteration facts change.
---

# 项目文档维护

先判断真实文档影响。纯文档审查或同步仍由本 Skill 负责，即使仓库存在未完成的实现计划；未经用户要求不转为开发。内部小改且行为、架构、配置、使用不变，可明确无需更新；单链接修复保持最小。只读审查只报告缺口。

1. 读取当前任务和相关事实，按[变更映射](references/change-to-docs.md)定位唯一权威源。
2. 在授权范围更新源。生成契约不能手改结果掩盖源缺陷；源是业务代码而仅授权文档时，报告所需开发事项，不自行改业务代码。
3. 按[文档事实](references/document-truth.md)区分当前实现、已批准计划、历史、假设、未知和未验证；引用真实验证证据。项目能力/里程碑变化同步事实入口，任务变化只维护原状态正本；人类快照从正本生成并检查。
4. 必要时使用[ADR](../../../.ai-workflow/templates/adr.md)、[重要迭代](../../../.ai-workflow/templates/iteration.md)、[运维记录](../../../.ai-workflow/templates/operations-record.md)。旧 ADR 保留背景，以 superseded/后继记录表达新决定。
5. 交接交 project-continuity，复用[任务状态](../../../.ai-workflow/templates/task-state.md)；未完成小任务也保留最小交接记录，不创建第二计划或另一份动态状态。公共索引由整合者维护，已完成任务退出活动列表但保留证据链接。

输出更新及原因、权威来源、检查结果和证据缺口；不编造 benchmark、日期、提交或部署事实，不把写文档当重新设计和实现授权。
