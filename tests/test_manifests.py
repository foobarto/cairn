from __future__ import annotations

import json
import pathlib
import re
import unittest
from typing import cast


RELEASE_VERSION = "0.3.0"


class ManifestTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = pathlib.Path(__file__).resolve().parent.parent
        self.claude_plugin = self.read_json(self.root / ".claude-plugin" / "plugin.json")
        self.claude_marketplace = self.read_json(
            self.root / ".claude-plugin" / "marketplace.json"
        )
        self.codex_plugin = self.read_json(self.root / ".codex-plugin" / "plugin.json")
        self.codex_marketplace = self.read_json(
            self.root / ".agents" / "plugins" / "marketplace.json"
        )

    def read_json(self, path: pathlib.Path) -> dict[str, object]:
        with path.open(encoding="utf-8") as handle:
            value = json.load(handle)
        self.assertIsInstance(value, dict)
        return cast(dict[str, object], value)

    def test_plugin_has_distribution_metadata(self) -> None:
        for plugin in (self.claude_plugin, self.codex_plugin):
            with self.subTest(plugin=plugin):
                self.assertEqual("cairn", plugin["name"])
                self.assertEqual(RELEASE_VERSION, plugin["version"])
                self.assertRegex(
                    cast(str, plugin["version"]),
                    r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$",
                )
                self.assertEqual("MIT OR Apache-2.0", plugin["license"])
                self.assertEqual("https://github.com/foobarto/cairn", plugin["repository"])

    def test_marketplace_points_to_the_root_plugin(self) -> None:
        claude_plugins = cast(
            list[dict[str, object]], self.claude_marketplace["plugins"]
        )
        self.assertEqual(1, len(claude_plugins))
        self.assertEqual("cairn", claude_plugins[0]["name"])
        self.assertEqual("./", claude_plugins[0]["source"])

        codex_plugins = cast(list[dict[str, object]], self.codex_marketplace["plugins"])
        self.assertEqual(1, len(codex_plugins))
        self.assertEqual("cairn", codex_plugins[0]["name"])
        self.assertEqual(
            # Codex resolves ./ to the installed marketplace checkout root,
            # preserving the marketplace ref rather than re-fetching main.
            {"source": "url", "url": "./"},
            codex_plugins[0]["source"],
        )
        self.assertEqual(
            {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
            codex_plugins[0]["policy"],
        )

    def test_all_canonical_skill_names_are_unique(self) -> None:
        names: list[str] = []
        for path in sorted((self.root / "skills").glob("*/SKILL.md")):
            match = re.search(r"(?m)^name: ([a-z0-9-]+)$", path.read_text(encoding="utf-8"))
            self.assertIsNotNone(match, path)
            assert match is not None
            names.append(match.group(1))
        self.assertEqual(len(names), len(set(names)))

    def test_all_skill_versions_match_the_release(self) -> None:
        for path in sorted((self.root / "skills").glob("*/SKILL.md")):
            text = path.read_text(encoding="utf-8")
            with self.subTest(skill=path.parent.name):
                self.assertIn(f'version: "{RELEASE_VERSION}"', text)


if __name__ == "__main__":
    unittest.main()
