# Releasing

The repository uses one Semantic Version for the plugin collection and all bundled skills.

During `0.x`:

- patch releases fix or clarify documented behavior without changing the supported workflow;
- minor releases add skills, supported profiles, invocation behavior, or substantial routing changes.

## Release checklist

1. Move relevant entries from `Unreleased` into a dated version in `CHANGELOG.md`.
2. Set the same version in `.codex-plugin/plugin.json`.
3. Run all structural and behavioral checks in `docs/validation.md`.
4. Commit the verified release state.
5. Create an annotated tag: `git tag -a vX.Y.Z -m "vX.Y.Z"`.
6. Push the branch and tag. The release workflow validates the tag, packages the repository, writes a SHA-256 checksum, and creates the GitHub release.
7. Verify installation from GitHub and the published skills.sh entry before announcing the release.
8. Confirm GitHub private vulnerability reporting remains enabled so the contact path in `SECURITY.md` is available.

Release notes should state the affected skills, observable behavior changes, compatibility changes, migrations, and known limitations.
