# Harsh's Agent Skills

Focused workflows for deliberate agent engineering.

[![CI](https://github.com/hrsh22/skills/actions/workflows/ci.yml/badge.svg)](https://github.com/hrsh22/skills/actions/workflows/ci.yml)
[![GitHub release](https://img.shields.io/github/v/release/hrsh22/skills?display_name=tag)](https://github.com/hrsh22/skills/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![skills.sh](https://img.shields.io/badge/skills.sh-codex--staff-111827)](https://skills.sh/hrsh22/skills/codex-staff)

This repository contains small, inspectable agent skills that solve specific workflow problems. Each released skill has an explicit compatibility boundary and shares one source between standalone installation and plugin packaging.

The project is independent and is not affiliated with or endorsed by OpenAI.

## Skills

### Codex Staff

A Codex workflow that selects models and reasoning effort for implementation, consequential decisions, and review.

A coding task can include routine discovery, straightforward implementation, difficult design decisions, and final review. Those assignments do not need the same model or the same reasoning budget.

Codex Staff uses a Sol Medium coordinator and Sol workers for most execution. It brings in Astra for consequential design, difficult specialist implementation, and review. The coordinator retains requirements, integration, and final validation.

The goal is to limit unnecessary use of the strongest model while preserving careful judgment where mistakes would cause substantial rework. Cost, allowance, and quality improvements have not yet been measured.

## Install

Install the editable skill with the open Skills CLI:

```bash
npx skills@latest add hrsh22/skills --skill codex-staff
```

Choose the target agent and project or global scope when prompted. For a non-interactive global Codex installation:

```bash
npx skills@latest add hrsh22/skills --skill codex-staff --agent codex --global --yes
```

The repository also includes a native Codex plugin manifest. Public plugin-directory installation will be documented after that distribution path has been submitted and verified. Choose one installation route when both become available; installing both can expose the same skill twice.

## Use

Select **Sol Medium** as the main model in Codex, then invoke the skill with a task:

```text
$codex-staff implement the account export flow and verify it end to end
```

To stop staff created by the current invocation and continue the task directly:

```text
$codex-staff off
```

The skill cannot change the running main model. If the requested model or delegation controls are unavailable, it reports the limitation and continues directly when that remains useful.

### How work is staffed

| Assignment | Default staffing |
| --- | --- |
| File discovery, narrow source checks | Sol Low scout |
| Routine implementation | Sol Medium worker |
| Difficult debugging or implementation | Sol High worker |
| Consequential design and architecture | Astra Medium lead |
| Subtle correctness or specialist work | Astra High specialist |
| Consequential review | Astra Medium reviewer |

Small edits can remain with the coordinator. Delegation is used when a bounded assignment adds useful capacity, not merely because multiple agents are available.

## Compatibility

Codex Staff currently targets Codex environments that provide:

- a user-selected Sol coordinator;
- subagent spawning with explicit model and reasoning-effort selection;
- the `gpt-5.6-sol` and `gpt-6-astra` model identifiers;
- shared workspace access and agent lifecycle controls.

The workflow principle may transfer to other agent systems, but other hosts and model profiles are not yet supported claims. See [validation and evidence](docs/validation.md).

## Repository structure

```text
skills/
  codex-staff/
    SKILL.md
    agents/openai.yaml
.codex-plugin/plugin.json
```

`skills/` contains released skills targeting the documented Codex runtime. See [validation and evidence](docs/validation.md) for verified behavior and installation paths. Draft, experimental, or host-incompatible work does not belong there.

## Contributing

Issues and focused pull requests are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before proposing behavioral changes. Security reports should follow [SECURITY.md](SECURITY.md).

## Releases

The collection uses Semantic Versioning and one release version across all bundled skills. See [the release process](docs/releasing.md) and [CHANGELOG.md](CHANGELOG.md).

## License

[MIT](LICENSE) © 2026 Harsh Gupta.
