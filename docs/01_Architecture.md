# Architecture

[[README|Knowledge Base Home]] > Architecture

Ather OS is structured as a future full-stack system with a Python [[Backend]] execution engine and a future [[Frontend]] dashboard. The current repository implements the earliest backend domain schema layer, structural workflow graph validation, a local append-only [[State Store]] foundation, [[Checkpoint Engine]] replay, and dependency-aware in-memory [[Queue Broker]] scheduling.

## Current Architecture

```mermaid
flowchart TD
    Docs["Root vision docs"] --> Backend["backend/ Python package"]
    Docs --> Frontend["frontend/ placeholder"]
    Backend --> DAG["dag/models.py"]
    Backend --> Validator["dag/validators.py"]
    Backend --> Queue["queue/"]
    Backend --> State["state/"]
    Backend --> Checkpoint["checkpoint/"]
    DAG --> Workflow["Workflow Model"]
    Workflow --> Task["Task Model"]
    Task --> TaskType["TaskType enum"]
    Task --> QualityTier["QualityTier enum"]
    Validator --> Workflow
    Queue --> Workflow
    Queue --> Validator
    Queue --> Lifecycle["lifecycle.py"]
    Lifecycle --> State
    State --> Events["events.py"]
    State --> Store["store.py"]
    State --> SQLite["sqlite.py"]
    Checkpoint --> Projections["models.py"]
    Checkpoint --> Replay["replay.py"]
```

The active code paths are importable schema code under [[DAG Models]], structural validation under [[DAG Validator]], append-only event persistence under [[State Store]], event replay under [[Checkpoint Engine]], and local in-memory task scheduling under [[Queue Broker]]. [[Queue Lifecycle Service]] connects the queue and event store for local lifecycle operations. There is no running API app, no worker, no provider router, and no frontend application code yet.

## Intended Architecture

The package structure and project documents point to this planned design:

```mermaid
flowchart TD
    User["User"] --> API["API Layer"]
    API --> DAG["DAG Models and Validator"]
    DAG --> Queue["Queue Broker"]
    Queue --> Worker["Worker"]
    Worker --> Provider["Provider Router"]
    Provider --> Cache["Response Cache"]
    Worker --> State["State Store"]
    State --> Checkpoint["Checkpoint Engine"]
    Checkpoint --> Worker
    API --> State
    Frontend["Frontend Dashboard"] --> API
```

This diagram is architectural intent, not current runtime behavior. Today, [[DAG Models]], [[DAG Validator]], [[State Store]], and [[Checkpoint Engine]] exist as real implementation.

## Module Responsibilities

- [[04_APIs|API Layer]]: package exists at `backend/src/ather_os/api`, but contains only a docstring.
- [[Response Cache]]: package exists at `backend/src/ather_os/cache`, but no interface or implementation exists.
- [[Checkpoint Engine]]: implemented with workflow/task status projection models and pure event replay logic.
- [[Configuration]]: package exists at `backend/src/ather_os/config`, but no settings model or environment loading exists.
- [[DAG Models]]: implemented in `backend/src/ather_os/dag/models.py`.
- [[DAG Validator]]: implemented in `backend/src/ather_os/dag/validators.py`.
- [[Provider Router]]: package exists at `backend/src/ather_os/providers`, but no router or mock provider exists.
- [[Queue Broker]]: implemented with a minimal protocol, dependency-aware in-memory queue, and [[Queue Lifecycle Service]] for local event emission.
- [[State Store]]: implemented with lifecycle event models, a minimal storage protocol, and a local SQLite event store.
- [[Worker]]: package exists at `backend/src/ather_os/worker`, but no execution loop exists.

## Data Flow

Current data flow supports in-memory validation when a developer instantiates [[Workflow Model]] or [[Task Model]] through Pydantic, then calls [[DAG Validator]] to validate dependency structure. [[Queue Lifecycle Service]] submits the workflow to [[Queue Broker]] and appends its lifecycle events to [[State Store]]; it also records task claims, successful completion, and newly unblocked tasks. Stored events can be replayed by [[Checkpoint Engine]] into workflow/task snapshots. There is still no API request flow or execution loop.

Planned data flow is documented as:

1. User submits a goal through [[04_APIs|APIs]] or future [[Frontend]].
2. Orchestrator creates or receives a [[Workflow Model]].
3. Each [[Task Model]] declares dependencies and context needs.
4. [[Queue Broker]] schedules executable tasks.
5. [[Worker]] executes tasks through [[Provider Router]].
6. [[State Store]] appends task events. This append-only portion now exists locally through SQLite.
7. [[Checkpoint Engine]] replays events into workflow/task snapshots. This in-memory replay portion now exists; worker restart behavior does not.

## Dependencies

Current runtime dependencies from `backend/pyproject.toml`:

- FastAPI
- Pydantic
- Uvicorn

Current development dependency:

- Pytest

Pydantic and the Python standard library are used by the current source code. The [[State Store]] uses the standard `sqlite3` module. FastAPI and Uvicorn are installed for planned [[04_APIs|API]] work but are not imported by application code.

## Related

- [[00_Project_Overview|Project Overview]]
- [[02_Folder_Structure|Folder Structure]]
- [[03_Database|Database]]
- [[04_APIs|APIs]]
- [[06_State_Management|State Management]]
- [[10_Current_Status|Current Status]]
