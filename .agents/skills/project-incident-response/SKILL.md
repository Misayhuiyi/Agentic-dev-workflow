---
name: project-incident-response
description: Use when a production disruption, severe service degradation, suspected data loss, or active security impact requires incident triage or recovery.
---

# 生产事故响应

事故先管理影响与恢复，再调试根因；普通非生产 Bug 返回 project-development 按复杂度选择调查方法，已确认根因时复用证据。本 Skill 不因紧急语气扩展环境、数据或操作授权。

1. 按[分级与角色](references/triage-and-severity.md)确定角色、严重性和授权边界。
2. 界定用户影响、范围、时间和数据/安全风险，分开事实、假设、未知。
3. 按[证据保护](references/evidence-preservation.md)记录最小脱敏时间线，保护复现所需证据。
4. 只执行已明确获准的止损/恢复，核对环境、版本、动作、停止条件；缺失时继续安全只读分级和下一决策点，不猜测回滚或清数据。
5. 通过业务路径、数据完整性及指标观察窗口确认稳定；不能仅凭进程存活宣布恢复。
6. 系统稳定且诊断获准后，将根因排查交 systematic-debugging；修复获准且根因明确后交 test-driven-development，结果交 project-verification，恢复发布交 project-release，复盘交 maintaining-project-docs。

使用[事故记录](../../../.ai-workflow/templates/incident.md)和[运维记录](../../../.ai-workflow/templates/operations-record.md)，输出当前影响、证据、获准动作、稳定状态和下一责任/决策点。事故管理不能替代根因、验证或发布证据。
