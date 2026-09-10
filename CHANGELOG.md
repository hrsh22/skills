# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and releases follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.1] - 2026-09-10

### Fixed

- Make release checksums portable when assets are downloaded outside the workflow's `dist/` directory.
- Clarify that `$codex-staff off` stops only the current invocation's staff and resumes direct work.
- Distinguish standalone installation evidence from pending public Codex plugin-directory verification.
- Harden repository validation with negative-path tests and stricter released-skill discovery.
- Require repository tests and complete Skills CLI discovery before CI or tagged releases pass.
- Replace the unavailable skills.sh dynamic badge with a stable badge linked to the published skill page.
- Update pinned GitHub Actions to Node 24 compatible releases.

## [0.1.0] - 2026-09-10

### Added

- `codex-staff`, an explicit Codex workflow for assignment-level model and reasoning-effort selection.
- A native Codex plugin manifest backed by the same canonical skill files.
- Repository validation, standalone discovery checks, and tag-driven GitHub releases.
- Compatibility, contribution, security, and release documentation.

[Unreleased]: https://github.com/hrsh22/skills/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/hrsh22/skills/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/hrsh22/skills/releases/tag/v0.1.0
