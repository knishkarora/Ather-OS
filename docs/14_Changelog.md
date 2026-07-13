# Changelog

[[README|Knowledge Base Home]] > Changelog

This changelog records repository state changes that are visible from the audited files.

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
