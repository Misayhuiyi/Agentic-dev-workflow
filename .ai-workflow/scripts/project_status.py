#!/usr/bin/env python3
"""只读输出当前项目的最小恢复快照。"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    sys.dont_write_bytecode = True

from _taskstate import GitSnapshot, assess_freshness, parse_task_file, parse_task_index, resolve_task_path, select_task


VIEW_START = "<!-- ai-workflow-project-status:start -->"
VIEW_END = "<!-- ai-workflow-project-status:end -->"


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    environment = os.environ.copy()
    environment["GIT_OPTIONAL_LOCKS"] = "0"
    return subprocess.run(
        ["git", "-c", "core.fsmonitor=false", *args],
        cwd=root,
        shell=False,
        check=False,
        capture_output=True,
        timeout=10,
        env=environment,
    )


def _decode(value: bytes) -> str:
    return value.decode("utf-8", errors="surrogateescape").strip()


def git_snapshot(root: Path) -> GitSnapshot:
    try:
        discovered = _git(root, "rev-parse", "--show-toplevel")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return GitSnapshot(False, None, None, None, None, ())
    if discovered.returncode != 0:
        return GitSnapshot(False, None, None, None, None, ())
    git_root = Path(_decode(discovered.stdout)).resolve()
    branch_result = _git(root, "symbolic-ref", "--short", "-q", "HEAD")
    head_result = _git(root, "rev-parse", "HEAD")
    status_result = _git(root, "status", "--porcelain=v1", "-z", "--untracked-files=all")
    worktree_result = _git(root, "worktree", "list", "--porcelain")
    if status_result.returncode != 0:
        detail = _decode(status_result.stderr) or f"exit {status_result.returncode}"
        raise ValueError(f"git status failed: {detail}")
    head = _decode(head_result.stdout) if head_result.returncode == 0 else None
    branch = _decode(branch_result.stdout) if branch_result.returncode == 0 else None
    dirty: list[str] = []
    tokens = status_result.stdout.split(b"\x00")
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if not token:
            index += 1
            continue
        text = token.decode("utf-8", errors="surrogateescape")
        status = text[:2]
        relative = text[3:].replace("\\", "/") if len(text) >= 3 else ""
        if relative:
            dirty.append(relative)
        if ("R" in status or "C" in status) and index + 1 < len(tokens) and tokens[index + 1]:
            dirty.append(tokens[index + 1].decode("utf-8", errors="surrogateescape").replace("\\", "/"))
            index += 1
        index += 1
    worktree = root.resolve()
    if worktree_result.returncode == 0:
        for line in _decode(worktree_result.stdout).splitlines():
            if line.startswith("worktree "):
                candidate = Path(line[9:]).resolve()
                try:
                    root.resolve().relative_to(candidate)
                except ValueError:
                    continue
                worktree = candidate
                break
    return GitSnapshot(True, git_root, branch, head, worktree, tuple(sorted(set(dirty))))


def _content_without_view(data: bytes) -> bytes | None:
    try:
        lines = data.decode("utf-8").splitlines()
    except UnicodeDecodeError:
        return None
    starts = [index for index, line in enumerate(lines) if line == VIEW_START]
    ends = [index for index, line in enumerate(lines) if line == VIEW_END]
    marker_mentions = sum(line.count(VIEW_START) + line.count(VIEW_END) for line in lines)
    if marker_mentions:
        if len(starts) != 1 or len(ends) != 1 or starts[0] >= ends[0] or marker_mentions != 2:
            return None
        del lines[starts[0] : ends[0] + 1]
    while lines and not lines[-1].strip():
        lines.pop()
    return (("\n".join(lines) + "\n") if lines else "").encode("utf-8")


def _git_entry_mode(data: bytes, relative: str) -> str | None:
    records = [record for record in data.split(b"\x00") if record]
    if len(records) != 1 or b"\t" not in records[0]:
        return None
    metadata, raw_path = records[0].split(b"\t", 1)
    if raw_path.decode("utf-8", errors="surrogateescape").replace("\\", "/") != relative:
        return None
    fields = metadata.split()
    if len(fields) != 3 or fields[0] not in {b"100644", b"100755", b"120000"}:
        return None
    return fields[0].decode("ascii")


def _worktree_mode(path: Path) -> str | None:
    try:
        mode = path.lstat().st_mode
    except OSError:
        return None
    if stat.S_ISLNK(mode):
        return "120000"
    if not stat.S_ISREG(mode):
        return None
    return "100755" if mode & 0o111 else "100644"


def _is_view_only_dirty(root: Path, dirty_paths: list[str], relative: str) -> bool:
    if relative not in dirty_paths:
        return False
    try:
        current_path = root.joinpath(*relative.split("/"))
        current = current_path.read_bytes()
        baseline = _git(root, "show", f"HEAD:{relative}")
        staged = _git(root, "show", f":{relative}")
        baseline_entry = _git(root, "ls-tree", "-z", "HEAD", "--", relative)
        staged_entry = _git(root, "ls-files", "--stage", "-z", "--", relative)
    except (OSError, subprocess.SubprocessError):
        return False
    if any(result.returncode != 0 for result in (baseline, staged, baseline_entry, staged_entry)):
        return False
    contents = (_content_without_view(current), _content_without_view(staged.stdout), _content_without_view(baseline.stdout))
    modes = (_worktree_mode(current_path), _git_entry_mode(staged_entry.stdout, relative), _git_entry_mode(baseline_entry.stdout, relative))
    return all(content is not None for content in contents) and all(mode is not None for mode in modes) and contents[0] == contents[1] == contents[2] and modes[0] == modes[1] == modes[2]


def _base_result(root_selection: str, git: GitSnapshot, args: argparse.Namespace) -> dict[str, object]:
    return {
        "schema_version": 1,
        "kind": "project_status",
        "root": {"path": ".", "selection": root_selection},
        "git": {
            "available": git.available,
            "root": "." if git.available else None,
            "branch": git.branch,
            "head": git.head,
            "worktree": Path(git.worktree).name if git.worktree else None,
            "dirty_paths": list(git.dirty_paths),
        },
        "task_selection": {
            "status": "none",
            "requested_id": args.task,
            "requested_path": args.task_file,
            "requested_worktree": args.worktree,
            "selected_id": None,
            "candidates": [],
        },
        "freshness": {"status": "unknown", "reasons": ["no_task_selected"]},
        "snapshot": {"goal": None, "completed": [], "uncommitted": list(git.dirty_paths), "verification": None, "risks": [], "next_step": None},
        "warnings": [],
        "errors": [],
    }


def inspect_status(root: Path, args: argparse.Namespace, root_selection: str = "explicit") -> dict[str, object]:
    git = git_snapshot(root)
    result = _base_result(root_selection, git, args)
    index_path = root / "docs" / "tasks" / "index.md"
    selection_json = result["task_selection"]
    assert isinstance(selection_json, dict)
    index = parse_task_index(index_path, root) if index_path.exists() else None
    if args.task_file is not None:
        task_path = resolve_task_path(root, args.task_file)
        task = parse_task_file(task_path, root)
        if index is not None:
            matches = []
            for entry in index.tasks:
                try:
                    same_path = resolve_task_path(root, entry.path).samefile(task_path)
                except OSError:
                    same_path = False
                if entry.id == task.id or same_path:
                    matches.append((entry, same_path))
            if matches:
                if len(matches) != 1:
                    raise ValueError("task index and task file disagree")
                entry, same_path = matches[0]
                indexed = (entry.id, entry.state, entry.owner, entry.worktree)
                recorded = (task.id, task.state, task.owner, task.worktree)
                if not same_path or indexed != recorded:
                    raise ValueError("task index and task file disagree")
        selection_json["status"] = "selected"
        selection_json["candidates"] = [task.id]
    else:
        if index is None:
            return result
        selection = select_task(
            index,
            requested_id=args.task,
            requested_path=None,
            branch=git.branch,
            worktree=args.worktree,
            detected_worktree=str(git.worktree) if git.worktree else None,
        )
        selection_json["status"] = selection.status
        selection_json["candidates"] = list(selection.candidates)
        if selection.selected is None:
            result["freshness"] = {"status": "unknown", "reasons": [f"task_selection_{selection.status}"]}
            return result
        entry = selection.selected
        task = parse_task_file(root.joinpath(*entry.path.split("/")), root)
        if (task.id, task.state, task.owner, task.worktree) != (entry.id, entry.state, entry.owner, entry.worktree):
            raise ValueError("task index and task file disagree")
    freshness = assess_freshness(root, task, git)
    selection_json["selected_id"] = task.id
    result["freshness"] = {"status": freshness.status, "reasons": list(freshness.reasons)}
    result["snapshot"] = {
        "goal": task.snapshot["goal"],
        "completed": list(task.snapshot["completed"]),
        "uncommitted": list(git.dirty_paths),
        "verification": {
            "status": task.verification["status"],
            "command": task.verification["command"],
            "evidence": task.verification["evidence"],
            "freshness": freshness.status,
        },
        "risks": list(task.snapshot["risks"]),
        "next_step": dict(task.next_step),
    }
    return result


def _selection_note(result: dict[str, object]) -> str:
    selection = result["task_selection"]
    assert isinstance(selection, dict)
    candidates = selection["candidates"]
    if isinstance(candidates, list) and candidates:
        return f"未选择任务（候选：{'、'.join(str(item) for item in candidates)}）"
    requested = selection["requested_id"] or selection["requested_path"] or selection["requested_worktree"]
    if requested:
        return f"未选择任务（未找到：{requested}）"
    return "未选择任务"


def _uncommitted_text(result: dict[str, object]) -> str:
    snapshot = result["snapshot"]
    git = result["git"]
    assert isinstance(snapshot, dict) and isinstance(git, dict)
    uncommitted = snapshot["uncommitted"]
    if isinstance(uncommitted, list) and uncommitted:
        return "；".join(str(item) for item in uncommitted)
    return "无" if git["available"] else "无法判断（Git 不可用）"


def _markdown_uncommitted_text(result: dict[str, object], root: Path) -> str:
    snapshot = result["snapshot"]
    git = result["git"]
    selection = result["task_selection"]
    assert isinstance(snapshot, dict) and isinstance(git, dict) and isinstance(selection, dict)
    dirty = list(snapshot["uncommitted"]) if isinstance(snapshot["uncommitted"], list) else []
    if git["available"] and selection["selected_id"] is not None:
        relative = _selected_task_relative(root, result)
        if _is_view_only_dirty(root, dirty, relative):
            dirty = [path for path in dirty if path != relative]
    if not git["available"]:
        return "；".join(str(item) for item in dirty) if dirty else "无法判断（Git 不可用）"
    visible = "；".join(str(item) for item in dirty) if dirty else "无"
    return f"{visible}（派生展示排除经 HEAD、索引与工作树三方确认的纯派生视图区变化；原始 Git 状态请看 JSON 或 git status）"


def _next_text(result: dict[str, object]) -> str:
    snapshot = result["snapshot"]
    assert isinstance(snapshot, dict)
    next_step = snapshot["next_step"]
    if isinstance(next_step, dict):
        return f"{next_step['summary']}；检查：{next_step['verify']}；停止条件：{next_step['stop_condition']}"
    selection = result["task_selection"]
    assert isinstance(selection, dict)
    candidates = selection["candidates"]
    choice = "、".join(str(item) for item in candidates) if isinstance(candidates, list) and candidates else "task ID"
    return f"先明确 {choice}；检查：重新运行并确认唯一任务；停止条件：仍未选定唯一任务"


def _text(result: dict[str, object]) -> str:
    snapshot = result["snapshot"]
    assert isinstance(snapshot, dict)
    verification = snapshot["verification"]
    if isinstance(verification, dict):
        verification_text = f"{verification['status']} ({verification['freshness']})"
    else:
        verification_text = f"未知（{_selection_note(result)}）"
    selected = result["task_selection"]["selected_id"] is not None
    unknown = f"未知（{_selection_note(result)}）"
    values = (
        ("目标", snapshot["goal"] or _selection_note(result)),
        ("完成项", "；".join(snapshot["completed"]) if snapshot["completed"] else ("无" if selected else unknown)),
        ("未提交内容", _uncommitted_text(result)),
        ("验证", verification_text),
        ("风险", "；".join(snapshot["risks"]) if snapshot["risks"] else ("无" if selected else unknown)),
        ("下一步", _next_text(result)),
    )
    return "\n".join(f"{label}：{value}" for label, value in values) + "\n"


def _one_line(value: object, root: Path) -> str:
    if value is None:
        return "未记录"
    text = " ".join(str(value).split())
    resolved = root.resolve()
    for candidate in {str(root), root.as_posix(), str(resolved), resolved.as_posix()}:
        if candidate:
            text = text.replace(candidate, ".")
    text = re.sub(r'''(?i)(["'])(?:[a-z]:[\\/]|\\\\|/)[^"']*\1''', "[本机绝对路径]", text)
    text = re.sub(r"(?i)(?<![\w:/])(?:[a-z]:[\\/]|\\\\)[^\s；，,)\]}]+", "[本机绝对路径]", text)
    text = re.sub(r"(?<![\w:/])/(?:[^/\s；，,)\]}]+/)*[^/\s；，,)\]}]+", "[本机绝对路径]", text)
    return html.escape(text, quote=False)


def _markdown(result: dict[str, object], root: Path) -> str:
    snapshot = result["snapshot"]
    selection = result["task_selection"]
    freshness = result["freshness"]
    assert isinstance(snapshot, dict) and isinstance(selection, dict) and isinstance(freshness, dict)
    selected = selection["selected_id"] is not None
    note = _selection_note(result)
    completed = "；".join(snapshot["completed"]) if snapshot["completed"] else ("无" if selected else f"未知（{note}）")
    risks = "；".join(snapshot["risks"]) if snapshot["risks"] else ("无" if selected else f"未知（{note}）")
    verification = snapshot["verification"]
    if isinstance(verification, dict):
        reasons = freshness["reasons"]
        reason_text = "；".join(str(item) for item in reasons) if isinstance(reasons, list) and reasons else "无"
        verification_text = (
            f"状态：{verification['status']}；新鲜度：{verification['freshness']}；"
            f"原因：{reason_text}；命令：{verification['command'] if verification['command'] is not None else '未记录'}；"
            f"证据：{verification['evidence'] if verification['evidence'] is not None else '未记录'}"
        )
    else:
        reasons = freshness["reasons"]
        reason_text = "；".join(str(item) for item in reasons) if isinstance(reasons, list) and reasons else "无"
        verification_text = f"状态：未知；新鲜度：{freshness['status']}；原因：{reason_text}；命令：未记录；证据：未记录"
    task_id = selection["selected_id"] or ("、".join(str(item) for item in selection["candidates"]) if selection["candidates"] else "未选择")
    values = (
        ("目标", snapshot["goal"] or note),
        ("完成项", completed),
        ("未提交内容", _markdown_uncommitted_text(result, root)),
        ("验证", verification_text),
        ("风险", risks),
        ("下一步", _next_text(result)),
    )
    lines = [
        VIEW_START,
        "> 派生展示：供人和 Agent 快速浏览；任务首行机器块是唯一结构化正本，本区不是第二正本。",
        f"- 任务 ID：{_one_line(task_id, root)}",
    ]
    lines.extend(f"- {label}：{_one_line(value, root)}" for label, value in values)
    lines.append(VIEW_END)
    return "\n".join(lines) + "\n"


def _selected_task_relative(root: Path, result: dict[str, object]) -> str:
    selection = result["task_selection"]
    assert isinstance(selection, dict)
    selected_id = selection["selected_id"]
    if not isinstance(selected_id, str):
        raise ValueError("no selected task")
    requested_path = selection["requested_path"]
    if isinstance(requested_path, str):
        resolve_task_path(root, requested_path)
        return requested_path
    index = parse_task_index(root / "docs" / "tasks" / "index.md", root)
    matches = [entry.path for entry in index.tasks if entry.id == selected_id]
    if len(matches) != 1:
        raise ValueError("selected task is missing from task index")
    return matches[0]


def _check_view(root: Path, result: dict[str, object]) -> int:
    warnings = result["warnings"]
    errors = result["errors"]
    selection = result["task_selection"]
    assert isinstance(warnings, list) and isinstance(errors, list) and isinstance(selection, dict)
    if selection["selected_id"] is None:
        candidates = selection["candidates"]
        suffix = f"; candidates={','.join(str(item) for item in candidates)}" if isinstance(candidates, list) and candidates else ""
        warnings.append(f"task_view_unavailable: task_selection={selection['status']}{suffix}")
        return 1
    relative = _selected_task_relative(root, result)
    path = root.joinpath(*relative.split("/"))
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        errors.append(f"task_view_markers_broken:{relative}:invalid_utf8")
        return 2
    except OSError:
        errors.append(f"task_view_markers_broken:{relative}:unreadable")
        return 2
    start_count = text.count(VIEW_START)
    end_count = text.count(VIEW_END)
    if start_count == 0 and end_count == 0:
        warnings.append(f"task_view_missing:{relative}")
        return 1
    if start_count > 1 or end_count > 1:
        errors.append(f"task_view_markers_duplicate:{relative}:start={start_count},end={end_count}")
        return 2
    lines = text.splitlines()
    start_lines = [index for index, line in enumerate(lines) if line == VIEW_START]
    end_lines = [index for index, line in enumerate(lines) if line == VIEW_END]
    if start_count != 1 or end_count != 1 or len(start_lines) != 1 or len(end_lines) != 1 or start_lines[0] >= end_lines[0]:
        errors.append(f"task_view_markers_broken:{relative}")
        return 2
    actual = "\n".join(lines[start_lines[0] : end_lines[0] + 1]) + "\n"
    if actual != _markdown(result, root):
        warnings.append(f"task_view_stale:{relative}")
        return 1
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Read-only project continuity snapshot")
    parser.add_argument("--root", type=Path)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--task")
    group.add_argument("--task-file")
    parser.add_argument("--worktree")
    parser.add_argument("--format", choices=("text", "json", "markdown"), default="text")
    parser.add_argument("--require-fresh", action="store_true")
    parser.add_argument("--check-view", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    try:
        if args.root is not None:
            root = args.root.resolve(strict=True)
            selection = "explicit"
        else:
            cwd = Path.cwd().resolve()
            discovered = git_snapshot(cwd)
            if discovered.available and discovered.root is not None:
                root = discovered.root
                selection = "git_root"
            else:
                root = cwd
                selection = "cwd"
        if not root.is_dir():
            raise ValueError("root is not a directory")
        result = inspect_status(root, args, selection)
        view_status = _check_view(root, result) if args.check_view else 0
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        if args.format == "json":
            fallback_git = GitSnapshot(False, None, None, None, None, ())
            result = _base_result("explicit" if args.root else "cwd", fallback_git, args)
            result["errors"] = [str(exc)]
            print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        else:
            print(f"project_status: {exc}", file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    elif args.format == "markdown":
        sys.stdout.write(_markdown(result, root))
    else:
        sys.stdout.write(_text(result))
    if args.check_view and args.format != "json":
        for issue in [*result["errors"], *result["warnings"]]:
            print(f"project_status: {issue}", file=sys.stderr)
    if result["errors"]:
        return 2
    if view_status:
        return view_status
    task_status = result["task_selection"]["status"]
    freshness = result["freshness"]["status"]
    if args.require_fresh and (task_status in {"ambiguous", "not_found", "none"} or freshness in {"stale", "unknown"}):
        return 1
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    raise SystemExit(main())
