---
name: project-verification
description: Use when acceptance, independent code review, integration evaluation, performance or AI evaluation, UX, or accessibility assessment is requested. Routine completion checks stay in the current project Skill; status questions use relevant facts directly.
---

# 项目验收与证据

审查和验收不授权修复、改断言或发布。普通任务内的回归和完成核对留在原主路由，单纯状态查询直接读取事实，不因此加载本 Skill。先确认检查命令的实际环境和外部副作用。

以当前请求定义验收对象和比较目标。仓库中的其他 pending 实施计划只作背景；目标配置或基线不明时，列出精确缺口及只读补证动作，不把评测变成完成旧计划、申请提交推送或修复无关问题。

1. 按[审查清单](references/review-checklist.md)建立要求 → 实现 → 验证映射，界定任务候选、未提交及新增文件。
2. 按风险执行实际测试/构建/集成/用户路径检查，用[证据格式](../../../.ai-workflow/templates/verification.md)绑定命令、时间、环境、退出码和提交或有限工作区指纹。
3. 相关代码、测试、配置或依赖变化后，旧证据标 stale，重跑受影响检查。真实集成不可用时报告未运行；替身检查不能冒充集成通过。
4. AI/性能变化按[评测合同](references/ai-evaluation.md)固定数据、模型、配置、随机性和预算；输出时逐项显式列出评测合同字段，缺失则写未知或未执行，不用“固定条件”等概括替代。UX/可访问性区分静态审查、浏览器实测和辅助技术证据。
5. 简单验收在本 Skill 内检查与报告，不自动加载 Superpowers。复杂/高风险交付需要正式证据门槛或重要独立审查时才选 verification-before-completion 或 requesting-code-review；方法 Skill 或子 Agent 的完成声明不能替代实际证据。只读审查保持零写入。

输出验收覆盖、可定位发现、本任务结果、已有失败、未执行原因和剩余风险；自审明确标记。缺少必需证据时只能部分验证，不能宣布整个任务完成。
