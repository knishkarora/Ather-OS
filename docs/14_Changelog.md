# Changelog

[[README|Knowledge Base Home]] > Changelog

This changelog records repository state changes that are visible from the audited files.

## 2026-07-23

- Added `ProviderRouter`, `SingleProviderRouter`, and `RoutedTaskProvider` to
  separate provider selection from worker execution without changing local
  one-provider behavior; added focused router tests.
- Added a process-local `InMemoryResponseCache` and `CachedTaskProvider` around provider execution.
- Cache keys cover output-affecting task fields, successful outputs are reused across equivalent tasks, and provider failures are not cached.
- Added cache unit tests and API wiring coverage; the backend suite now has 71 passing tests.
- Updated architecture, components, API, state-management, roadmap, status, task, and decision documentation for the completed caching slice.
- Added `WorkflowRecovery` to rebuild an in-memory workflow queue from persisted lifecycle events and resume unfinished local workflows.
- Requeues interrupted running tasks with incremented attempts, preserves completed outputs, and writes missing terminal workflow events after interrupted finalization.
- Added `POST /workflows/{workflow_id}/recover` and focused API/recovery tests.
- Updated the knowledge base and journey documentation for the completed recovery slice.

## 2026-07-21

- Added the FastAPI application in `backend/src/ather_os/api/app.py` with synchronous workflow submission and persisted replay-backed status routes.
- Added API tests for successful execution, status retrieval after app recreation, invalid graphs, missing workflows, and duplicate IDs.
- Added `httpx` as an explicit development dependency for FastAPI endpoint tests.
- Updated the backend README and API, roadmap, status, tasks, bugs, and journey documentation for the completed API slice.

## 2026-07-21

- Added `TaskProvider` and deterministic `MockProvider` under `backend/src/ather_os/providers/`.
- Added `WorkflowWorker` under `backend/src/ather_os/worker/` to execute dependency-ready tasks through [[Queue Lifecycle Service]].
- Added terminal task/workflow failure recording and final workflow completion recording to [[Queue Lifecycle Service]].
- Added replay-backed `WorkflowStatusQuery` for current workflow/task snapshots from a [[State Store]].
- Added execution tests covering dependency ordering, successful completion, and provider failure; the backend suite now has 57 passing tests.
- Updated roadmap, tasks, current status, and bugs documentation to reflect the completed local execution slice.

## 2026-07-19

- Added [[Queue Lifecycle Service]] in `backend/src/ather_os/queue/lifecycle.py` to coordinate local queue transitions with append-only lifecycle events.
- Added pytest coverage for submission, task claim/completion, dependency unblocking event order, and invalid completion handling.
- Updated the knowledge base so the next engineering step is an in-process [[Worker]] loop using the lifecycle service.
- Added the minimal [[Queue Broker]] protocol in `backend/src/ather_os/queue/broker.py`.
- Added dependency-aware `InMemoryQueueBroker` in `backend/src/ather_os/queue/memory.py` using only standard Python data structures.
- Added pytest coverage for queue submission, task claiming, dependency unblocking, duplicate workflow submission, and unknown workflow/task errors.
- Added [[Queue Broker]] documentation and updated architecture, components, state management, current status, and tasks docs so the next backend step is worker integration.

## 2026-07-13

- Added typed workflow/task lifecycle events in `backend/src/ather_os/state/events.py`.
- Added the minimal [[State Store]] protocol in `backend/src/ather_os/state/store.py`.
- Added `SQLiteStateStore` in `backend/src/ather_os/state/sqlite.py` using Python's standard `sqlite3` module.
- Added pytest coverage for lifecycle event validation, event JSON parsing, SQLite append ordering, workflow filtering, persistence across store instances, and duplicate event IDs.
- Added [[State Store]] documentation and updated architecture, database, state management, roadmap, tasks, decisions, current status, and folder structure docs to reflect the implemented persistence foundation.
- Added [[Checkpoint Engine]] projection models in `backend/src/ather_os/checkpoint/models.py`.
- Added `replay_workflow(events)` in `backend/src/ather_os/checkpoint/replay.py`.
- Added pytest coverage for workflow submission replay, task queue/start/completion/failure replay, workflow completion/failure replay, and invalid event logs.
- Added [[Checkpoint Engine]] documentation and updated the knowledge base so the next backend step is now [[Queue Broker]] scheduling.

## 2026-07-09

- Renamed and reformatted the project master document as `AtherOS_Project_Master_Document.md` for easier Markdown viewing.
- Added pytest coverage for [[DAG Models]] field constraints in `backend/tests/test_dag_models.py`.
- Covered task type and quality tier values, default quality, prompt and goal minimum lengths, token bounds, retry bounds, and workflow task count limits.
- Updated [[10_Current_Status|Current Status]] and [[11_Tasks|Tasks]] so the knowledge base reflects the expanded DAG foundation test coverage.
- Added sample workflow JSON files under `backend/samples/`.
- Added a minimal workflow validation command in `backend/src/ather_os/dag/validate_workflow.py`.
- Added pytest coverage for valid and invalid workflow samples in `backend/tests/test_validate_workflow_command.py`.
- Updated [[09_Roadmap|Roadmap]] and [[11_Tasks|Tasks]] so the next backend step is now the local [[State Store]] interface.

## 2026-07-08

- Added [[DAG Validator]] in `backend/src/ather_os/dag/validators.py`.
- Added `DagValidationError` and `validate_workflow_graph(workflow: Workflow) -> None`.
- Added pytest coverage for duplicate task IDs, unknown dependencies, self-dependencies, dependency cycles, multiple roots, disconnected roots, and valid connected DAGs.
- Updated documentation to mark DAG structural validation as implemented.
- Added `/docs` Obsidian knowledge base.
- Documented actual current implementation across overview, architecture, folder structure, database, APIs, components, state management, authentication, UI, roadmap, current status, tasks, bugs, decisions, and changelog.
- Recorded that [[DAG Models]] are the only substantive implemented domain logic.
- Recorded that [[04_APIs|APIs]], [[03_Database|Database]], [[Checkpoint Engine]], [[Response Cache]], [[Provider Router]], [[Queue Broker]], [[State Store]], [[Worker]], [[Frontend]], and [[07_Authentication|Authentication]] are not implemented yet.

## Earlier Repository State

Based on `JOURNEY.md`, the initial project shape was created on Sunday, 17 May:

- Root `README.md`.
- `JOURNEY.md`.
- `backend/` and `frontend/` folders.
- `backend/pyproject.toml`.
- Backend package skeleton under `backend/src/ather_os/`.
- Initial [[DAG Models]] in `backend/src/ather_os/dag/models.py`.
- Backend virtual environment and installed dependencies.

## Related

- [[10_Current_Status|Current Status]]
- [[11_Tasks|Tasks]]
- [[13_Decisions|Decisions]]
