from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from _workflowlib import read_utf8


@dataclass(frozen=True)
class SkillMetadata:
    name: str
    description: str


def _scalar(value: str, field: str) -> str:
    value = value.strip()
    if not value or value in {"|", ">", "|-", ">-", "|+", ">+"}:
        raise ValueError(f"{field} must be a non-empty single-line scalar")
    if value.startswith('"'):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as error:
            raise ValueError(f"invalid quoted {field}") from error
        if not isinstance(parsed, str) or not parsed.strip() or "\n" in parsed or "\r" in parsed:
            raise ValueError(f"{field} must be a single-line string")
        return parsed
    if value.startswith("'"):
        if len(value) < 2 or not value.endswith("'"):
            raise ValueError(f"invalid quoted {field}")
        inner = value[1:-1]
        if not inner.strip() or re.fullmatch(r"(?:[^']|'')+", inner) is None:
            raise ValueError(f"invalid quoted {field}")
        return inner.replace("''", "'")
    if value[0] in "[{&*!" or value.startswith(("!!", "---", "...")):
        raise ValueError(f"unsupported {field} scalar")
    if value.casefold() in {"null", "true", "false", "yes", "no", "on", "off", "~"}:
        raise ValueError(f"implicit YAML value is not allowed for {field}")
    if re.search(r"(^|\s)#", value) or ": " in value:
        raise ValueError(f"YAML comment or mapping syntax is not allowed for {field}")
    if value.startswith(('"', "'")) or "\t" in value:
        raise ValueError(f"invalid unquoted {field} scalar")
    return value


def parse_skill_metadata(path: Path) -> SkillMetadata:
    lines = read_utf8(path).splitlines()
    if not lines or lines[0] != "---":
        raise ValueError(f"missing frontmatter opener: {path}")
    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise ValueError(f"unclosed frontmatter: {path}") from error
    fields: dict[str, str] = {}
    for line in lines[1:end]:
        if not line or line[:1].isspace() or ":" not in line:
            raise ValueError(f"unsupported frontmatter line: {line!r}")
        key, raw = line.split(":", 1)
        if key not in {"name", "description"}:
            raise ValueError(f"unsupported frontmatter field: {key}")
        if key in fields:
            raise ValueError(f"duplicate frontmatter field: {key}")
        fields[key] = _scalar(raw, key)
    if set(fields) != {"name", "description"}:
        raise ValueError("frontmatter requires name and description")
    if path.name != "SKILL.md" or path.parent.name != fields["name"]:
        raise ValueError(f"skill name does not match directory: {fields['name']}")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", fields["name"]):
        raise ValueError("invalid skill name")
    return SkillMetadata(fields["name"], fields["description"])
