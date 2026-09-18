<!-- ai-workflow-task: {"schema_version":1,"id":"RAG-003","state":"active","owner":"integrator","worktree":null,"baseline":{"kind":"none","files":{"src/example.py":"absent"}},"scope":{"related_paths":["src/example.py","tests/test_example.py"],"excluded_paths":[]},"snapshot":{"goal":"具体目标","acceptance":["可核对结果"],"completed":[],"risks":["未验证项"]},"verification":{"status":"not_run","command":null,"evidence":null,"fingerprint":null},"next_step":{"summary":"一个精确动作","verify":"对应检查","stop_condition":"需要停止的条件"}} -->

本文件中的任务 ID、路径、目标与指纹是模板示例，使用时替换为真实值。首行 JSON 是动态正本。

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
