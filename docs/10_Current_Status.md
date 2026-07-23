# Current Status

[[README|Knowledge Base Home]] > Current Status

This is the audited state of the repository.

## Implemented

- Root README describing Ather OS and Phase 0 focus.
- `JOURNEY.md` with Day 1 project notes.
- Markdown product master document with long-term vision.
- Python backend project using `pyproject.toml`.
- Backend package skeleton under `backend/src/ather_os`.
- Pydantic [[DAG Models]] in `backend/src/ather_os/dag/models.py`.
- Structural [[DAG Validator]] in `backend/src/ather_os/dag/validators.py`.
- Sample workflow JSON files under `backend/samples/`.
- Minimal workflow validation command in `backend/src/ather_os/dag/validate_workflow.py`.
- Pytest coverage for [[DAG Models]] field constraints in `backend/tests/test_dag_models.py`.
- Pytest coverage for [[DAG Validator]] in `backend/tests/test_dag_validators.py`.
- Pytest coverage for sample workflow validation in `backend/tests/test_validate_workflow_command.py`.
- Typed workflow/task lifecycle event models in `backend/src/ather_os/state/events.py`.
- Minimal [[State Store]] protocol in `backend/src/ather_os/state/store.py`.
- SQLite-backed append-only event store in `backend/src/ather_os/state/sqlite.py`.
- Pytest coverage for state event validation and SQLite event persistence.
- [[Checkpoint Engine]] status projection models in `backend/src/ather_os/checkpoint/models.py`.
- [[Checkpoint Engine]] event replay in `backend/src/ather_os/checkpoint/replay.py`.
- Pytest coverage for checkpoint replay behavior and invalid event logs.
- Minimal [[Queue Broker]] protocol in `backend/src/ather_os/queue/broker.py`.
- Dependency-aware in-memory queue in `backend/src/ather_os/queue/memory.py`.
- Pytest coverage for queue submission, task claiming, dependency unblocking, duplicate workflow submissions, and unknown workflow/task errors.
- [[Queue Lifecycle Service]] in `backend/src/ather_os/queue/lifecycle.py` coordinates local queue operations with append-only lifecycle events.
- `WorkflowStatusQuery` replays stored workflow events into the current workflow/task snapshot.
- `TaskProvider` protocol and deterministic `MockProvider` implementation for local execution.
- `WorkflowWorker` runs a workflow through the queue lifecycle service, records terminal failures, and records workflow completion after the final task.
- FastAPI application with asynchronous `POST /workflows` submission, replay-backed `GET /workflows/{workflow_id}` status retrieval, and `GET /workflows/{workflow_id}/events` lifecycle inspection.
- `WorkflowRecovery` rebuilds local queue state from persisted events and resumes unfinished workflows with at-least-once semantics for interrupted running tasks.
- FastAPI `POST /workflows/{workflow_id}/recover` exposes explicit local recovery.
- Process-local response cache wraps provider execution and reuses successful outputs for equivalent tasks.
- `ProviderRouter`, `SingleProviderRouter`, and `RoutedTaskProvider` separate
  future provider selection from worker execution while preserving one local
  deterministic provider today.
- Pytest coverage for API submission, validation, persisted status retrieval, lifecycle-event inspection, missing workflows, and duplicate workflow IDs.
- Pytest coverage for workflow submission events, task claim/completion events, dependency unblocking events, final workflow completion, invalid completion handling, dependency-ordered worker execution, provider failures, and recovery of queued/running/completed/terminal states.
- Placeholder package boundary for [[Configuration]].
- Placeholder [[Frontend]] README.
- `.gitignore` for Python, local databases, env files, frontend build outputs, and editor metadata.

## Partially Completed

- [[Backend]] structure exists, but several packages still contain only docstrings.
- [[DAG Models]] validate field shapes and basic constraints.
- [[DAG Validator]] validates duplicate task IDs, unknown dependencies, self-dependencies, cycles, multiple roots, and disconnected roots.
- The validation command loads local workflow JSON and validates it, but does not execute or persist workflows.
- [[State Store]] can append and list events, [[Checkpoint Engine]] can replay listed events into workflow/task status snapshots, and `WorkflowStatusQuery` exposes that replay against a state store.
- The in-process [[Worker]] executes ready tasks sequentially with the deterministic mock provider and uses [[Queue Lifecycle Service]] to persist queue-driven lifecycle events. `WorkflowRecovery` can reconstruct that in-memory queue from persisted events when explicitly invoked.
- Test configuration exists in `pyproject.toml`, and focused DAG model, validator, and validation command tests now exist.
- A local virtual environment exists and contains installed dependencies, but the global shell PATH does not expose `pytest`.

## Missing

- Database migrations.
- Frontend app.
- Authentication.
- Environment configuration code.
- Deployment configuration.
- CI configuration.
- Tests for future API, queue, provider, worker, and cache behavior.

## Verification

Command run from `backend/`:

```powershell
.\.venv\Scripts\pytest.exe
```

Result: pytest started successfully using Python 3.12.13, collected 75 items, and all 75 tests passed.

Running plain `pytest` from the shell failed because `pytest` is not on PATH.

## Known Mismatch

`AtherOS_Project_Master_Document.md` states that Stage 0 features are built, including storage, event sourcing, checkpoint recovery, cache, mock provider, worker, and REST API. The audited source code now includes local storage, event sourcing, checkpoint replay, explicit local recovery, in-memory queue scheduling, a deterministic mock provider, a single-provider router, a local worker, and a small REST API. Automatic restart recovery and multi-provider routing remain unimplemented. Treat those remaining Stage 0 claims as aspirational or stale until code is added.

## Current Assumptions in Code

- Workflow IDs and task IDs are UUIDs.
- Workflows must contain between 1 and 20 tasks.
- Task prompts and workflow goals cannot be empty.
- Estimated tokens must be from 1 to 8000.
- Task retry count cannot be negative.
- Task quality defaults to `standard`.
- Task dependencies are represented as UUID references and can now be structurally validated with [[DAG Validator]].
- A workflow graph is expected to have exactly one root task with no dependencies.
- Workflow and task lifecycle changes are persisted as append-only events.
- SQLite events store UUIDs and timestamps as text plus the full event JSON payload.
- Checkpoint replay expects append-ordered events and starts with `workflow_submitted`.
- Workflow/task snapshots are in-memory projections, not database tables.
- The local queue keeps workflow scheduling state in memory only, while [[Queue Lifecycle Service]] appends related lifecycle events.
- A task becomes queueable only after all dependency task IDs have completed.
- The local worker executes one queued task at a time and treats a provider exception as a terminal workflow failure.
- Cached provider outputs are keyed by task type, prompt, context needs, and quality tier; they are not persisted or replayed.
- The current router always selects one provider. A multi-provider router must
  make response-cache keys provider-aware.
- Recovery preserves completed tasks, requeues queued and interrupted running tasks, and increments the attempt for re-executed tasks. It is at-least-once and is not automatic at service startup.

## Related

- [[00_Project_Overview|Project Overview]]
- [[09_Roadmap|Roadmap]]
- [[11_Tasks|Tasks]]
- [[12_Bugs|Bugs]]
- [[14_Changelog|Changelog]]
