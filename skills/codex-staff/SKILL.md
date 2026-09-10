---
name: codex-staff
description: Coordinate an explicitly requested Codex staff of Sol and Astra subagents for one task.
license: MIT
---

# Codex Staff

Coordinate a task-local staff while retaining responsibility for requirements, integration, and the final answer.

## Compatibility

Use this workflow only in a Codex runtime that exposes subagent spawning and the named `gpt-5.6-sol` and `gpt-6-astra` models with the requested reasoning efforts. This skill cannot change the model or reasoning effort of the running main agent. If the active main setting is known and differs from the user's expectation, disclose that once and coordinate with the active setting unless the user changes it.

When a requested model, effort, spawning capability, or concurrency slot is unavailable, say which route is unavailable. Choose the nearest available route only when that substitution is useful and identify it as a substitution; otherwise perform the work directly. Never claim that an unavailable route ran.

## Activation

Apply this workflow only when the user explicitly invokes `$codex-staff`, and only to the task in which it was invoked. New tasks require a new invocation. `$codex-staff off` stops active staff when the runtime permits, preserves useful findings already returned, and resumes direct work.

If another team workflow is active for the same task, replace its routing rules with this workflow unless the user explicitly asks to combine them. Preserve the user's scope, permissions, and requested outcome.

## Coordinator role

The main agent is the coordinator. It owns:

- the complete requirements and authorization boundary;
- decomposition, routing, and non-overlapping file ownership;
- decisions that span assignments;
- integration of returned work;
- proportionate final validation and the user-facing result.

Delegate substantial independent work through bounded assignments. Handle small edits, integration fixes, and work with no useful independent seam directly. Size the staff to the actual independent work and the runtime's concurrency limit.

## Routing

Choose a route from the assignment's difficulty, uncertainty, and consequences; there is no required escalation ladder.

| Role | Model | Effort | Use for |
| --- | --- | --- | --- |
| Scout | `gpt-5.6-sol` | `low` | Locate files, trace a code path, find tests, collect sources, or verify one narrow fact. |
| Worker | `gpt-5.6-sol` | `medium` | Clearly scoped implementation with established requirements. |
| Harder worker | `gpt-5.6-sol` | `high` | Difficult debugging or implementation across modules. |
| Focused specialist | `gpt-6-astra` | `low` | A narrow judgment question with clear constraints and enough evidence. |
| Design or architecture lead | `gpt-6-astra` | `medium` | Consequential ambiguity, tradeoffs, invariants, and acceptance criteria before dependent work. |
| Specialist worker | `gpt-6-astra` | `medium` | Implementation whose design judgment remains inseparable from the code. |
| Reviewer | `gpt-6-astra` | `medium` | Challenge consequential designs or implementations against requirements, failure modes, and evidence. |
| Difficult specialist | `gpt-6-astra` | `high` | Subtle correctness, hard algorithms, cross-system reasoning, or unresolved complex failures. |
| Exceptional assignment | `gpt-5.6-sol` or `gpt-6-astra` | `xhigh` | Unusually demanding work that warrants the additional reasoning; choose the model by the work. |

Use Sol for most execution and Astra for focused judgment. Route consequential uncertainty to Astra early when a wrong decision would create substantial rework. Astra Medium is the normal choice for consequential judgment; Low suits a narrow question, and High suits difficult specialist work. Use Xhigh selectively. Do not infer that a higher effort or different model guarantees lower cost or better quality.

Substantial designs, difficult correctness questions, and repeated failures can merit Astra review. Small patches need proportionate validation, not automatic specialist review. Complex research synthesis belongs with the coordinator or an Astra lead rather than automatically with a Low scout.

## Assignments and ownership

For explicit model and effort routing, spawn with `fork_turns: "none"`. Name the agent `<assignment>_<model>_<effort>` using lowercase words and underscores; use `sol` or `astra`, and `low`, `med`, `high`, or `xhigh`. Reuse an agent only while its name still describes the model, effort, and assignment.

Every assignment must include a bounded outcome or question, relevant paths or primary excerpts, constraints and permissions, known evidence and attempted fixes, and a checkable completion criterion. Keep the handoff proportional: provide decisive context, not an undifferentiated transcript or log.

Use these ownership rules:

- Scouts, design leads, and reviewers return findings and do not edit files.
- Workers receive explicit file ownership and validation criteria.
- Each delegated agent performs its assignment directly without further delegation.
- Avoid overlapping edit ownership. The coordinator waits for an owned edit to finish before editing the same files.
- While a worker runs, the coordinator handles integration, unresolved requirements, or other independent work instead of duplicating that assignment.

Missing user preferences or authorization require the user's answer, not a specialist's guess.

## Evidence handoffs

Scouts, leads, and reviewers return file-and-line references, links or citations when applicable, material uncertainties, and recommended next checks. Design leads also provide a recommended decision, tradeoffs, failure modes, and implementable acceptance criteria.

Gather the relevant code, requirements, constraints, and prior attempts before asking for judgment. Return focused excerpts and summaries from large logs, searches, or browser snapshots while keeping full artifacts available by a workspace-relative path. Include decisive errors or conflicting evidence verbatim when necessary.

Reuse a relevant agent thread for a related follow-up. Return to the design lead when new evidence challenges its decision or implementation exposes a difficult unresolved issue. Give a lead a distinct implementation assignment before asking it to edit.

## Integration and validation

The coordinator checks returned evidence, reconciles conflicts, integrates owned changes, and carries accepted decisions into final verification. Validation should match the risk and observable outcome: run focused checks for a small change and broader checks for cross-cutting or consequential work.

For implementation from an approved visual reference, compare the rendered result directly with the reference, including relevant states and interactions. When the user identifies a mismatch, update the acceptance criteria and verify the correction before widening scope.

Report which roles actually ran, the integrated result, validation performed, substitutions, and material limitations. When comparing staffing approaches, use observable outcomes, elapsed time, available usage measurements, and user corrections; label impressions as impressions and never invent savings.

## Long-running tasks

For work spanning multiple stages, substantial steering, or context compaction, keep a compact task-specific Markdown worklog. Reuse the project's established task-log location; otherwise use a unique task log under repository metadata so internal notes stay out of commits. For non-repository work, use a task-specific temporary directory. Refer to the log by a repository-relative or task-relative path rather than exposing machine-specific absolute paths.

Record only the current objective, constraints, decisions, completed work and verification, active ownership, unresolved questions, and next steps. Update it at meaningful milestones and when steering changes the plan. Preserve earlier objectives unless the user changes or cancels them, and mark superseded decisions clearly. The coordinator owns the log and incorporates staff reports.
