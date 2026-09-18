---
name: project-maintenance
description: Use when dependencies, runtimes, lockfiles, CI toolchains, deprecations, or a dependency vulnerability require assessment or migration.
---

# 依赖与工具链维护

用于维护已有依赖和兼容边界；新功能进入 development，正在影响生产的故障先 incident-response。评估请求不授权升级。

1. 查真实 manifest、锁文件、运行时、CI、生成物与调用方，建立受影响依赖图。
2. 按[升级评估](references/upgrade-assessment.md)核查版本、通告和兼容性，区分最小修复与推荐迁移；未知版本或离线资料明确标记，不能默认最新 major。
3. 按[弃用迁移](references/deprecation-migration.md)确定兼容窗口、顺序、回滚与停止条件。获准后同步依赖锁、运行时、CI 和有权威来源的生成物。
4. 实现变化交 test-driven-development，异常交 systematic-debugging。发现 CVE 本身不启动完整安全审查；只有暴露面、鉴权/租户/数据边界相关，或明确要求安全审查时交 project-security。
5. 将影响范围、变更和新鲜证据交 project-verification，使用/运维变化交 maintaining-project-docs。

输出当前/候选依据、风险分级、实际变更、验证和未解决项。提交与部署仍需独立授权。
