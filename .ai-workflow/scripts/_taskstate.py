"""任务索引、任务状态与新鲜度的严格解析。"""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from _workflowlib import resolve_under


_ID = re.compile(r"^[A-Z][A-Z0-9-]{1,31}$")
_SHA = re.compile(r"^[0-9a-f]{64}$")
_HEAD = re.compile(r"^[0-9a-f]{40}$")
_STATES = {"active", "blocked", "paused", "done"}
_VERIFICATION = {"pass", "fail", "not_run", "stale"}
_HUMAN_ACCEPTANCE = {"pending", "changes_requested", "accepted", "not_required"}


@dataclass(frozen=True)
class TaskIndexEntry:
    id: str
    path: str
    state: str
    worktree: str | None
    owner: str


@dataclass(frozen=True)
class TaskIndex:
    path: Path
    tasks: tuple[TaskIndexEntry, ...]


@dataclass(frozen=True)
class TaskRecord:
    path: Path
    id: str
    state: str
    owner: str
    worktree: str | None
    baseline: dict[str, object]
    scope: dict[str, tuple[str, ...]]
    snapshot: dict[str, object]
    verification: dict[str, object]
    next_step: dict[str, str]
    human_acceptance: dict[str, object] | None = None


@dataclass(frozen=True)
class TaskSelection:
    status: str
    selected: TaskIndexEntry | None
    candidates: tuple[str, ...]


@dataclass(frozen=True)
class GitSnapshot:
    available: bool
    root: Path | None
    branch: str | None
    head: str | None
    worktree: Path | None
    dirty_paths: tuple[str, ...]


@dataclass(frozen=True)
class Freshness:
    status: str
    reasons: tuple[str, ...]


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _relative(value: object) -> str:
    if not isinstance(value, str) or not value or "\x00" in value or "\\" in value:
        raise ValueError("path must be a non-empty POSIX relative path")
    candidate = PurePosixPath(value)
    if candidate.is_absolute() or any(part in {"", ".", ".."} for part in candidate.parts):
        raise ValueError(f"unsafe task path: {value!r}")
    if candidate.as_posix() != value:
        raise ValueError(f"non-canonical task path: {value!r}")
    return value


def _under(root: Path, relative: str) -> Path:
    root_real = root.resolve(strict=True)
    target = root_real.joinpath(*PurePosixPath(relative).parts)
    resolve_under(root_real, relative)
    return target


def resolve_task_path(root: Path, relative: str) -> Path:
    """Resolve one canonical project-relative task path without escaping root."""
    return _under(Path(root), _relative(relative))


def _machine_payload(path: Path, root: Path, prefix: str) -> dict[str, object]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise ValueError(f"cannot read task file: {path.name}") from exc
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"invalid UTF-8: {path.name}") from exc
    lines = text.splitlines()
    first_index = next((index for index, line in enumerate(lines) if line.strip()), None)
    if first_index is None:
        raise ValueError("missing machine block")
    line = lines[first_index].strip()
    marker = f"<!-- {prefix}: "
    if len(line.encode("utf-8")) > 16 * 1024 or not line.startswith(marker) or not line.endswith(" -->"):
        raise ValueError("machine block must be one complete first nonblank line")
    if any(marker in later for later in lines[first_index + 1 :]):
        raise ValueError("duplicate machine block")
    encoded = line[len(marker) : -4]
    try:
        payload = json.loads(encoded, object_pairs_hook=_pairs)
    except json.JSONDecodeError as exc:
        raise ValueError("invalid machine block JSON") from exc
    if not isinstance(payload, dict):
        raise ValueError("machine block payload must be an object")
    try:
        path.resolve(strict=True).relative_to(root.resolve(strict=True))
    except ValueError as exc:
        raise ValueError("task file is outside root") from exc
    return payload


def _exact(payload: dict[str, object], fields: set[str], kind: str) -> None:
    if set(payload) != fields:
        raise ValueError(f"{kind} fields do not match schema")


def parse_task_index(path: Path, root: Path) -> TaskIndex:
    payload = _machine_payload(Path(path), Path(root), "ai-workflow-task-index")
    _exact(payload, {"schema_version", "tasks"}, "task index")
    if type(payload["schema_version"]) is not int or payload["schema_version"] != 1 or not isinstance(payload["tasks"], list):
        raise ValueError("invalid task index schema")
    entries: list[TaskIndexEntry] = []
    ids: set[str] = set()
    paths: set[str] = set()
    for raw in payload["tasks"]:
        if not isinstance(raw, dict):
            raise ValueError("task index entry must be an object")
        _exact(raw, {"id", "path", "state", "worktree", "owner"}, "task index entry")
        task_id = raw["id"]
        if not isinstance(task_id, str) or not _ID.fullmatch(task_id) or task_id in ids:
            raise ValueError("invalid or duplicate task id")
        relative = _relative(raw["path"])
        _under(Path(root), relative)
        if relative in paths:
            raise ValueError("duplicate task path")
        state = raw["state"]
        owner = raw["owner"]
        worktree = raw["worktree"]
        if not isinstance(state, str) or state not in _STATES or not isinstance(owner, str) or not owner.strip():
            raise ValueError("invalid task index state or owner")
        if worktree is not None and (not isinstance(worktree, str) or not worktree.strip() or "\x00" in worktree):
            raise ValueError("invalid worktree")
        ids.add(task_id)
        paths.add(relative)
        entries.append(TaskIndexEntry(task_id, relative, state, worktree, owner))
    return TaskIndex(Path(path), tuple(entries))


def _hash_map(value: object, *, label: str) -> dict[str, str]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    result: dict[str, str] = {}
    for raw_path, raw_hash in value.items():
        path = _relative(raw_path)
        if not isinstance(raw_hash, str) or (raw_hash != "absent" and not _SHA.fullmatch(raw_hash)):
            raise ValueError(f"invalid fingerprint hash for {path}")
        result[path] = raw_hash
    return result


def _validate_fingerprint(fingerprint: object, related: tuple[str, ...], label: str) -> None:
    if not isinstance(fingerprint, dict):
        raise ValueError(f"{label} fingerprint is required")
    fingerprint_kind = fingerprint.get("kind")
    if fingerprint_kind == "git":
        _exact(fingerprint, {"kind", "head", "files"}, "git fingerprint")
        if not isinstance(fingerprint["head"], str) or not _HEAD.fullmatch(fingerprint["head"]):
            raise ValueError("invalid fingerprint head")
        samples = _hash_map(fingerprint["files"], label="fingerprint files")
    elif fingerprint_kind == "files":
        _exact(fingerprint, {"kind", "entries"}, "file fingerprint")
        samples = _hash_map(fingerprint["entries"], label="fingerprint entries")
    else:
        raise ValueError("invalid fingerprint kind")
    if set(samples) != set(related):
        raise ValueError(f"{label} fingerprint must sample every related path exactly")


def _parse_human_acceptance(value: object, related: tuple[str, ...]) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError("invalid human_acceptance")
    _exact(value, {"status", "reason", "reviewer", "reviewed_at", "evidence", "fingerprint", "criteria_sha256"}, "human_acceptance")
    if not isinstance(value["status"], str) or value["status"] not in _HUMAN_ACCEPTANCE:
        raise ValueError("invalid human_acceptance status")
    if not isinstance(value["reason"], str) or not value["reason"].strip():
        raise ValueError("human_acceptance reason is required")
    accepted = value["status"] == "accepted"
    for key in ("reviewer", "reviewed_at", "evidence"):
        field = value[key]
        if (accepted and field is None) or (field is not None and (not isinstance(field, str) or not field.strip())):
            raise ValueError(f"human_acceptance {key} must be a non-empty string" + ("" if accepted else " or null"))
    criteria = value["criteria_sha256"]
    if (accepted and criteria is None) or (criteria is not None and (not isinstance(criteria, str) or not _SHA.fullmatch(criteria))):
        raise ValueError("invalid human_acceptance criteria_sha256")
    if accepted or value["fingerprint"] is not None:
        _validate_fingerprint(value["fingerprint"], related, "human_acceptance")
    return value


def parse_task_file(path: Path, root: Path) -> TaskRecord:
    payload = _machine_payload(Path(path), Path(root), "ai-workflow-task")
    fields = {"schema_version", "id", "state", "owner", "worktree", "baseline", "scope", "snapshot", "verification", "next_step"}
    if "human_acceptance" in payload:
        fields.add("human_acceptance")
    _exact(payload, fields, "task")
    if type(payload["schema_version"]) is not int or payload["schema_version"] != 1 or not isinstance(payload["id"], str) or not _ID.fullmatch(payload["id"]):
        raise ValueError("invalid task identity")
    if not isinstance(payload["state"], str) or payload["state"] not in _STATES or not isinstance(payload["owner"], str) or not payload["owner"].strip():
        raise ValueError("invalid task state or owner")
    worktree = payload["worktree"]
    if worktree is not None and (not isinstance(worktree, str) or not worktree.strip() or "\x00" in worktree):
        raise ValueError("invalid worktree")
    baseline = payload["baseline"]
    if not isinstance(baseline, dict) or not isinstance(baseline.get("kind"), str) or baseline.get("kind") not in {"git", "none"}:
        raise ValueError("invalid baseline")
    if baseline["kind"] == "git":
        _exact(baseline, {"kind", "head"}, "git baseline")
        if not isinstance(baseline["head"], str) or not _HEAD.fullmatch(baseline["head"]):
            raise ValueError("invalid git baseline head")
    else:
        _exact(baseline, {"kind", "files"}, "file baseline")
        baseline = {"kind": "none", "files": _hash_map(baseline["files"], label="baseline files")}
        if not baseline["files"]:
            raise ValueError("non-git baseline must contain files")
    scope = payload["scope"]
    if not isinstance(scope, dict):
        raise ValueError("invalid task scope")
    _exact(scope, {"related_paths", "excluded_paths"}, "scope")
    related = tuple(_relative(item) for item in scope["related_paths"]) if isinstance(scope["related_paths"], list) else ()
    excluded = tuple(_relative(item) for item in scope["excluded_paths"]) if isinstance(scope["excluded_paths"], list) else ()
    if not related or len(set(related)) != len(related) or set(related) & set(excluded):
        raise ValueError("related paths must be non-empty, unique, and not excluded")
    for relative in related + excluded:
        _under(Path(root), relative)
    snapshot = payload["snapshot"]
    if not isinstance(snapshot, dict):
        raise ValueError("invalid snapshot")
    _exact(snapshot, {"goal", "acceptance", "completed", "risks"}, "snapshot")
    if not isinstance(snapshot["goal"], str) or not snapshot["goal"].strip():
        raise ValueError("snapshot goal is required")
    for key in ("acceptance", "completed", "risks"):
        if not isinstance(snapshot[key], list) or not all(isinstance(item, str) for item in snapshot[key]):
            raise ValueError(f"snapshot {key} must contain strings")
    verification = payload["verification"]
    if not isinstance(verification, dict):
        raise ValueError("invalid verification")
    _exact(verification, {"status", "command", "evidence", "fingerprint"}, "verification")
    if not isinstance(verification["status"], str) or verification["status"] not in _VERIFICATION:
        raise ValueError("invalid verification status")
    for key in ("command", "evidence"):
        if verification[key] is not None and not isinstance(verification[key], str):
            raise ValueError(f"verification {key} must be a string or null")
    fingerprint = verification["fingerprint"]
    if verification["status"] == "not_run":
        if fingerprint is not None:
            raise ValueError("not_run verification cannot have a fingerprint")
    else:
        _validate_fingerprint(fingerprint, related, "verification")
    human_acceptance = _parse_human_acceptance(payload["human_acceptance"], related) if "human_acceptance" in payload else None
    next_step = payload["next_step"]
    if not isinstance(next_step, dict):
        raise ValueError("invalid next_step")
    _exact(next_step, {"summary", "verify", "stop_condition"}, "next_step")
    if any(not isinstance(next_step[key], str) or not next_step[key].strip() for key in next_step):
        raise ValueError("next_step values are required")
    return TaskRecord(Path(path), payload["id"], payload["state"], payload["owner"], worktree, baseline, {"related_paths": related, "excluded_paths": excluded}, snapshot, verification, next_step, human_acceptance)


def select_task(
    index: TaskIndex,
    *,
    requested_id: str | None,
    requested_path: str | None,
    branch: str | None,
    worktree: str | None,
    detected_worktree: str | None = None,
) -> TaskSelection:
    def result(matches: list[TaskIndexEntry], *, explicit: bool = False) -> TaskSelection:
        if not matches:
            return TaskSelection("not_found" if explicit else "none", None, ())
        if len(matches) > 1:
            return TaskSelection("ambiguous", None, tuple(sorted(item.id for item in matches)))
        return TaskSelection("selected", matches[0], (matches[0].id,))

    def matches_worktree(binding: str | None, selector: str) -> bool:
        if not binding:
            return False
        recorded = binding.replace("\\", "/").rstrip("/")
        normalized = selector.replace("\\", "/").rstrip("/")
        if os.name == "nt" and Path(recorded).is_absolute() and Path(normalized).is_absolute():
            return os.path.normcase(recorded) == os.path.normcase(normalized)
        # 兼容单段工作树名；两个带目录的路径不能仅因末段相同而匹配。
        return recorded == normalized or (
            "/" not in recorded and recorded == PurePosixPath(normalized).name
        ) or (
            "/" not in normalized and normalized == PurePosixPath(recorded).name
        )

    if requested_id is not None:
        return result([item for item in index.tasks if item.id == requested_id], explicit=True)
    if requested_path is not None:
        try:
            requested_path = _relative(requested_path)
        except ValueError:
            return TaskSelection("not_found", None, ())
        return result([item for item in index.tasks if item.path == requested_path], explicit=True)
    if worktree is not None:
        if not worktree:
            return TaskSelection("not_found", None, ())
        matches = [item for item in index.tasks if matches_worktree(item.worktree, worktree)]
        return result(matches, explicit=True)
    active = [item for item in index.tasks if item.state == "active"]
    if detected_worktree:
        matches = [item for item in active if matches_worktree(item.worktree, detected_worktree)]
        if matches:
            return result(matches)
    if branch:
        return result([item for item in active if item.worktree == branch])
    # 已核实工作树却没有匹配时不得跳到其他任务；无身份信息保留旧兼容行为。
    return result([] if detected_worktree else active)


def _sample(root: Path, relative: str) -> tuple[str | None, str | None]:
    try:
        target = _under(root, relative)
        if not target.exists():
            return "absent", None
        if target.is_symlink() or not target.is_file():
            return None, f"{relative}:not_regular"
        digest = hashlib.sha256()
        with target.open("rb") as handle:
            while chunk := handle.read(1024 * 1024):
                digest.update(chunk)
        return digest.hexdigest(), None
    except (OSError, ValueError):
        return None, f"{relative}:unreadable"


def assess_freshness(root: Path, task: TaskRecord, git: GitSnapshot) -> Freshness:
    verification = task.verification
    fingerprint = verification["fingerprint"]
    if verification["status"] == "stale":
        return Freshness("stale", ("verification_marked_stale",))
    if verification["status"] == "not_run" or fingerprint is None:
        return Freshness("unknown", ("verification_not_run",))
    return _assess_fingerprint(root, task.scope["related_paths"], fingerprint, git)


def criteria_sha256(task: TaskRecord) -> str:
    """以规范化 UTF-8 JSON 对目标、验收条件和有序任务范围计算摘要。"""
    criteria = {"goal": task.snapshot["goal"], "acceptance": task.snapshot["acceptance"], "scope": task.scope}
    encoded = json.dumps(criteria, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def assess_human_acceptance(root: Path, task: TaskRecord, git: GitSnapshot) -> Freshness:
    human = task.human_acceptance
    if human is None:
        return Freshness("unknown", ("human_acceptance_unrecorded",))
    if human["criteria_sha256"] is None:
        return Freshness("unknown", ("human_acceptance_criteria_unrecorded",))
    if human["criteria_sha256"] != criteria_sha256(task):
        return Freshness("stale", ("human_acceptance_criteria_changed",))
    if human["status"] == "not_required":
        return Freshness("fresh", ())
    if human["fingerprint"] is None:
        return Freshness("unknown", ("human_acceptance_candidate_unrecorded",))
    # 技术检查重跑时，人工审阅过的候选仍保留独立指纹。
    return _assess_fingerprint(root, task.scope["related_paths"], human["fingerprint"], git)


def _assess_fingerprint(root: Path, related: tuple[str, ...], fingerprint: dict[str, object], git: GitSnapshot) -> Freshness:
    reasons: list[str] = []
    if fingerprint["kind"] == "git":
        if not git.available or git.head is None:
            return Freshness("unknown", ("git_unavailable",))
        if git.head != fingerprint["head"]:
            return Freshness("stale", ("head_changed",))
        expected = fingerprint["files"]
    else:
        expected = fingerprint["entries"]
    unknown: list[str] = []
    for relative in related:
        actual, problem = _sample(Path(root), relative)
        if problem:
            unknown.append(problem)
        elif actual != expected[relative]:
            reasons.append(f"{relative}:content_changed")
    if unknown:
        return Freshness("unknown", tuple(sorted(unknown)))
    if reasons:
        return Freshness("stale", tuple(sorted(reasons)))
    return Freshness("fresh", ())
