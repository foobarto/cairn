#!/usr/bin/env python3
"""Validate YAML frontmatter across cairn's skills, commands, and agents.

Emits ``::error::`` / ``::warning::`` annotations when run under GitHub
Actions and exits non-zero on any error. Safe to run locally — the
annotations degrade gracefully to plain stdout.

Per artefact type (rules match cairn's conventions, so a clean tree
passes):

  skills/*/SKILL.md   required: name (slug), description
  commands/*.md       required: description   (name derives from filename)
  agents/*.md         required: name (slug), description

Checks:
  error   - missing YAML frontmatter fence / unterminated / unparseable
  error   - frontmatter is not a mapping
  error   - missing required field(s)
  error   - `name` present but not a valid slug ([a-z][a-z0-9-]*)
  warn    - description shorter than 30 chars (not a useful trigger)
  warn    - description longer than 1024 chars (truncated by Claude Code)
  warn    - description present but not a string
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
    """Validate one artefact. ``path`` is absolute (read from it); messages
    are reported with the repo-relative path so output is stable regardless
    of the caller's working directory."""
    errors: list[str] = []
    warnings: list[str] = []
    rel = path.relative_to(ROOT)

    meta, err = parse_frontmatter(path)
    if err:
        errors.append(f"{rel}: {err}")
        return errors, warnings

    missing = required - set(meta.keys())
    if missing:
        errors.append(f"{rel}: missing required field(s): {sorted(missing)}")

    # A present `name` must be a string slug when the artefact type requires
    # one. A non-string scalar (e.g. `name: 123` or `name: true`) otherwise
    # satisfies the required-field check and skips slug validation, so reject
    # it explicitly.
    if needs_slug_name and "name" in meta:
        name = meta["name"]
        if not isinstance(name, str):
            errors.append(
                f"{rel}: name must be a string slug, got {type(name).__name__}"
            )
        elif not SLUG_RE.match(name):
            errors.append(f"{rel}: name {name!r} must match [a-z][a-z0-9-]*")

    if "description" in meta:
        desc = meta["description"]
        if not isinstance(desc, str):
            warnings.append(f"{rel}: description is not a string")
        elif len(desc) < DESC_MIN:
            warnings.append(
                f"{rel}: description is short ({len(desc)} chars); "
                "should explain when to use it"
            )
        elif len(desc) > DESC_MAX:
            warnings.append(
                f"{rel}: description is {len(desc)} chars; "
                f"Claude Code truncates at ~{DESC_MAX}"
            )

    return errors, warnings


def main() -> int:
    all_errors: list[str] = []
    all_warnings: list[str] = []
    count = 0

    for glob, required, needs_slug in SPECS:
        for path in sorted(ROOT.glob(glob)):
            count += 1
            errors, warnings = validate_file(path, required, needs_slug)
            all_errors += errors
            all_warnings += warnings

    for w in all_warnings:
        print(f"::warning::{w}")
    for e in all_errors:
        print(f"::error::{e}")

    if all_errors:
        return 1
    print(f"OK — {count} frontmatter file(s) validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
