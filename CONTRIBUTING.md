# Contributing

Thanks for helping improve these skills. Contributions should make observable agent behavior more reliable without widening a skill beyond its stated job.

## Before opening a change

1. Open an issue for a new skill or consequential workflow change.
2. Describe the request or failure that motivates the change.
3. Keep one canonical source for every instruction; use references only for conditional detail.
4. Preserve authorization boundaries and avoid environment-specific claims that have not been tested.
5. Add or update a behavioral scenario in `docs/validation.md` when behavior changes.

## Local checks

Create a virtual environment and install the validation dependencies:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
```

Run the repository and Agent Skills validators:

```bash
.venv/bin/python scripts/validate_repo.py
.venv/bin/agentskills validate skills/codex-staff
npx skills@1.5.25 add . --list
```

Also exercise the affected workflow in a clean Codex session. Structural validation cannot prove that an instruction set makes good decisions.

## Pull requests

Keep pull requests focused. Include:

- the behavior being changed and why;
- the scenarios exercised;
- actual validation output;
- compatibility or migration consequences;
- documentation updates for user-visible changes.

By contributing, you agree that your contribution is licensed under the repository's MIT License.
