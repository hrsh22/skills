# Repository guidance

## Released content

`skills/` contains only released skills targeting the documented Codex runtime. Keep drafts and host-incompatible skills outside this directory. Every skill name must match its parent directory and use lowercase letters, digits, and hyphens. Use `docs/validation.md` as the source of truth for verified behavior and installation paths.

## Skill changes

Keep `SKILL.md` focused on behavior needed in every invocation. Put conditional detail in a directly linked reference. Preserve one source of truth, explicit authorization boundaries, and checkable completion criteria. Update `agents/openai.yaml`, README usage, validation scenarios, and the changelog when public behavior changes.

## Verification

Install `requirements-dev.txt`, run `python -m unittest discover -s tests`, `python scripts/validate_repo.py`, the Agent Skills reference validator for every changed skill, and `npx skills@1.5.25 add . --list`. Exercise behavioral changes in a clean supported Codex session before claiming them verified.

## Releases

The version in `.codex-plugin/plugin.json` is the collection version. A release tag is exactly `v<version>`. Do not tag until CI passes, every changed behavior passes its documented scenario, and other unexercised paths are recorded as known limitations.
