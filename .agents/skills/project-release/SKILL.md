---
name: project-release
description: Use when release readiness, deployment preparation, data or index migration, rollback planning, or execution in an explicitly authorized environment is requested.
---

# 发布准备与执行

“检查能否上线”只授权检查。准备、部署、运行验证分别记录；日常开发完成不自动进入发布。

1. 确认精确候选/产物、未提交差异、环境、变更、证据和既有授权；按[就绪检查](references/readiness.md)评估缺口。
2. 数据/索引变化按[迁移恢复](references/migration-rollback.md)核查兼容、备份、恢复演练和停止条件。备份存在不等于可恢复；恢复未知阻止破坏性迁移。
3. 用[发布合同](../../../.ai-workflow/templates/release.md)记录准备结果；只检查请求到此返回，不写生产、不建资源。
4. 只有目标环境、版本和既有流水线操作已有明确授权时才执行。finishing-a-development-branch 不创造 commit/push/merge/deploy 权限。失败或停止条件触发时暂停相关操作，使用已授权恢复路径。
5. 执行后核对业务冒烟、指标和观察窗口，记录真实[运维事实](../../../.ai-workflow/templates/operations-record.md)。生产影响先交 project-incident-response，记录交 maintaining-project-docs。

输出候选、授权范围、准备/部署/运行验证各自状态、证据、阻塞与风险。未观测时不能宣布稳定运行。
