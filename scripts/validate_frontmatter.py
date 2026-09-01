#!/usr/bin/env python3
"""Validate Cairn skills and Claude Code adapter frontmatter.

Skill validation follows https://agentskills.io/specification. Commands and
agents use the narrower Claude Code adapter rules documented by this project.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Literal, TypeAlias, cast

import yaml


Severity: TypeAlias = Literal["error", "warning"]
Metadata: TypeAlias = dict[str, object]

SKILL_FIELDS = frozenset(
    {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
)
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
AGENT_NAME_RE = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
DESCRIPTION_MAX = 1024
DESCRIPTION_RECOMMENDED_MIN = 30
COMPATIBILITY_MAX = 500
SKILL_RECOMMENDED_MAX_LINES = 500


@dataclass(frozen=True)
class Finding:
    """One validation diagnostic."""

    severity: Severity
    path: str
    message: str


@dataclass(frozen=True)
class ParsedDocument:
    """Parsed YAML metadata and Markdown body from one artifact."""

    metadata: Metadata
    body: str
    line_count: int


def parse_frontmatter(path: pathlib.Path) -> tuple[ParsedDocument | None, str | None]:
    """Parse a frontmatter document and return either the document or an error."""

    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return None, f"cannot read UTF-8 text: {exc}"

    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return None, "missing YAML frontmatter"

    try:
        closing_index = lines.index("---", 1)
    except ValueError:
        return None, "unterminated YAML frontmatter"

    frontmatter = "\n".join(lines[1:closing_index])
    try:
        loaded = cast(object, yaml.safe_load(frontmatter))
    except yaml.YAMLError as exc:
        return None, f"frontmatter YAML error: {exc}"

    if not isinstance(loaded, Mapping):
        return None, "frontmatter must be a mapping"
    if not all(isinstance(key, str) for key in loaded):
        return None, "frontmatter keys must be strings"

    metadata = {cast(str, key): value for key, value in loaded.items()}
    body = "\n".join(lines[closing_index + 1 :]).strip()
    return ParsedDocument(metadata=metadata, body=body, line_count=len(lines)), None


def _finding(severity: Severity, path: pathlib.Path, root: pathlib.Path, message: str) -> Finding:
    """Create a diagnostic with a stable repository-relative path."""

    try:
        display_path = str(path.relative_to(root))
    except ValueError:
        display_path = str(path)
    return Finding(severity=severity, path=display_path, message=message)


def _require_string(
    metadata: Metadata,
    field: str,
    path: pathlib.Path,
    root: pathlib.Path,
    *,
    maximum: int | None = None,
) -> list[Finding]:
    """Validate a required non-empty string field."""

    value = metadata.get(field)
    if field not in metadata:
        return [_finding("error", path, root, f"missing required field: {field}")]
    if not isinstance(value, str):
        return [
            _finding(
                "error",
                path,
                root,
                f"{field} must be a string, got {type(value).__name__}",
            )
        ]
    if not value.strip():
        return [_finding("error", path, root, f"{field} must not be empty")]
    if maximum is not None and len(value) > maximum:
        return [
            _finding(
                "error",
                path,
                root,
                f"{field} is {len(value)} characters; maximum is {maximum}",
            )
        ]
    return []


def _validate_optional_string(
    metadata: Metadata,
    field: str,
    path: pathlib.Path,
    root: pathlib.Path,
    *,
    maximum: int | None = None,
) -> list[Finding]:
    """Validate an optional non-empty string field."""

    if field not in metadata:
        return []
    value = metadata[field]
    if not isinstance(value, str):
        return [
            _finding(
                "error",
                path,
                root,
                f"{field} must be a string, got {type(value).__name__}",
            )
        ]
    if not value.strip():
        return [_finding("error", path, root, f"{field} must not be empty")]
    if maximum is not None and len(value) > maximum:
        return [
            _finding(
                "error",
                path,
                root,
                f"{field} is {len(value)} characters; maximum is {maximum}",
            )
        ]
    return []


def validate_skill(path: pathlib.Path, root: pathlib.Path) -> list[Finding]:
    """Validate one Agent Skills skill directory."""

    document, parse_error = parse_frontmatter(path)
    if parse_error is not None:
        return [_finding("error", path, root, parse_error)]
    assert document is not None

    metadata = document.metadata
    findings: list[Finding] = []

    unexpected = sorted(set(metadata) - SKILL_FIELDS)
    if unexpected:
        findings.append(
            _finding(
                "error",
                path,
                root,
                f"unsupported Agent Skills field(s): {unexpected}",
            )
        )

    findings.extend(_require_string(metadata, "name", path, root, maximum=64))
    name = metadata.get("name")
    if isinstance(name, str):
        if not SKILL_NAME_RE.fullmatch(name):
            findings.append(
                _finding(
                    "error",
                    path,
                    root,
                    "name must contain lowercase ASCII letters, digits, and single hyphens only",
                )
            )
        if name != path.parent.name:
            findings.append(
                _finding(
                    "error",
                    path,
                    root,
                    f"name {name!r} must match parent directory {path.parent.name!r}",
                )
            )

    findings.extend(
        _require_string(metadata, "description", path, root, maximum=DESCRIPTION_MAX)
    )
    description = metadata.get("description")
    if isinstance(description, str) and 0 < len(description) < DESCRIPTION_RECOMMENDED_MIN:
        findings.append(
            _finding(
                "warning",
                path,
                root,
                f"description is short ({len(description)} characters); include what and when",
            )
        )

    findings.extend(_validate_optional_string(metadata, "license", path, root))
    findings.extend(
        _validate_optional_string(
            metadata,
            "compatibility",
            path,
            root,
            maximum=COMPATIBILITY_MAX,
        )
    )
    findings.extend(_validate_optional_string(metadata, "allowed-tools", path, root))

    skill_metadata = metadata.get("metadata")
    if "metadata" in metadata:
        if not isinstance(skill_metadata, Mapping):
            findings.append(
                _finding("error", path, root, "metadata must be a mapping of string keys to strings")
            )
        elif not all(
            isinstance(key, str) and isinstance(value, str)
            for key, value in skill_metadata.items()
        ):
            findings.append(
                _finding("error", path, root, "metadata keys and values must all be strings")
            )

    if not document.body:
        findings.append(_finding("error", path, root, "Markdown body must not be empty"))
    if document.line_count > SKILL_RECOMMENDED_MAX_LINES:
        findings.append(
            _finding(
                "warning",
                path,
                root,
                f"skill is {document.line_count} lines; keep SKILL.md under 500 lines when practical",
            )
        )
    return findings


def validate_adapter_artifact(
    path: pathlib.Path,
    root: pathlib.Path,
    *,
    needs_name: bool,
) -> list[Finding]:
    """Validate one Claude Code command or subagent definition."""

    document, parse_error = parse_frontmatter(path)
    if parse_error is not None:
        return [_finding("error", path, root, parse_error)]
    assert document is not None

    findings = _require_string(
        document.metadata,
        "description",
        path,
        root,
        maximum=DESCRIPTION_MAX,
    )
    if needs_name:
        findings.extend(_require_string(document.metadata, "name", path, root, maximum=64))
        name = document.metadata.get("name")
        if isinstance(name, str) and not AGENT_NAME_RE.fullmatch(name):
            findings.append(
                _finding("error", path, root, "name must be a lowercase hyphenated slug")
            )
    if not document.body:
        findings.append(_finding("error", path, root, "Markdown body must not be empty"))
    return findings


def validate_repository(
    root: pathlib.Path,
    *,
    skills_root: pathlib.Path | None = None,
    include_adapters: bool = True,
) -> list[Finding]:
    """Validate a skill tree and, optionally, repository adapter artifacts."""

    resolved_root = root.resolve()
    if skills_root is None:
        resolved_skills_root = (resolved_root / "skills").resolve()
    elif skills_root.is_absolute():
        resolved_skills_root = skills_root.resolve()
    else:
        resolved_skills_root = (resolved_root / skills_root).resolve()
    findings: list[Finding] = []
    skill_paths = sorted(resolved_skills_root.glob("*/SKILL.md"))
    if not skill_paths:
        findings.append(
            _finding(
                "error",
                resolved_skills_root,
                resolved_root,
                "no skills found under */SKILL.md",
            )
        )
    for path in skill_paths:
        findings.extend(validate_skill(path, resolved_root))
    if include_adapters:
        for path in sorted(resolved_root.glob("commands/*.md")):
            findings.extend(validate_adapter_artifact(path, resolved_root, needs_name=False))
        for path in sorted(resolved_root.glob("agents/*.md")):
            findings.extend(validate_adapter_artifact(path, resolved_root, needs_name=True))
    return findings


def _escape_workflow_command(value: str) -> str:
    """Escape data embedded in a GitHub Actions workflow command."""

    return value.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def _escape_workflow_property(value: str) -> str:
    """Escape one GitHub Actions workflow-command property."""

    return _escape_workflow_command(value).replace(":", "%3A").replace(",", "%2C")


def render_finding(finding: Finding) -> str:
    """Render one finding as a file-linked GitHub Actions annotation."""

    level = "error" if finding.severity == "error" else "warning"
    path = _escape_workflow_property(finding.path)
    message = _escape_workflow_command(finding.message)
    return f"::{level} file={path}::{message}"


def _build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=pathlib.Path,
        default=pathlib.Path(__file__).resolve().parent.parent,
        help="repository root to validate (default: validator's parent repository)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="treat recommendations emitted as warnings as failures",
    )
    parser.add_argument(
        "--skills-root",
        type=pathlib.Path,
        help="skill directory to validate instead of <root>/skills",
    )
    parser.add_argument(
        "--skills-only",
        action="store_true",
        help="skip Claude Code command and subagent adapter validation",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run repository validation and return a process exit status."""

    args = _build_parser().parse_args(argv)
    root = cast(pathlib.Path, args.root)
    strict = cast(bool, args.strict)
    skills_root = cast(pathlib.Path | None, args.skills_root)
    skills_only = cast(bool, args.skills_only)
    findings = validate_repository(
        root,
        skills_root=skills_root,
        include_adapters=not skills_only,
    )
    for finding in findings:
        print(render_finding(finding))

    errors = sum(finding.severity == "error" for finding in findings)
    warnings = sum(finding.severity == "warning" for finding in findings)
    if errors or (strict and warnings):
        return 1

    if skills_root is None:
        skill_base = root.resolve() / "skills"
    elif skills_root.is_absolute():
        skill_base = skills_root.resolve()
    else:
        skill_base = (root.resolve() / skills_root).resolve()
    skill_count = len(list(skill_base.glob("*/SKILL.md")))
    print(f"OK — {skill_count} Agent Skills validated ({warnings} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
