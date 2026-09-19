---
name: project-kickoff
description: Use when a project starts from an empty directory, an existing project first adopts the workflow, or its scope and first milestone are undefined.
---

# 项目建项与首次接入

只在建项或首次接入时使用；明确的小功能进入 project-development，普通知识问答直接回答。设计请求不授予实施权限。

1. 按[发现边界](references/discovery.md)核对实际目录、Shell、Git 或无 Git、已有实现/调用方/测试及文档，区别空项目与已有项目。
2. 提炼目标、非目标、验收与外部边界；已有用户答案和授权直接复用。许可来源、敏感数据、费用和部署权限未知时明确记录。
3. 对仍在初始文档阶段的项目，核对已有需求依据。若缺少影响目标、可行性或重要设计的调研材料，说明具体缺口及建议调查范围，先询问是否需要调研；获准才交 project-research。用户已明确要求调研则直接进入；拒绝或未回答时保留未知，继续不依赖它的已授权工作。已有材料足够或需求明确的小项目不强制调研。
4. 提出一个最小端到端里程碑。若关键假设必须实际运行才知道，且失败会改变方案或造成明显返工/成本，先提出有界可行性实验，获准交 project-verification；已有当前环境证据的成熟方案无需实验。调研候选结论经用户审核后才能进入设计/计划。仅有未决重要行为/架构选择时交 brainstorming，复杂实施才交 writing-plans；复用同一权威 spec/plan。
   业务模块在投入完整开发前明确使用者、真实场景、代表性样本、可观察验收及用户/指定验收人；未知就询问，不虚构业务口径。首个里程碑优先展示可用闭环以便人工及早纠偏，不等全项目写完才看效果。边界清楚的轻量接入仍留在本 Skill，不因建项自动加载方法。
5. 只有获准接入或实施后，才按需要建立[事实入口](../../../.ai-workflow/templates/project-context.md)、任务入口与[设计合同](../../../.ai-workflow/templates/spec.md)。只分析时零写入，不自行初始化 Git、选择技术栈或铺设基础设施。

多阶段业务项目需要明确阶段职责时才读[可裁剪交付闭环](../../../.ai-workflow/references/delivery-loop.md)；复用 spec 承载业务需求，不为 PRD 文件名再复制一套。MVP 只裁范围，不免基本质量。输出已知边界、待决定事实、首个可验收增量、验收和精确下一步；未验证命令如实标记。实施、提交和发布授权互不传递。
