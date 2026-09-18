from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any


def read_utf8(path: Path) -> str:
    if not path.is_file():
        raise ValueError(f"not a regular file: {path}")
    return path.read_text(encoding="utf-8", errors="strict")


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json_object(path: Path, label: str) -> dict[str, object]:
    try:
        value = json.loads(read_utf8(path), object_pairs_hook=_unique_object)
    except (json.JSONDecodeError, UnicodeError) as error:
        raise ValueError(f"invalid {label}: {error}") from error
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value


def safe_relative(root: Path, path: Path) -> str:
    root_resolved = root.resolve()
    resolved = path.resolve()
    try:
        relative = resolved.relative_to(root_resolved)
    except ValueError as error:
        raise ValueError(f"path escapes root: {path}") from error
    if relative == Path("."):
        raise ValueError("path must name an entry below root")
    return relative.as_posix()


def resolve_under(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative or "\0" in relative:
        raise ValueError("relative path is empty or contains NUL")
    posix = PurePosixPath(relative)
    native = Path(relative)
    if posix.is_absolute() or native.is_absolute() or any(part in {"", ".", ".."} for part in posix.parts):
        raise ValueError(f"unsafe relative path: {relative!r}")
    root_resolved = root.resolve()
    target = (root_resolved / Path(*posix.parts)).resolve()
    try:
        target.relative_to(root_resolved)
    except ValueError as error:
        raise ValueError(f"path escapes root: {relative!r}") from error
    return target


def sha256_file(path: Path) -> str:
    if not path.is_file():
        raise ValueError(f"not a regular file: {path}")
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_fingerprint(root: Path, relpaths: list[str]) -> dict[str, str]:
    if len(relpaths) != len(set(relpaths)):
        raise ValueError("duplicate relative path")
    return {relative: sha256_file(resolve_under(root, relative)) for relative in sorted(relpaths)}


def _reject_write_symlinks(path: Path) -> None:
    if path.is_symlink():
        raise ValueError(f"write target is a symlink: {path}")
    current = path.parent
    while current != current.parent:
        if current.exists() and current.is_symlink():
            raise ValueError(f"write parent is a symlink: {current}")
        current = current.parent


def write_bytes_atomic(path: Path, data: bytes, mode: int = 0o644) -> None:
    _reject_write_symlinks(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    _reject_write_symlinks(path)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def write_json_atomic(path: Path, value: object) -> None:
    data = (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    write_bytes_atomic(path, data)
