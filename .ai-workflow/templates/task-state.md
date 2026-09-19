<!-- ai-workflow-task: {"schema_version":1,"id":"RAG-003","state":"active","owner":"integrator","worktree":null,"baseline":{"kind":"none","files":{"src/example.py":"absent"}},"scope":{"related_paths":["src/example.py","tests/test_example.py"],"excluded_paths":[]},"snapshot":{"goal":"具体目标","acceptance":["可核对结果"],"completed":[],"risks":["未验证项"]},"verification":{"status":"not_run","command":null,"evidence":null,"fingerprint":null},"human_acceptance":{"status":"pending","reason":"业务模块需要人工效果验收","reviewer":null,"reviewed_at":null,"evidence":null,"fingerprint":null,"criteria_sha256":null},"next_step":{"summary":"一个精确动作","verify":"对应检查","stop_condition":"需要停止的条件"}} -->

本文件中的任务 ID、路径、目标与指纹是模板示例，使用时替换为真实值。首行 JSON 是动态正本。

## 技术完成与人工接受

verification 只表示技术检查。业务模块未获得明确接受时保持 state=active，human_acceptance.status=pending；被退回或必需条件未闭合时 changes_requested。这两种情况都保留活动索引，next_step 指向人工检查或获准修正，不写整模块 done。

技术 pass 的完成依据必须填写非空 command 和 evidence：前者是实际检查命令，非命令式检查则写具体操作步骤；后者是实际结果摘要及可追溯证据位置。只填 pass、只记文件指纹、空字符串或空白都不能通过完成门槛。脚本不替你执行检查，也不能证明记录的真实性。

human_acceptance 固定字段为 status、reason、reviewer、reviewed_at、evidence、fingerprint、criteria_sha256。reason 填具体依据；pending 可暂用 null 表示未知。accepted 必须有真实验收人、时间、反馈来源、独立候选指纹与准则摘要，不能用 Agent 自评代替。纯内部/文案等确实无业务效果变化的任务可标 not_required 并说明理由，但同样要绑定准则摘要；不能用它豁免小型业务模块。

先从项目根运行 `py -3 -B .ai-workflow/scripts/project_status.py --root . --task <ID> --format json`，从 `snapshot.human_acceptance.current_criteria_sha256` 取得当前准则摘要；它绑定 goal、acceptance 及 scope。只在真实接受当前候选、或实际确认不适用时记录该摘要。accepted 的 fingerprint 与 verification.fingerprint 使用同一格式，但独立保存验收时的真实候选，不在重跑技术测试时自动替换。相关权威 spec、配置、数据/模型等文件也按需纳入 related_paths。

技术 pass/fresh、检查动作和证据非空，且人工 accepted/fresh（或有理由及当前摘要的 not_required/fresh）后才设 done。用 `py -3 -B .ai-workflow/scripts/project_status.py --root . --task <ID> --require-complete --format json` 检查：0 为记录满足完成条件，1 为未满足，2 为结构/读取错误；不自动修改状态或证明业务真的由人操作过。`--require-fresh` 仍只检查技术证据新鲜度，不表示技术通过或人工接受。非 Windows 环境将 `py -3` 换成实际 Python 3 命令。

旧记录缺 human_acceptance 仍可读取，但显示未记录/未知，不能通过完成门槛；恢复时据真实反馈补全，不自动迁移成 accepted 或 not_required。候选/准则变更使旧接受过期，保留原依据并复核受影响项。

## 可读快照

从项目根运行 Python 脚本 `.ai-workflow/scripts/project_status.py --root . --task <真实任务ID> --format markdown`，将输出的完整标记区放在此处。机器块更新后重新生成，`--check-view` 检查同步情况。不手工维护第二份进度，保留以下人工备注。

## 背景/决策依据

说明任务来源、批准依据和必要背景，不在正文复制可变状态字段。

## 详细证据

记录重要证据的位置和解释，不粘贴完整命令日志。

## 风险说明

补充风险的原因、影响和处置边界。

## 交接备注

保留跨会话需要但不适合放入短快照的说明。
