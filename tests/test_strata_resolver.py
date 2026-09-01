from __future__ import annotations

import json
import pathlib
import subprocess
import tempfile
import unittest
from typing import cast


class StrataResolverTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = pathlib.Path(__file__).resolve().parent.parent
        self.resolver = (
            self.root
            / "skills"
            / "cairn-strata-interop"
            / "scripts"
            / "resolve_strata.py"
        )

    def run_resolver(
        self, start: pathlib.Path, *, expected_status: int = 0
    ) -> tuple[dict[str, object] | None, str]:
        result = subprocess.run(
            [str(self.resolver), "--start", str(start)],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(expected_status, result.returncode, result.stderr)
        payload = json.loads(result.stdout) if result.stdout else None
        if payload is not None:
            self.assertIsInstance(payload, dict)
        return cast(dict[str, object] | None, payload), result.stderr

    def test_missing_contract_is_optional(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            payload, stderr = self.run_resolver(pathlib.Path(temporary_directory))
        self.assertEqual(
            {
                "installed": False,
                "config_path": None,
                "project_root": None,
                "proposal_dir": None,
                "prefix": None,
                "validator": None,
                "kit_version": None,
            },
            payload,
        )
        self.assertEqual("", stderr)

    def test_resolves_current_contract_from_nested_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = pathlib.Path(temporary_directory)
            nested = root / "one" / "two"
            nested.mkdir(parents=True)
            (root / ".ep-kit").write_text(
                "dir=docs/rfcs\nprefix=rfc\n"
                "validator=scripts/validate-rfcs.sh\nkit_version=1.3.0\n",
                encoding="utf-8",
            )
            payload, _ = self.run_resolver(nested)

        assert payload is not None
        self.assertTrue(payload["installed"])
        self.assertEqual("rfc", payload["prefix"])
        self.assertEqual("1.3.0", payload["kit_version"])
        self.assertEqual(str(root / "docs" / "rfcs"), payload["proposal_dir"])
        self.assertEqual(
            str(root / "scripts" / "validate-rfcs.sh"), payload["validator"]
        )

    def test_older_contract_defaults_newer_optional_keys(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = pathlib.Path(temporary_directory)
            (root / ".ep-kit").write_text("# older install\n", encoding="utf-8")
            payload, _ = self.run_resolver(root)

        assert payload is not None
        self.assertEqual("ep", payload["prefix"])
        self.assertEqual(str(root / "docs" / "eps"), payload["proposal_dir"])
        self.assertIsNone(payload["validator"])
        self.assertIsNone(payload["kit_version"])

    def test_accepts_ep_kit_compatible_custom_prefix(self) -> None:
        for prefix in ("RFC", "_RFC2"):
            with self.subTest(prefix=prefix):
                with tempfile.TemporaryDirectory() as temporary_directory:
                    root = pathlib.Path(temporary_directory)
                    (root / ".ep-kit").write_text(
                        f"prefix={prefix}\n", encoding="utf-8"
                    )
                    payload, _ = self.run_resolver(root)

                assert payload is not None
                self.assertEqual(prefix, payload["prefix"])

    def test_rejects_unsafe_or_ambiguous_config_before_use(self) -> None:
        invalid_configs = (
            "dir=../outside\n",
            "validator=/tmp/validator\n",
            "prefix=9starts-with-a-digit\n",
            "dir=docs/eps\ndir=docs/rfcs\n",
            "not-a-pair\n",
        )
        for config in invalid_configs:
            with self.subTest(config=config):
                with tempfile.TemporaryDirectory() as temporary_directory:
                    root = pathlib.Path(temporary_directory)
                    (root / ".ep-kit").write_text(config, encoding="utf-8")
                    payload, stderr = self.run_resolver(root, expected_status=1)
                self.assertIsNone(payload)
                self.assertIn("Strata configuration error:", stderr)


if __name__ == "__main__":
    unittest.main()
