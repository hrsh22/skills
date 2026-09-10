#!/usr/bin/env python3
"""Validate repository-level skill and Codex plugin invariants."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER_PATTERN = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
IGNORED_DIRECTORIES = {".git", ".venv", "__pycache__", "dist", "node_modules"}


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def load_frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing opening YAML delimiter")
    try:
        _, frontmatter, _ = text.split("---", 2)
    except ValueError as exc:
        raise ValueError("missing closing YAML delimiter") from exc
    value = yaml.safe_load(frontmatter)
    if not isinstance(value, dict):
        raise ValueError("frontmatter must be a mapping")
    return value


def validate(expected_tag: str | None) -> list[str]:
    failures: list[str] = []
    manifest_path = ROOT / ".codex-plugin" / "plugin.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{manifest_path}: {exc}"]

    if manifest.get("name") != "hrsh22-skills":
        fail("unexpected Codex plugin identifier", failures)

    version = manifest.get("version")
    if not isinstance(version, str) or not SEMVER_PATTERN.fullmatch(version):
        fail("plugin version must be valid Semantic Versioning", failures)
    if expected_tag and expected_tag != f"v{version}":
        fail(f"tag {expected_tag!r} does not match plugin version v{version}", failures)

    skills_value = manifest.get("skills")
    if skills_value != "./skills/":
        fail("plugin must expose the canonical ./skills/ directory", failures)

    skills_root = ROOT / "skills"
    skill_files = sorted(skills_root.glob("*/SKILL.md"))
    if not skill_files:
        fail("no released skills found under skills/", failures)

    for skill_file in skill_files:
        skill_dir = skill_file.parent
        try:
            metadata = load_frontmatter(skill_file)
        except (OSError, ValueError, yaml.YAMLError) as exc:
            fail(f"{skill_file.relative_to(ROOT)}: {exc}", failures)
            continue

        name = metadata.get("name")
        if name != skill_dir.name:
            fail(f"{skill_file.relative_to(ROOT)}: name must match parent directory", failures)
        if not isinstance(name, str) or not NAME_PATTERN.fullmatch(name):
            fail(f"{skill_file.relative_to(ROOT)}: invalid skill name", failures)
        if metadata.get("license") != "MIT":
            fail(f"{skill_file.relative_to(ROOT)}: expected license: MIT", failures)

        openai_yaml = skill_dir / "agents" / "openai.yaml"
        try:
            openai_data = yaml.safe_load(openai_yaml.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as exc:
            fail(f"{openai_yaml.relative_to(ROOT)}: {exc}", failures)
            continue
        if not isinstance(openai_data, dict) or not isinstance(openai_data.get("interface"), dict):
            fail(f"{openai_yaml.relative_to(ROOT)}: missing interface mapping", failures)
            continue

        default_prompt = openai_data["interface"].get("default_prompt")
        if not isinstance(default_prompt, str) or not default_prompt.startswith(f"Use ${name} "):
            fail(
                f"{openai_yaml.relative_to(ROOT)}: default_prompt must explicitly invoke ${name}",
                failures,
            )

    plugin_prompts = manifest.get("interface", {}).get("defaultPrompt", [])
    if not isinstance(plugin_prompts, list) or not plugin_prompts:
        fail("plugin must provide at least one default prompt", failures)
    elif any(not isinstance(prompt, str) or not prompt.startswith("$codex-staff ") for prompt in plugin_prompts):
        fail("every plugin default prompt must explicitly invoke $codex-staff", failures)

    repository_text = [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and not IGNORED_DIRECTORIES.intersection(path.relative_to(ROOT).parts)
        and path.suffix in {".md", ".json", ".yaml", ".yml", ".py"}
    ]
    unfinished_marker = "[" + "TODO:"
    for path in repository_text:
        if unfinished_marker in path.read_text(encoding="utf-8"):
            fail(f"{path.relative_to(ROOT)}: unfinished scaffold placeholder", failures)

    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", help="release tag expected to match the plugin version")
    args = parser.parse_args()

    failures = validate(args.tag)
    if failures:
        for failure in failures:
            print(f"ERROR: {failure}", file=sys.stderr)
        return 1

    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
