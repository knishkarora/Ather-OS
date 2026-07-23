# Folder Structure

[[README|Knowledge Base Home]] > Folder Structure

This document records the audited folder structure and responsibilities.

## Root

```text
.
|-- .gitignore
|-- AtherOS_Project_Master_Document.md
|-- JOURNEY.md
|-- README.md
|-- backend/
|-- docs/
`-- frontend/
```

## Root Files

- `README.md`: project introduction, current Phase 0 focus, and top-level structure.
- `JOURNEY.md`: human learning log and checkpoint notes.
- `AtherOS_Project_Master_Document.md`: product vision, architectural principles, staged roadmap, and explanatory messaging.
- `.gitignore`: excludes Python caches, virtual environments, local databases, env files, frontend build artifacts, and editor files.

## Backend

```text
backend/
|-- README.md
|-- pyproject.toml
|-- samples/
|   |-- invalid_cycle_workflow.json
|   |-- invalid_unknown_dependency_workflow.json
|   `-- valid_research_workflow.json
|-- src/
|   |-- ather_os/
|   |   |-- __init__.py
|   |   |-- api/
|   |   |-- cache/
|   |   |-- checkpoint/
|   |   |   |-- __init__.py
|   |   |   |-- models.py
|   |   |   |-- query.py
|   |   |   `-- replay.py
|   |   |-- config/
|   |   |-- dag/
|   |   |   |-- __init__.py
|   |   |   |-- models.py
|   |   |   |-- validate_workflow.py
|   |   |   `-- validators.py
|   |   |-- providers/
|   |   |-- queue/
|   |   |   |-- __init__.py
|   |   |   |-- broker.py
|   |   |   |-- lifecycle.py
|   |   |   `-- memory.py
|   |   |-- state/
|   |   |   |-- __init__.py
|   |   |   |-- events.py
|   |   |   |-- sqlite.py
|   |   |   `-- store.py
|   |   `-- worker/
|   |       |-- __init__.py
|   |       |-- loop.py
|   |       `-- recovery.py
|   `-- ather_os_backend.egg-info/
`-- tests/
    |-- __init__.py
    |-- test_checkpoint_replay.py
    |-- test_dag_models.py
    |-- test_dag_validators.py
    |-- test_sqlite_state_store.py
    |-- test_state_events.py
    `-- test_validate_workflow_command.py
```

`backend/pyproject.toml` defines a Python 3.11+ package named `ather-os-backend` using setuptools package discovery from `src`.

`backend/src/ather_os/dag/models.py` is the implemented domain model file. `backend/src/ather_os/dag/validators.py` validates workflow graph structure. `backend/src/ather_os/dag/validate_workflow.py` loads workflow JSON files and validates both model constraints and DAG structure.

`backend/src/ather_os/state/` now contains the local [[State Store]] foundation: lifecycle event models, a minimal storage protocol, and a SQLite-backed append-only event store.

`backend/src/ather_os/checkpoint/` now contains the local [[Checkpoint Engine]] replay foundation: projection models, status enums, and a pure event replay function.

`backend/src/ather_os/queue/` now contains the local [[Queue Broker]] foundation: a minimal scheduling protocol, dependency-aware in-memory queue, and [[Queue Lifecycle Service]] that emits local lifecycle events through [[State Store]].

`backend/src/ather_os_backend.egg-info/` appears to be generated package metadata from an editable install and is ignored by `.gitignore`.

`backend/.venv/` and `backend/.pytest_cache/` exist locally but are ignored by `.gitignore`; they are not project source.

`backend/samples/` contains one valid workflow JSON file and two intentionally invalid workflow JSON files used by tests and manual validation.

`backend/tests/` contains focused tests for DAG models, DAG validators, the sample workflow validation command, state events, the SQLite state store, checkpoint replay, in-memory queue scheduling, queue lifecycle coordination, worker execution, recovery, and the API.

## Frontend

```text
frontend/
`-- README.md
```

The [[Frontend]] is a placeholder. There is no `package.json`, framework configuration, component tree, routing setup, build pipeline, or UI source code.

## Docs

The `docs/` folder is this Obsidian knowledge base. It is the single source of truth for future AI-assisted development and should be updated whenever implementation changes.

## Relationship Map

- [[Backend]] owns [[DAG Models]], [[DAG Validator]], sample workflow JSON files, the workflow validation command, the local [[State Store]] foundation, the local [[Checkpoint Engine]] replay foundation, and the local [[Queue Broker]] scheduling foundation today.
- [[Frontend]] depends on future [[04_APIs|APIs]], but no dependency exists in code yet.
- [[04_APIs|APIs]] will depend on [[DAG Models]] when implemented.
- [[State Store]] has lifecycle event models, a storage protocol, and a SQLite implementation.
- [[Checkpoint Engine]] has status projection models and event replay logic.
- [[Queue Broker]] has a scheduling protocol, dependency-aware in-memory implementation, and event-coordinating [[Queue Lifecycle Service]].
- [[Response Cache]] and [[Provider Router]] have local implementations. [[Worker]] has local execution and explicit recovery implementations.

## Related

- [[00_Project_Overview|Project Overview]]
- [[01_Architecture|Architecture]]
- [[10_Current_Status|Current Status]]
