# Validation and evidence

Codex Staff is instruction-driven. Structural checks catch packaging mistakes; behavioral scenarios test whether the instructions produce the intended staffing decisions.

## Structural checks

Run from the repository root:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python scripts/validate_repo.py
.venv/bin/agentskills validate skills/codex-staff
npx skills@1.5.25 add . --list
```

Before a release, also validate the plugin with the current Codex plugin validator and perform a clean installation from the exact commit being tagged.

## Behavioral scenarios

Record the Codex version, available models, coordinator model and effort, roles actually spawned, elapsed time, validation outcome, and any user corrections.

| Scenario | Expected behavior |
| --- | --- |
| Small documentation correction | Coordinator handles it directly and validates proportionately. |
| Routine independent implementation | Sol workers receive bounded, non-overlapping ownership. |
| Consequential architecture choice | Astra judgment is requested before dependent implementation. |
| Difficult unresolved correctness issue | A suitable specialist investigates with primary evidence. |
| Unavailable requested model | The coordinator reports the limitation and continues directly only when useful. |
| `codex-staff off` | Only this invocation's active agents stop; useful findings are preserved. |
| Long task with context pressure | A private, ignored worklog preserves decisions and active ownership without exposing machine-specific paths. |

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

## Comparative evidence

Claims about cost, allowance usage, speed, or quality require matched tasks and acceptance criteria. Compare direct Sol, direct Astra, and Codex Staff. Report only metrics the environment exposes, distinguish measurements from impressions, and include coordination overhead and failed runs.

No comparative savings claim is established in version 0.1.0.
