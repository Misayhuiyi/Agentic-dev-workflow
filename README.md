# Agentic Dev Workflow

中文 | [English](README.en.md)

一套可以直接放在项目根目录的 AI 长期开发工作流基座。默认面向 Codex，同时提供通用规则、标准 Skill 目录和其他工具的轻量入口。

它解决的是“怎样持续、有条理地与 AI 开发”，不是替你选择框架或生成一套业务架构。小模块、小项目、已有产品和大型系统都可以采用：流程随**本次改动的风险与复杂度**变化，而不是按项目大小增加步骤。

- 普通对话、知识问答和只读解释：直接回答，涉及项目事实时只查相关文件。
- 简单且明确的低风险改动：由对应生命周期 Skill 指导修改和验证，不自动加载 Superpowers 方法。
- 复杂或有未决选择的工作：先明确设计，再用一份计划分阶段推进。
- 换会话或换 Agent：从项目文档、任务状态和真实工作区恢复，不依赖聊天记忆。
- 根目录散乱：先分类并给出移动方案，获准后整理目录、更新引用和验证。
- 控制上下文：长期规则保持简短，Skill 正文和详细参考只在需要时读取。

当前模板版本：`2.0.1`。包含 **10 个项目生命周期 Skill + 14 个 Superpowers 方法 Skill**，没有示例业务代码、验收样例项目或构建历史。

## 1. 三分钟开始

### 新项目

1. 在 GitHub 点击 **Use this template** 创建自己的仓库；也可以下载 ZIP，把解压后的内容（包括隐藏目录）复制到空项目根目录。
2. 从这个根目录打开 Codex 或其他具备项目文件访问能力的 AI 编程工具。
3. 发送下面的请求，替换方括号内容：

```text
先读取 AGENTS.md，按需使用项目内 Skills。
我要开发：[目标和面向的用户]。
第一个可验收结果：[一条可以实际演示的业务闭环]。
约束：[技术栈、运行环境、数据权限、时间等；未知项请先查明]。
请使用 project-kickoff 开始，先明确边界，不要铺设尚不需要的基础设施。
```

初次使用可先让 Agent 只读确认：项目规则在哪里、能否发现本地 24 个 Skills、有没有同名全局 Skill 或更高层规则冲突。**发现名称不等于已经执行或验证过 Skill。**

### 已有项目

不要直接覆盖现有项目。先在独立目录查看模板，再让 Agent 比较并合并 `AGENTS.md`、同名 Skills、工具入口和文档约定。已有合理路径、业务 README、测试体系和项目许可证优先保留。

```text
将这套工作流接入现有项目。先只读盘点，列出规则/Skills/文档冲突和最小合并方案。
保留现有实现、README、目录约定和未提交修改；未经确认不要覆盖同名文件。
```

不需要同时安装所有 AI 工具，也不需要为使用 Markdown 规则而安装 Python。只有下面的可选辅助脚本需要 Python。

## 2. 目录结构与作用

```text
项目根目录/
├── README.md                    中文使用说明；建项后改为你的业务项目首页
├── README.en.md                 英文使用说明
├── AGENTS.md                    唯一的基础规则与任务路由入口
├── CLAUDE.md                    Claude 的轻量规则入口
├── GEMINI.md                    Gemini 的轻量规则入口
├── .gitignore                   缓存、临时文件和常见本地环境文件的忽略规则
├── .gitattributes               跨平台文本及工作流指纹的 Git 处理约定
├── .agents/skills/              24 个完整 Skill 的唯一正本
│   └── <skill-name>/
│       ├── SKILL.md             触发条件和必要步骤
│       └── references/…         仅部分 Skill 需要的详细参考或辅助资源
├── .claude/skills/              转发到正本的轻量 Skill 入口，不维护第二套正文
├── .ai-workflow/
│   ├── ROUTING.md               生命周期与方法 Skill 的选择规则
│   ├── superpowers-compat.md    Superpowers 与本项目权限、轻重流程的衔接
│   ├── templates/              项目上下文、任务、设计、验证等文档模板
│   ├── scripts/                两个日常辅助命令及三个内部依赖模块
│   ├── third_party/            上游许可、版本、文件校验与补丁记录
│   ├── VERSION                 工作流版本
│   ├── SOURCES.lock.json        锁定的调研和第三方来源
│   ├── ADAPTERS.lock.json       受管适配文件的指纹，防止覆盖人工修改
│   ├── LICENSE                 本工作流原创部分的 MIT 许可
│   ├── LICENSE-SCOPE.md         许可适用范围
│   └── THIRD_PARTY_NOTICES.md   第三方来源声明
└── docs/
    └── README.md                项目文档导航及维护约定
```

没有预建 `src/`、`apps/`、数据库、容器或 CI。它们应由实际业务和技术栈决定。`references/`、`scripts/` 等 Skill 子目录只在确有用途时存在；上游必要资源不是示例业务。

部分 Superpowers 可选辅助资源需要 Git、Node.js、Bash 或宿主的多 Agent/浏览器能力；选用时再检查，不要求一次装齐。Bash 脚本不能直接当作 PowerShell 命令运行。缺少能力时使用受支持的串行/人工核对方式，并如实说明未执行部分。

本模板的开发测试、评测脚手架、历史日志和打包记录不随基座复制。**这不意味着业务项目可以不写测试**；功能与修复仍应补充适用测试并执行验证。

## 3. 日常怎么用

通常直接描述需求即可，Agent 根据规则选择入口；不需要背下所有 Skill 名称。支持显式 Skill 选择的工具也可以使用 `$project-development` 等语法，具体选择方式以宿主为准。

| 你要做的事 | 按需入口 |
| --- | --- |
| 普通对话、知识问答、只读解释或状态查询 | 直接回答；需要项目事实时只读相关文件，不自动加载方法 Skill |
| 从零建项、首次接入已有项目 | `project-kickoff` |
| 功能、重构、普通非生产 Bug、执行已批准计划 | `project-development` |
| 恢复任务、换会话、暂停与交接 | `project-continuity` |
| 整理散乱文件、调整目录结构 | `project-organization` |
| 依赖、运行时、工具链维护 | `project-maintenance` |
| 测试验收、代码审查、性能/AI/UX 评测 | `project-verification` |
| 安全审查、身份/权限/租户边界 | `project-security` |
| 项目事实、使用说明和文档维护 | `maintaining-project-docs` |
| 发布、迁移与回滚准备 | `project-release` |
| 生产故障或正在发生的安全影响 | `project-incident-response` |

### 小改动

```text
给现有函数增加一个可选参数，保留旧调用方式；只改相关实现和测试。
验收条件是：[具体边界行为]。请完成并运行现有验证。
```

目标、验收和边界清楚，且沿用现有模式的低风险局部任务，只走对应的生命周期 Skill，简述做法后实施与验证，不自动加载任何 Superpowers 方法。仍须执行适用的回归测试、查明故障根因，并用当前工作区的新鲜证据支持完成声明；这些基本要求不等于必须读取 TDD、调试或完成验证方法的全文。不强制新建 spec、计划、并行任务或迭代日志。

### 复杂工作

```text
实现批量导入和中断恢复，现有 API 必须兼容。
先查明现有调用方和数据约束，明确未决设计，再维护一份实施计划，分阶段验收。
已批准的决定不要反复询问；实质改变数据或对外契约时再确认。
```

未知故障先定位根因；有证据支持的根因可直接用于已授权修复。只有确有独立任务、稳定边界和宿主支持时才并行。提交、推送、部署、付费服务和破坏性操作需要对应授权，不能由“同意设计”推导出来。

## 4. 散乱目录怎么整理

```text
使用 project-organization 盘点当前项目。
识别散落代码、配置、参考资料、任务书和草稿，先只读给出原路径到目标路径的映射。
说明影响的导入、运行命令和文档链接、验证及回退方式；暂时不要移动文件。
```

确认方案后，再明确批准具体移动范围。Skill 会在执行前复核源文件和目标位置；源文件发生变化、目标已存在、链接越界或消费者不明确时停止，不盲目继续。

它不会按扩展名把所有 `.py` 丢进 `src/`，也不会把草稿当成已批准任务书。运行入口可原位保留；同名文档不覆盖；秘密配置只识别路径、不为归类读取值；未知文件和用户修改保持不动。获准移动代码时，需要同步引用并重新运行适用测试。

## 5. 文档怎样同时服务人和 Agent

详细约定见 [docs/README.md](docs/README.md)。采用项目原有路径；没有约定时再按下表创建，不一次性复制全部模板。

| 文档 | 负责记录什么 | 什么时候需要 |
| --- | --- | --- |
| 业务 README | 项目用途、启动方法、文档入口 | 建项后维护；不要让模板说明永久充当产品首页 |
| `docs/project-context.md` | 当前能力、技术栈、真实命令、模块地图、里程碑、已知限制 | 初次接入及项目级事实变化；保持简短 |
| `docs/tasks/index.md` | 活动任务 ID、负责人、工作树与任务文件指针 | 有需要持续跟踪的活动任务时 |
| `docs/tasks/<ID>.md` | 目标、完成项、验证、风险、下一步 | 跨会话或未完成任务；这是动态状态正本 |
| `docs/specs/`、`docs/plans/` | 已批准设计与唯一实施计划 | 需要书面设计或复杂步骤时 |
| `docs/adr/` | 长期架构决定、理由与后继决定 | 重要决策时，不记录普通流水账 |
| `docs/iterations/` | 重要迭代的历史总结、验证和遗留事项 | 有值得保留的迭代结果时 |
| `docs/operations/` | 发布、迁移、回滚、事故的实际记录 | 真实运维需要时 |

已完成的小改可只在回复中说明结果。未完成工作即使很小，暂停或交接前也应在已有写入授权内保存最小状态；只读任务则明确“尚未持久化”。已完成任务退出活动索引，但保留原记录与证据链接。

模板示例中的 `RAG-003`、`src/example.py` 等必须替换为真实标识，不能当作项目已存在的事实。

## 6. 换会话时怎样接着做

结束前：

```text
我要换会话。请更新任务 TEXT-001 的真实状态、验证证据、风险和精确下一步；
保留唯一任务记录与可读快照，不复制完整聊天。
```

新会话：

```text
继续任务 TEXT-001。先按 project-continuity 核对任务文件和实际工作区，
给出目标、已完成、未提交内容、验证、风险、精确下一步，再继续已批准范围。
```

任务文件首行 JSON 是唯一结构化状态；下面的人类可读快照由脚本生成。两者不是两份手工进度。脚本只读，不自动写回：让 Agent 在授权范围内更新标记区，保留人工背景和证据备注。

```powershell
# Windows PowerShell；在业务项目根运行，替换真实任务 ID。
py -3 -B .ai-workflow/scripts/project_status.py --root . --task TEXT-001
py -3 -B .ai-workflow/scripts/project_status.py --root . --task TEXT-001 --format json --require-fresh
py -3 -B .ai-workflow/scripts/project_status.py --root . --task TEXT-001 --format markdown
py -3 -B .ai-workflow/scripts/project_status.py --root . --task TEXT-001 --check-view
```

macOS / Linux 使用 `python3 -B` 替换 `py -3 -B`。脚本使用 Python 3.10+ 标准库；`2.0.0` 的实测环境为 Windows / Python 3.11.9，其他系统需在自己的项目验证。

没有任务记录时先按模板建立真实记录，不伪造快照。多任务不按“最新日期”猜选；相关文件改变后，旧验证变为陈旧或未知，不能继续当作通过。`--check-view` 缺失/过期返回 1，结构错误返回 2。没有 Python 可人工核对同样六项，并注明未自动验证。

`--task <ID>` 从活动索引选择；已完成并移出索引的任务，用明确文件路径读取，不扫描全部历史：

```powershell
py -3 -B .ai-workflow/scripts/project_status.py --root . --task-file docs/tasks/TEXT-001.md --check-view --require-fresh
```

这不是实时监控或永久记忆。可靠接续依赖每次暂停前保存必要事实，以及新会话对代码、配置和证据重新核对。

## 7. Skill 为什么是按需加载

`AGENTS.md` 只放长期约束、分级与入口；Skill 名称和描述用于发现；正文在使用时读取；引用文件只展开当前步骤需要的部分。先判断当前请求，再选择需要读取的内容：

| 当前请求 | 加载范围 |
| --- | --- |
| 普通对话、知识问答、只读解释或状态查询 | 不自动进入方法流程；涉及项目事实时只查相关文件 |
| 目标、验收、边界明确，沿用现有模式的低风险局部任务 | 一个对应的生命周期 Skill；不自动加载 Superpowers 方法 |
| 非简单、高风险、多步依赖或复杂未知故障 | 一个生命周期 Skill 负责范围，再按当前阶段读取必要的具体方法 |
| 明确要求使用某个方法 | 使用所指定的方法；只提到名称或询问其含义不算调用请求 |

方法读取与基本质量要求分开：简单任务也要进行适用测试、根因核查与证据验证；发现风险或复杂度升级后，才加入所需方法。新会话本身不触发 Superpowers，也不代表要恢复旧任务。

以下方法保留按需自动发现，适用时由生命周期主路由组合使用：

| 方法 | 用途 |
| --- | --- |
| `brainstorming`、`writing-plans` | 未决设计与复杂实施计划 |
| `test-driven-development`、`systematic-debugging` | 非简单或高风险功能/修复的测试设计，复杂未知故障的系统定位 |
| `verification-before-completion` | 非简单或高风险交付的验证关卡；简单任务在主路由内核对证据 |
| `requesting-code-review`、`receiving-code-review` | 需要深入或独立审查的工作及复杂审查意见 |
| `dispatching-parallel-agents`、`subagent-driven-development`、`executing-plans` | 有必要时编排独立工作或执行既有计划 |
| `using-git-worktrees`、`finishing-a-development-branch` | 需要时隔离工作和处理集成收尾 |
| `writing-skills` | 新建或实质改变 Skill 行为时进行场景验证 |
| `using-superpowers` | 方法选择或集成排错需要时读取的可选指南；不是会话启动入口 |

`2.0.1` 对 14 个方法的触发描述和正文入口加入项目适用边界，并移除 `using-superpowers` 的会话启动、回复前调用及“1% 可能性”强制链。具体补丁见 [PATCHES.md](.ai-workflow/third_party/superpowers/PATCHES.md)。本模板追求减少重复与无关读取，**不承诺固定 token 节省比例**。

## 8. AI 工具适配与实际边界

| 工具 | 本模板提供的入口 | 使用前注意 |
| --- | --- | --- |
| [Codex（默认）](https://learn.chatgpt.com/docs/customization/overview#skills) | `AGENTS.md` + `.agents/skills/` | 从项目根打开，确认本地发现结果 |
| Claude Code | `CLAUDE.md` + `.claude/skills/` 转发入口 | 正文仍来自 `.agents/skills/`；检查同名全局插件 |
| Gemini | `GEMINI.md` + 公共 Skill 目录 | 核对当前版本的规则导入和 Skill 加载支持 |
| [GitHub Copilot](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills) | `AGENTS.md` + 公共 Skill 目录 | IDE/CLI 和版本可能有差异；`gh` 不是 Copilot 验收 |
| [Cursor](https://prod.cursor.com/docs/skills) | `AGENTS.md` + 公共 Skill 目录 | 确认当前项目入口和 Skill 支持，不以文件存在代替实测 |
| [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md) | 公共规则和 Skill 目录 | 取决于实际版本/preset 是否启用规则加载、文件 Skill 提供与消费能力；需实测 |

其他工具若能读取项目规则及 Markdown Skill，也可以显式指定这些文件。普通聊天界面若没有文件、终端和写入能力，只能讨论或审查，不能真正操作本地项目。本模板不会替宿主增加工具或权限。

不要为同一个规则分别维护多套全文；Claude/Gemini 入口只转发正本。DeepSeek Harness 不额外创建可能抢占公共入口的 `.dsh/skills/`。

项目内方法与全局安装的同名 Superpowers 插件是独立来源。此模板的补丁只作用于 `.agents/skills/` 正本及其适配入口，不会修改全局插件；方法间引用也应继续读取项目正本。当前会话已经注入的 Skill 清单不保证随文件修改即时刷新，更新后应在宿主支持的重新发现或新会话中核对来源。若宿主仍强制加载独立插件，应检查其配置和更高层规则；模板不能承诺跨宿主完全禁止加载。

## 9. 两个辅助脚本

### `project_status.py`：恢复状态

作用和用法见第 6 节。内部依赖 `_taskstate.py`、`_workflowlib.py`；不要只复制入口文件。Git 可选，缺少 Git 不会自动初始化仓库，也不能将“未知未提交状态”说成干净。

### `sync_adapters.py`：维护工具入口

修改规则或内置 Skill 后，先检查生成计划，再决定是否写入。默认 dry-run；人工改动导致冲突时保留原文件，不强制覆盖。

```powershell
py -3 -B .ai-workflow/scripts/sync_adapters.py --root . --json
py -3 -B .ai-workflow/scripts/sync_adapters.py --root . --check --json
py -3 -B .ai-workflow/scripts/sync_adapters.py --root . --apply --json
```

POSIX 同样用 `python3 -B`。内部依赖 `_skillmeta.py`、`_workflowlib.py` 和 `ADAPTERS.lock.json`；适配检查只证明生成文件一致，不证明某款 AI 已成功执行工作流。

添加项目专用 Skill 后，可以使用 `--allow-extra-skills`：只维护内置 24 个 Skill 的入口，保留额外 Skill、代理与其锁记录。额外 Skill 的其他工具入口由项目自己维护，此参数不会自动为它们生成代理。

```powershell
py -3 -B .ai-workflow/scripts/sync_adapters.py --root . --allow-extra-skills --check --json
```

## 10. 定制与升级

- 项目专用 Skill 放在 `.agents/skills/<清晰唯一的名称>/SKILL.md`，写明适用条件；详细资料放引用目录，不把大段手册塞进 `AGENTS.md`。
- 业务代码遵循实际技术栈，不为了模板移动所有目录或更换测试框架。
- 保留一份原始模板版本。升级时比较上游变化，再合并自己的规则和 Skill；不要下载新模板覆盖整个业务根目录。
- 修改 vendored Superpowers 前核对来源和许可，在 `.ai-workflow/third_party/superpowers/PATCHES.md` 留下实际补丁说明，并验证受影响行为。升级版本不等于所有旧行为仍然成立。
- 根目录 README 建项后应介绍你的产品。仍需保留模板用法时，可在既有开发文档中维护必要链接，避免两个相互矛盾的项目首页。

## 11. 验证范围与不能保证的事情

`2.0.1` 的本轮定向验证：在当前会话宿主中，对同一个小功能分别使用修复前后的规则。旧规则读取 TDD、完成验证及方法参考；新规则只读取 `AGENTS.md` 和 `project-development`，实际功能回归 2/2 通过。另一个简单 Bug 修复同样未读取 Superpowers，先复现失败再修复，3/3 通过。五类只读路由情景检查覆盖普通问答、Skill 解释、文档小改、复杂设计和生产诊断；这些是路由检查，不能冒充五个真实业务项目的端到端测试。24 个 Skill 通过 UTF-8 格式检查，开发工作区的适配测试 11/11、来源补丁校验测试 9/9 通过；交付物的 26 个适配入口与 60 个第三方文件校验一致。未测账单 token 或其他宿主自动发现行为。

以下是 `2.0.0` 在当前会话宿主内使用原生子任务和真实临时项目得到的历史有限样例，未调用 Codex CLI。独立子任务不继承父聊天历史，但仍共享宿主规则、工具和可发现的 Skill 目录；这不是完全隔离的跨产品认证，也不能直接证明 `2.0.1` 的触发边界已通过运行验证。

2026-09-18 的有限样例与独立复核结果：

- 辅助工具：56/56 项回归通过，覆盖任务选择、指纹陈旧、派生视图、路径边界、适配冲突及写入失败回退；包含实测发现后补上的完成任务文件查询和 Windows 路径大小写别名回归。
- 小功能：9/9 项业务样例测试通过，只改实现和测试两个文件；以原实现运行新增测试能检出缺失功能。
- A/B 交接：不传父聊天给接续 Agent，从持久文件恢复并完成后 5/5 通过；最终记录的 fresh 和视图一致性由候选工具再次核验。
- 目录整理：批准后移动文档和代码模块，更新链接/导入；原入口输出不变，1/1 项测试通过，移动内容指纹一致。
- 另外检查了复杂任务只规划、歧义/陈旧任务只读恢复、仅诊断不修复、单链接文档修改和租户边界只读审查；核对实际文件差异，未扩大这些样例的授权范围。

测试项目、日志、评分工具和构建历史留在模板之外。上述历史样例的模型请求为 GPT-5.6 / high，宿主实际模型版本、随机性和账单 token 未独立核实。当时的普通知识问答仍额外读取了通用 Skill；这是 `2.0.1` 修正触发边界的依据，不能将旧样例算作新边界通过。未执行其他 AI 产品、macOS/Linux 或生产环境的端到端认证；静态适配一致不代表跨工具实测通过。

不存在一套规则能保证任意模型、任意项目永不出错。模型能力、上下文、工具权限和具体业务测试仍决定效果；安全、数据迁移、生产发布等高风险工作需要对应审查和授权。本模板是可维护的起点，不是质量或安全责任的替代品。

## 12. 来源与许可

基础规则调研参考 [Misayhuiyi/Rules](https://github.com/Misayhuiyi/Rules)，以独立表述提炼查证、复用、简单方案、精确修改、环境适配与验证原则；不照搬“没有老用户”等个人化前提。

14 个方法 Skill 基于锁定的 [Superpowers 6.3.0](https://github.com/obra/superpowers/tree/b36e0829c6d0140e93cfef2ca599b1b07d4a7797)，带有本项目的按需路由补丁，并非全部上游原样正文。版本、许可、上游来源和单独标识的 UI 元数据见 [来源锁](.ai-workflow/SOURCES.lock.json)、[第三方声明](.ai-workflow/THIRD_PARTY_NOTICES.md) 与 [补丁记录](.ai-workflow/third_party/superpowers/PATCHES.md)。本项目不是这些 AI 工具的官方发行包。

原创工作流采用 [MIT](.ai-workflow/LICENSE)，具体见 [许可范围](.ai-workflow/LICENSE-SCOPE.md)。这不会自动替你的业务代码、数据、图片或产品文档选择许可证；项目所有者应自行决定项目许可。
