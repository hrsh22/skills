# Validation and evidence

Codex Staff is instruction-driven. Structural checks catch packaging mistakes; behavioral scenarios test whether the instructions produce the intended staffing decisions.

## Structural checks

Run from the repository root:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m unittest discover -s tests
.venv/bin/python scripts/validate_repo.py
.venv/bin/agentskills validate skills/codex-staff
npx skills@1.5.25 add . --list
```

Before a release, perform a clean installation from the exact commit being tagged. If public Codex plugin-directory distribution is in scope, also run the validator required by its submission process and record the tool and version used.

## Behavioral scenarios

Record the Codex version, available models, coordinator model and effort, roles actually spawned, elapsed time, validation outcome, and any user corrections.

| Scenario | Expected behavior |
| --- | --- |
| Small documentation correction | Coordinator handles it directly and validates proportionately. |
| Routine independent implementation | Sol workers receive bounded, non-overlapping ownership. |
| Consequential architecture choice | Astra judgment is requested before dependent implementation. |
| Difficult unresolved correctness issue | A suitable specialist investigates with primary evidence. |
| Unavailable requested model | The coordinator reports the limitation and continues directly only when useful. |
| `codex-staff off` | Only this invocation's agents stop; returned findings remain available, the coordinator continues the task directly, and staffing remains off until another explicit invocation. Any stop limitation is disclosed. |
| Long task with context pressure | A private, ignored worklog preserves decisions and active ownership without exposing machine-specific paths. |

To exercise `codex-staff off`, use a clean supported session with one finding already returned, one agent from the invocation still running, and an unrelated agent running outside the invocation. After `$codex-staff off`, verify that the owned running agent stops, the unrelated agent remains active, the returned finding remains available, direct work continues, and no staff is created until another explicit invocation. Record the loaded commit, runtime and model settings, agent identifiers, lifecycle results, and continuation evidence.

### Version 0.1.0 release-candidate run

Run on 2026-09-10 in the Codex harness; the product build number was not exposed. The coordinator was `gpt-5.6-sol` at medium effort, and both documented model families and explicit effort selection were available.

| Scenario | Observed staffing and result | Status |
| --- | --- | --- |
| Small documentation correction | The coordinator corrected release documentation and ran focused structural checks directly. | Passed |
| Routine independent implementation | A Sol Medium worker authored the skill package under bounded file ownership; the coordinator integrated and validated it. | Passed |
| Consequential architecture choice | An Astra Medium lead selected the public naming, collection shape, compatibility boundary, and initial version before dependent implementation. | Passed |
| Consequential review | A separate Astra Medium reviewer inspected the release candidate and returned two blocking findings with file-and-line evidence; both were corrected before release. | Passed |
| Long task with context pressure | A private ignored worklog preserved the objective, changed naming decision, validation state, and active next steps across context compaction. | Passed |
| Difficult unresolved correctness issue | No qualifying issue occurred during this run. | Not exercised |
| Unavailable requested model | All requested routes were available during this run. | Not exercised |
| `$codex-staff off` | The workflow was not stopped during this run. | Not exercised |

These results establish a successful release-candidate use, not comparative performance or universal routing quality. The unexercised failure and stop paths remain documented expectations rather than verified claims.

### Version 0.1.0 exact-tag installation

On 2026-09-10, a project-scoped installation was performed from a fresh temporary directory:

```bash
npx --yes skills@1.5.25 add https://github.com/hrsh22/skills/tree/v0.1.0 --skill codex-staff --agent codex --yes
```

Skills CLI resolved the source to `https://github.com/hrsh22/skills.git @ v0.1.0`, discovered one skill, and completed installation to `.agents/skills/codex-staff`. The installed `SKILL.md` and `agents/openai.yaml` were byte-identical to their tagged versions, verified with `cmp` against `git show v0.1.0:<path>`. The tag resolves to commit `4fc8b4a486569ccd4a77eb974baff9bbced1436e`.

This verifies standalone installation of the tagged files. Public Codex plugin-directory installation remains pending. It does not exercise unavailable-model handling or `$codex-staff off`.

### Version 0.1.1 stop-control run

Run on 2026-09-10 in a clean supported Codex session using the pre-release worktree based on commit `01d74f4d59a791ddf8595a552450c96c181d230f`. The product build number and exact coordinator setting were not reported.

| Check | Observed result | Status |
| --- | --- | --- |
| Returned finding | The scout completed with marker `OFF-MARKER-7319`. | Passed |
| Owned running agent | Worker `/root/bounded_wait_worker_sol_med` was interrupted successfully. | Passed |
| Isolation and continuation | The user confirmed that unrelated work remained active, the coordinator continued directly, and no new staff was created. | Passed |
| Stop limitations | No agent failed to stop. | Passed |

No substitutions or file changes occurred during the scenario. This run exercises `$codex-staff off`; unavailable-model handling remains unexercised.

## Comparative evidence

Claims about cost, allowance usage, speed, or quality require matched tasks and acceptance criteria. Compare direct Sol, direct Astra, and Codex Staff. Report only metrics the environment exposes, distinguish measurements from impressions, and include coordination overhead and failed runs.

No comparative savings claim is established.
