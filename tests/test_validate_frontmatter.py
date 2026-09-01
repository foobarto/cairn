from __future__ import annotations

import inspect
import pathlib
import re
import tempfile
import unittest
from collections.abc import Iterator
from contextlib import contextmanager

from scripts import validate_frontmatter as validator


class FrontmatterValidatorTests(unittest.TestCase):
    @contextmanager
    def skill_file(
        self,
        frontmatter: str,
        *,
        folder: str = "valid-skill",
        body: str = "# Valid skill\n\nDo the task.",
    ) -> Iterator[tuple[pathlib.Path, pathlib.Path]]:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = pathlib.Path(temporary_directory)
            skill_directory = root / "skills" / folder
            skill_directory.mkdir(parents=True)
            skill_path = skill_directory / "SKILL.md"
            skill_path.write_text(
                f"---\n{frontmatter}\n---\n\n{body}\n",
                encoding="utf-8",
            )
            yield root, skill_path

    def messages(self, findings: list[validator.Finding]) -> list[str]:
        return [finding.message for finding in findings]

    def test_repository_skills_pass_strict_validation(self) -> None:
        root = pathlib.Path(__file__).resolve().parent.parent
        findings = validator.validate_repository(root)
        self.assertEqual([], findings)

    def test_packaged_skill_relative_links_resolve_inside_the_skill(self) -> None:
        root = pathlib.Path(__file__).resolve().parent.parent
        link_pattern = re.compile(r"\[[^]]*\]\(([^)]+)\)")
        for skill_path in sorted((root / "skills").glob("*/SKILL.md")):
            for target in link_pattern.findall(skill_path.read_text(encoding="utf-8")):
                if "://" in target or target.startswith("#"):
                    continue
                clean_target = target.split("#", 1)[0]
                resolved = (skill_path.parent / clean_target).resolve()
                with self.subTest(skill=skill_path.parent.name, target=target):
                    self.assertTrue(resolved.is_relative_to(skill_path.parent.resolve()))
                    self.assertTrue(resolved.exists())

    def test_valid_skill_accepts_all_standard_fields(self) -> None:
        frontmatter = """name: valid-skill
description: Perform a valid task when the user requests the valid workflow.
license: MIT OR Apache-2.0
compatibility: Requires a client that supports Agent Skills.
metadata:
  version: "1.0.0"
allowed-tools: Read Bash(git:*)"""
        with self.skill_file(frontmatter) as (root, path):
            self.assertEqual([], validator.validate_skill(path, root))

    def test_name_must_match_parent_directory(self) -> None:
        frontmatter = """name: different-skill
description: Perform a valid task when the user requests the valid workflow."""
        with self.skill_file(frontmatter) as (root, path):
            findings = validator.validate_skill(path, root)
        self.assertTrue(any("must match parent directory" in item for item in self.messages(findings)))

    def test_unsupported_top_level_version_is_rejected(self) -> None:
        frontmatter = """name: valid-skill
description: Perform a valid task when the user requests the valid workflow.
version: 1.0.0"""
        with self.skill_file(frontmatter) as (root, path):
            findings = validator.validate_skill(path, root)
        self.assertTrue(any("unsupported Agent Skills field" in item for item in self.messages(findings)))

    def test_invalid_names_are_rejected(self) -> None:
        invalid_names = ("-leading", "trailing-", "double--hyphen", "Uppercase", "under_score")
        for name in invalid_names:
            with self.subTest(name=name):
                frontmatter = (
                    f"name: {name}\n"
                    "description: Perform a valid task when the user requests the valid workflow."
                )
                with self.skill_file(frontmatter, folder=name) as (root, path):
                    findings = validator.validate_skill(path, root)
                self.assertTrue(any("single hyphens only" in item for item in self.messages(findings)))

    def test_name_longer_than_spec_limit_is_rejected(self) -> None:
        name = "a" * 65
        frontmatter = (
            f"name: {name}\n"
            "description: Perform a valid task when the user requests the valid workflow."
        )
        with self.skill_file(frontmatter, folder=name) as (root, path):
            findings = validator.validate_skill(path, root)
        self.assertTrue(any("maximum is 64" in item for item in self.messages(findings)))

    def test_empty_and_long_descriptions_are_errors(self) -> None:
        for description in ('""', "x" * 1025):
            with self.subTest(length=len(description)):
                frontmatter = f"name: valid-skill\ndescription: {description}"
                with self.skill_file(frontmatter) as (root, path):
                    findings = validator.validate_skill(path, root)
                self.assertTrue(any(item.severity == "error" for item in findings))

    def test_metadata_values_must_be_strings(self) -> None:
        frontmatter = """name: valid-skill
description: Perform a valid task when the user requests the valid workflow.
metadata:
  version: 1"""
        with self.skill_file(frontmatter) as (root, path):
            findings = validator.validate_skill(path, root)
        self.assertIn("metadata keys and values must all be strings", self.messages(findings))

    def test_compatibility_limit_and_nonempty_body_are_enforced(self) -> None:
        frontmatter = (
            "name: valid-skill\n"
            "description: Perform a valid task when the user requests the valid workflow.\n"
            f"compatibility: {'x' * 501}"
        )
        with self.skill_file(frontmatter, body="") as (root, path):
            findings = validator.validate_skill(path, root)
        messages = self.messages(findings)
        self.assertTrue(any("maximum is 500" in item for item in messages))
        self.assertIn("Markdown body must not be empty", messages)

    def test_github_annotation_escapes_control_characters(self) -> None:
        rendered = validator.render_finding(
            validator.Finding("error", "a%b,c:d.md", "line one\nline two")
        )
        self.assertEqual(
            "::error file=a%25b%2Cc%3Ad.md::line one%0Aline two",
            rendered,
        )

    def test_module_functions_have_complete_annotations(self) -> None:
        functions = (
            function
            for _, function in inspect.getmembers(validator, inspect.isfunction)
            if function.__module__ == validator.__name__
        )
        for function in functions:
            with self.subTest(function=function.__name__):
                signature = inspect.signature(function)
                self.assertIsNot(signature.return_annotation, inspect.Signature.empty)
                for parameter in signature.parameters.values():
                    self.assertIsNot(parameter.annotation, inspect.Parameter.empty)


if __name__ == "__main__":
    unittest.main()
