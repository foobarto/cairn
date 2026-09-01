#!/usr/bin/env python3
"""Resolve an optional Strata project contract without mutating it."""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from typing import cast


PREFIX_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*$")
DEFAULT_EP_DIR = "docs/eps"
DEFAULT_PREFIX = "ep"
SEARCH_PARENT_LIMIT = 5


class ConfigError(ValueError):
    """Raised when a Strata contract is ambiguous or unsafe."""


@dataclass(frozen=True)
class StrataContract:
    """Resolved, read-only view of an installed Strata contract."""

    installed: bool
    config_path: str | None = None
    project_root: str | None = None
    proposal_dir: str | None = None
    prefix: str | None = None
    validator: str | None = None
    kit_version: str | None = None


def find_config(
    start: pathlib.Path,
    *,
    parent_limit: int = SEARCH_PARENT_LIMIT,
) -> pathlib.Path | None:
    """Find `.ep-kit` from ``start`` through at most ``parent_limit`` parents."""

    current = start.resolve()
    if current.is_file():
        current = current.parent
    for _ in range(parent_limit + 1):
        candidate = current / ".ep-kit"
        if candidate.is_file():
            return candidate
        if current.parent == current:
            break
        current = current.parent
    return None


def parse_config(path: pathlib.Path) -> dict[str, str]:
    """Parse Strata's documented ``key=value`` configuration subset."""

    values: dict[str, str] = {}
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        raise ConfigError(f"cannot read {path}: {exc}") from exc

    for line_number, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ConfigError(f"{path}:{line_number}: expected key=value")
        key, value = (part.strip() for part in line.split("=", 1))
        if not key or not value:
            raise ConfigError(f"{path}:{line_number}: key and value must be non-empty")
        if key in values:
            raise ConfigError(f"{path}:{line_number}: duplicate key {key!r}")
        values[key] = value
    return values


def resolve_project_path(root: pathlib.Path, value: str, *, field: str) -> pathlib.Path:
    """Resolve one project-relative config path and reject root escapes."""

    configured = pathlib.Path(value)
    if configured.is_absolute():
        raise ConfigError(f"{field} must be relative to .ep-kit")
    resolved = (root / configured).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ConfigError(f"{field} resolves outside the Strata project root") from exc
    return resolved


def resolve_contract(start: pathlib.Path) -> StrataContract:
    """Resolve the nearest Strata contract or report that none is installed."""

    config_path = find_config(start)
    if config_path is None:
        return StrataContract(installed=False)

    root = config_path.parent.resolve()
    values = parse_config(config_path)
    prefix = values.get("prefix", DEFAULT_PREFIX)
    if not PREFIX_RE.fullmatch(prefix):
        raise ConfigError(
            "prefix must start with a letter or underscore and contain only "
            "letters, digits, underscores, or hyphens"
        )

    proposal_dir = resolve_project_path(
        root,
        values.get("dir", DEFAULT_EP_DIR),
        field="dir",
    )
    validator_value = values.get("validator")
    validator = (
        resolve_project_path(root, validator_value, field="validator")
        if validator_value is not None
        else None
    )
    return StrataContract(
        installed=True,
        config_path=str(config_path.resolve()),
        project_root=str(root),
        proposal_dir=str(proposal_dir),
        prefix=prefix,
        validator=str(validator) if validator is not None else None,
        kit_version=values.get("kit_version"),
    )


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--start",
        type=pathlib.Path,
        default=pathlib.Path.cwd(),
        help="directory from which to search upward (default: current directory)",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Print the resolved contract as JSON and return a process status."""

    args = build_parser().parse_args(argv)
    start = cast(pathlib.Path, args.start)
    try:
        contract = resolve_contract(start)
    except ConfigError as exc:
        print(f"Strata configuration error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(asdict(contract), sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
