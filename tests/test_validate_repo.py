from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts import validate_repo


class ValidateRepoTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.root = Path(self.temporary_directory.name)
        self.manifest_path = self.root / ".codex-plugin" / "plugin.json"
        self.skill_directory = self.root / "skills" / "codex-staff"
        self.skill_path = self.skill_directory / "SKILL.md"
        self.openai_path = self.skill_directory / "agents" / "openai.yaml"

        self.manifest = {
            "name": "hrsh22-skills",
            "version": "0.1.0",
            "skills": "./skills/",
            "interface": {
                "defaultPrompt": ["$codex-staff coordinate this task."],
            },
        }
        self.write_manifest()
        self.write_skill()
        self.write_openai_yaml()

    def write_manifest(self) -> None:
        self.manifest_path.parent.mkdir(parents=True, exist_ok=True)
        self.manifest_path.write_text(json.dumps(self.manifest), encoding="utf-8")

    def write_skill(
        self,
        *,
        name: object = "codex-staff",
        license_value: object = "MIT",
    ) -> None:
        self.skill_directory.mkdir(parents=True, exist_ok=True)
        self.skill_path.write_text(
            "---\n"
            f"name: {json.dumps(name)}\n"
            f"license: {json.dumps(license_value)}\n"
            "---\n\n"
            "# Codex Staff\n",
            encoding="utf-8",
        )

    def write_openai_yaml(
        self,
        prompt: object = "Use $codex-staff to coordinate this task.",
    ) -> None:
        self.openai_path.parent.mkdir(parents=True, exist_ok=True)
        self.openai_path.write_text(
            "interface:\n"
            f"  default_prompt: {json.dumps(prompt)}\n",
            encoding="utf-8",
        )

    def validate(self, tag: str | None = None) -> list[str]:
        return validate_repo.validate(tag, root=self.root)

    def assert_failure_contains(self, expected: str, failures: list[str]) -> None:
        self.assertTrue(
            any(expected in failure for failure in failures),
            f"Expected a failure containing {expected!r}; got {failures!r}",
        )

    def test_valid_baseline(self) -> None:
        self.assertEqual([], self.validate())
        self.assertEqual([], self.validate("v0.1.0"))

    def test_missing_manifest_is_a_validation_failure(self) -> None:
        self.manifest_path.unlink()

        failures = self.validate()

        self.assertEqual(1, len(failures))
        self.assert_failure_contains("plugin.json", failures)

    def test_manifest_with_invalid_utf8_is_a_validation_failure(self) -> None:
        self.manifest_path.write_bytes(b"\xff")

        failures = self.validate()

        self.assertEqual(1, len(failures))
        self.assert_failure_contains("plugin.json", failures)

    def test_malformed_manifest_json_is_a_validation_failure(self) -> None:
        self.manifest_path.write_text("{", encoding="utf-8")

        failures = self.validate()

        self.assertEqual(1, len(failures))
        self.assert_failure_contains("plugin.json", failures)

    def test_manifest_must_be_an_object(self) -> None:
        for value in (None, [], "manifest"):
            with self.subTest(value=value):
                self.manifest_path.write_text(json.dumps(value), encoding="utf-8")

                failures = self.validate()

                self.assertEqual(1, len(failures))
                self.assert_failure_contains("manifest must be a JSON object", failures)

    def test_manifest_name_must_match_plugin_identifier(self) -> None:
        self.manifest["name"] = "another-plugin"
        self.write_manifest()

        self.assert_failure_contains("unexpected Codex plugin identifier", self.validate())

    def test_manifest_version_must_be_semver(self) -> None:
        invalid_versions = (None, 1, "1", "01.2.3", "1.2", "v1.2.3")
        for value in invalid_versions:
            with self.subTest(value=value):
                self.manifest["version"] = value
                self.write_manifest()

                self.assert_failure_contains(
                    "plugin version must be valid Semantic Versioning",
                    self.validate(),
                )

    def test_release_tag_must_match_manifest_version(self) -> None:
        failures = self.validate("v0.2.0")

        self.assert_failure_contains(
            "tag 'v0.2.0' does not match plugin version v0.1.0",
            failures,
        )

    def test_manifest_must_expose_canonical_skills_directory(self) -> None:
        for value in (None, "skills", "./other/"):
            with self.subTest(value=value):
                self.manifest["skills"] = value
                self.write_manifest()

                self.assert_failure_contains(
                    "plugin must expose the canonical ./skills/ directory",
                    self.validate(),
                )

    def test_manifest_interface_must_be_an_object_without_crashing(self) -> None:
        for value in (None, [], "interface"):
            with self.subTest(value=value):
                self.manifest["interface"] = value
                self.write_manifest()

                failures = self.validate()

                self.assert_failure_contains("plugin interface must be a JSON object", failures)

    def test_manifest_must_have_nonempty_default_prompts(self) -> None:
        for value in (None, "prompt", []):
            with self.subTest(value=value):
                self.manifest["interface"] = {"defaultPrompt": value}
                self.write_manifest()

                self.assert_failure_contains(
                    "plugin must provide at least one default prompt",
                    self.validate(),
                )

    def test_every_manifest_prompt_must_invoke_codex_staff(self) -> None:
        invalid_prompt_lists = (["coordinate this task"], [1], ["$codex-staff okay", None])
        for value in invalid_prompt_lists:
            with self.subTest(value=value):
                self.manifest["interface"] = {"defaultPrompt": value}
                self.write_manifest()

                self.assert_failure_contains(
                    "every plugin default prompt must explicitly invoke $codex-staff",
                    self.validate(),
                )

    def test_missing_skills_root_is_a_validation_failure(self) -> None:
        shutil.rmtree(self.root / "skills")

        failures = self.validate()

        self.assert_failure_contains("skills", failures)
        self.assert_failure_contains("no released skills found", failures)

    def test_skills_root_rejects_files(self) -> None:
        (self.root / "skills" / "README.md").write_text("not a skill", encoding="utf-8")

        failures = self.validate()

        self.assert_failure_contains(
            "skills/README.md: skills/ may contain only released skill directories",
            failures,
        )

    def test_skills_root_rejects_orphan_directories(self) -> None:
        (self.root / "skills" / "orphan" / "agents").mkdir(parents=True)

        failures = self.validate()

        self.assert_failure_contains(
            "skills/orphan: released skill directory must contain SKILL.md",
            failures,
        )

    def test_skills_root_rejects_nested_skill_layouts(self) -> None:
        nested_skill = self.skill_directory / "examples" / "nested" / "SKILL.md"
        nested_skill.parent.mkdir(parents=True)
        nested_skill.write_text("nested release", encoding="utf-8")

        failures = self.validate()

        self.assert_failure_contains(
            "skills/codex-staff/examples/nested/SKILL.md: nested skill layouts are not allowed",
            failures,
        )

    def test_skill_requires_opening_frontmatter_delimiter(self) -> None:
        self.skill_path.write_text("# Codex Staff\n", encoding="utf-8")

        self.assert_failure_contains("missing opening YAML delimiter", self.validate())

    def test_skill_requires_closing_frontmatter_delimiter(self) -> None:
        self.skill_path.write_text("---\nname: codex-staff\n", encoding="utf-8")

        self.assert_failure_contains("missing closing YAML delimiter", self.validate())

    def test_skill_frontmatter_must_be_a_mapping(self) -> None:
        self.skill_path.write_text("---\n- codex-staff\n---\n", encoding="utf-8")

        self.assert_failure_contains("frontmatter must be a mapping", self.validate())

    def test_skill_frontmatter_must_be_valid_yaml(self) -> None:
        self.skill_path.write_text("---\nname: [\n---\n", encoding="utf-8")

        failures = self.validate()

        self.assert_failure_contains("skills/codex-staff/SKILL.md", failures)

    def test_skill_name_must_match_parent_directory(self) -> None:
        self.write_skill(name="another-skill")

        self.assert_failure_contains("name must match parent directory", self.validate())

    def test_skill_name_must_use_release_naming_pattern(self) -> None:
        self.write_skill(name="Codex_Staff")

        self.assert_failure_contains("invalid skill name", self.validate())

    def test_skill_license_must_be_mit(self) -> None:
        self.write_skill(license_value="Apache-2.0")

        self.assert_failure_contains("expected license: MIT", self.validate())

    def test_missing_openai_yaml_is_a_validation_failure(self) -> None:
        self.openai_path.unlink()

        failures = self.validate()

        self.assert_failure_contains("skills/codex-staff/agents/openai.yaml", failures)

    def test_openai_yaml_must_be_valid_yaml(self) -> None:
        self.openai_path.write_text("interface: [", encoding="utf-8")

        failures = self.validate()

        self.assert_failure_contains("skills/codex-staff/agents/openai.yaml", failures)

    def test_openai_yaml_must_be_a_mapping(self) -> None:
        for value in ("- interface", "null"):
            with self.subTest(value=value):
                self.openai_path.write_text(value, encoding="utf-8")

                self.assert_failure_contains("missing interface mapping", self.validate())

    def test_openai_yaml_interface_must_be_a_mapping(self) -> None:
        for value in ("interface: null", "interface: []"):
            with self.subTest(value=value):
                self.openai_path.write_text(value, encoding="utf-8")

                self.assert_failure_contains("missing interface mapping", self.validate())

    def test_openai_default_prompt_must_invoke_matching_skill(self) -> None:
        for value in (None, 1, "Use the skill.", "Use $another-skill now."):
            with self.subTest(value=value):
                self.write_openai_yaml(value)

                self.assert_failure_contains(
                    "default_prompt must explicitly invoke $codex-staff",
                    self.validate(),
                )

    def test_unfinished_marker_is_rejected(self) -> None:
        marker = "[" + "TODO: replace me]"
        (self.root / "README.md").write_text(marker, encoding="utf-8")

        failures = self.validate()

        self.assert_failure_contains("README.md: unfinished scaffold placeholder", failures)

    def test_unfinished_marker_in_ignored_directory_is_ignored(self) -> None:
        marker = "[" + "TODO: replace me]"
        ignored_file = self.root / ".git" / "notes.md"
        ignored_file.parent.mkdir()
        ignored_file.write_text(marker, encoding="utf-8")

        self.assertEqual([], self.validate())


if __name__ == "__main__":
    unittest.main()
