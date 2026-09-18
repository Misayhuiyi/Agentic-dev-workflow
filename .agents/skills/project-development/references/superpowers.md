# 唯一方法链映射

本表只在非简单/高风险工作需要方法，或用户明确要求使用方法时读取。低风险局部任务留在生命周期 Skill 内完成适用测试、根因核对和新鲜证据检查，不加载本表中的方法。

| 可观察条件 | 方法及返回点 |
| --- | --- |
| 产品、接口、数据或架构存在未决设计选择 | brainstorming；设计批准后返回任务 |
| 已批准设计需要复杂多步实施 | writing-plans；复用同一 plan |
| 非简单或高风险功能/修复 | test-driven-development；仅覆盖当前获准实现 |
| 初步查证后根因仍不明、反复失败、跨组件或高风险调查 | systematic-debugging；根因确认后重新按修复复杂度选方法，仅诊断请求不授权修复 |
| 复杂或高风险交付需要正式完成证据检查 | verification-before-completion；普通状态回复及简单任务就地验证不触发 |
| 专门验收、重要独立审查或跨系统评测 | project-verification / requesting-code-review，按真实需求选用 |

简单任务直接在当前会话完成，不强制执行编排 Skill。已有多步计划需要编排时选一个：当前会话适合且获准委派时 subagent-driven-development；独立有界任务值得并行时 dispatching-parallel-agents；按书面计划分批串行时 executing-plans。不能虚构工具或 Agent 结果，有依赖/重叠写入不并行。

有限重试先证明错误可恢复并评估幂等，规定次数、总超时、退避及日志；认证失败或数据损坏不靠重试消失。普通非生产 Bug 由 project-development 保持范围与项目事实，按表中条件才进入 systematic-debugging；有可靠证据的根因直接复用，但症状或猜测不算证据。已有修复授权不因完成诊断而重新审批，仅实质改变范围/契约/数据时再确认。生产影响先 incident-response。工具不可用时说明限制，完成安全可行部分。

方法可以直接加载，无需先读 using-superpowers。嵌套方法同样检查当前阶段；`superpowers:<name>` 解析为本项目 `.agents/skills/<name>/SKILL.md`，不选择同名全局插件。

恢复只使用 project-continuity，不在本文件维护第二协议。
