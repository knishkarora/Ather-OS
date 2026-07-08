# Changelog

[[README|Knowledge Base Home]] > Changelog

This changelog records repository state changes that are visible from the audited files.

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
