#!/usr/bin/env python3
"""Validate YAML frontmatter across cairn's skills, commands, and agents.

Emits GitHub Actions ``::error file=...::`` / ``::warning file=...::``
annotations — so findings link to the offending file in the CI UI — and
exits non-zero on any error. Safe to run locally: the workflow commands
print as plain text with the path still visible in the ``file=`` field.

Per artefact type (rules match cairn's conventions, so a clean tree passes):

  skills/*/SKILL.md   required: name (slug), description
  commands/*.md       required: description   (name derives from filename)
  agents/*.md         required: name (slug), description

Checks:
  error   - missing YAML frontmatter fence / unterminated / unparseable
  error   - frontmatter is not a mapping
  error   - missing required field(s)
  error   - `name` present but not a string slug ([a-z][a-z0-9-]*)
  error   - `description` present but not a string
  warn    - description shorter than 30 chars (not a useful trigger)
  warn    - description longer than 1024 chars (truncated by Claude Code)
"""
from __future__ import annotations

import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
SLUG_RE = re.compile(r"^[a-z][a-z0-9-]*$")
DESC_MIN = 30
DESC_MAX = 1024  # Claude Code truncates descriptions beyond ~1024 chars.

# (glob, required-fields, name-must-be-a-slug)
SPECS = [
    ("skills/*/SKILL.md", {"name", "description"}, True),
    ("commands/*.md", {"description"}, False),
    ("agents/*.md", {"name", "description"}, True),
]


def parse_frontmatter(path: pathlib.Path):
    text = path.read_text()
    if not text.startswith("---\n"):
        return None, "missing YAML frontmatter"
    try:
        _, fm, _ = text.split("---\n", 2)
    except ValueError:
        return None, "unterminated YAML frontmatter"
    try:
        meta = yaml.safe_load(fm)
    except yaml.YAMLError as e:
        return None, f"frontmatter YAML error: {e}"
    if not isinstance(meta, dict):
        return None, "frontmatter must be a mapping"
    return meta, None


def validate_file(path, required, needs_slug_name):
    """Validate one artefact. ``path`` is absolute (read from it); findings
    carry the repo-relative path, so output is stable regardless of the
    caller's working directory and can be rendered as file-linked
    annotations. Returns ``(errors, warnings)`` as lists of ``(rel, msg)``."""
    rel = str(path.relative_to(ROOT))
    errors: list[tuple[str, str]] = []
    warnings: list[tuple[str, str]] = []

    meta, err = parse_frontmatter(path)
    if err:
        errors.append((rel, err))
        return errors, warnings

    missing = required - set(meta.keys())
    if missing:
        errors.append((rel, f"missing required field(s): {sorted(missing)}"))

    # A present `name` must be a string slug when the artefact type requires
    # one; a non-string scalar (e.g. `name: 123`) otherwise satisfies the
    # required-field check and skips validation.
    if needs_slug_name and "name" in meta:
        name = meta["name"]
        if not isinstance(name, str):
            errors.append(
                (rel, f"name must be a string slug, got {type(name).__name__}")
            )
        elif not SLUG_RE.match(name):
            errors.append((rel, f"name {name!r} must match [a-z][a-z0-9-]*"))

    # `description` is required for every artefact type, so a present-but-
    # non-string value is malformed, not merely unhelpful.
    if "description" in meta:
        desc = meta["description"]
        if not isinstance(desc, str):
            errors.append(
                (rel, f"description must be a string, got {type(desc).__name__}")
            )
        elif len(desc) < DESC_MIN:
            warnings.append(
                (rel, f"description is short ({len(desc)} chars); "
                      "should explain when to use it")
            )
        elif len(desc) > DESC_MAX:
            warnings.append(
                (rel, f"description is {len(desc)} chars; "
                      f"Claude Code truncates at ~{DESC_MAX}")
            )

    return errors, warnings


def _escape(msg: str) -> str:
    """Escape a message for a GitHub Actions workflow command."""
    return msg.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def _annotate(level: str, rel: str, msg: str) -> None:
    # `file=` links the annotation to the file; the path stays in `file=`
    # so local (non-Actions) runs still show which file is at fault.
    print(f"::{level} file={rel}::{_escape(msg)}")


def main() -> int:
    all_errors: list[tuple[str, str]] = []
    all_warnings: list[tuple[str, str]] = []
    count = 0

    for glob, required, needs_slug in SPECS:
        for path in sorted(ROOT.glob(glob)):
            count += 1
            errors, warnings = validate_file(path, required, needs_slug)
            all_errors += errors
            all_warnings += warnings

    for rel, msg in all_warnings:
        _annotate("warning", rel, msg)
    for rel, msg in all_errors:
        _annotate("error", rel, msg)

    if all_errors:
        return 1
    print(f"OK — {count} frontmatter file(s) validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
