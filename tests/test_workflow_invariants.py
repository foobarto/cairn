from __future__ import annotations

import pathlib
import unittest


class WorkflowInvariantTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = pathlib.Path(__file__).resolve().parent.parent

    def read(self, relative_path: str) -> str:
        return (self.root / relative_path).read_text(encoding="utf-8")

    def test_strata_uses_canonical_textual_references(self) -> None:
        interop = self.read("skills/cairn-strata-interop/SKILL.md")
        session_log = self.read("skills/cairn-session-log/SKILL.md")
        self.assertIn("`EP-NNNN`", interop)
        for text in (interop, session_log):
            with self.subTest(document=text[:40]):
                self.assertNotIn("`RFC-NNNN`", text)
                self.assertNotIn("`GEP-NNNN`", text)

    def test_strata_rename_preserves_the_legacy_protocol(self) -> None:
        readme = self.read("README.md")
        interop = self.read("skills/cairn-strata-interop/SKILL.md")
        self.assertIn("https://github.com/foobarto/strata", readme)
        self.assertIn("Strata 1.3.0", readme)
        self.assertIn("`.ep-kit`", readme)
        self.assertIn("`kit_version`", readme)
        self.assertIn("installed `ep-kit*` skill names", readme)
        self.assertIn("name: cairn-strata-interop", interop)
        paths = [self.root / "README.md"]
        for directory in ("agents", "commands", "docs", "evals", "skills", "templates"):
            paths.extend((self.root / directory).rglob("*.md"))
        for path in paths:
            with self.subTest(path=path):
                self.assertNotIn(
                    "cairn-ep-kit-interop", path.read_text(encoding="utf-8")
                )

    def test_release_roadmap_places_0_3_immediately_before_1_0(self) -> None:
        readme = self.read("README.md")
        changelog = self.read("CHANGELOG.md")
        self.assertIn("final pre-1.0 release line", readme)
        self.assertIn("next release line will be 1.0", readme)
        self.assertIn("## [v0.3.0] — 2026-09-01", changelog)

    def test_partial_proposals_are_implementation_authority(self) -> None:
        checklist = self.read("templates/workflow/six-phase-checklist.md")
        protocol = self.read("templates/workflow/autonomous-protocol.md")
        self.assertIn("Accepted/Partial proposal when required", checklist)
        self.assertIn("it is `Accepted` or `Partial`", checklist)
        self.assertNotIn("Proposal is `Accepted`.", checklist)
        self.assertIn("Only Accepted/Partial implementation work is", protocol)

    def test_autonomy_is_not_an_unaccepted_proposal_override(self) -> None:
        interop = self.read("skills/cairn-strata-interop/SKILL.md")
        self.assertIn("Never let L2, L3, or L4 override proposal status", interop)
        self.assertIn("specific, scoped pre-acceptance", interop)
        self.assertIn("Never infer one", interop)

    def test_user_profile_has_only_private_scopes_and_requires_authority(self) -> None:
        profile = self.read("templates/user-profile.md")
        self.assertNotIn("project-local-tracked", profile)
        self.assertNotIn("docs/user-profiles", profile)
        self.assertIn("explicitly asks to record", profile)
        self.assertIn("ordinary conversation is not permission", profile)

    def test_skill_cross_references_use_canonical_names(self) -> None:
        documents = (
            "agents/autonomous-planner.md",
            "agents/review-runner.md",
            "commands/cairn-loop.md",
            "commands/cairn-round.md",
            "skills/cairn-autonomous-loop/SKILL.md",
            "skills/cairn-autonomous-round/SKILL.md",
            "skills/cairn-build-project-profile/SKILL.md",
            "skills/cairn-build-user-profile/SKILL.md",
            "skills/cairn-close-session/SKILL.md",
            "templates/workflow/autonomous-protocol.md",
            "templates/workflow/six-phase-checklist.md",
        )
        stale_references = (
            "`review-phase` skill",
            "`build-user-profile`",
            "`build-project-profile`",
            "the session-log skill",
            "the autonomous-round skill",
        )
        for relative_path in documents:
            text = self.read(relative_path)
            for stale_reference in stale_references:
                with self.subTest(path=relative_path, reference=stale_reference):
                    self.assertNotIn(stale_reference, text)


if __name__ == "__main__":
    unittest.main()
