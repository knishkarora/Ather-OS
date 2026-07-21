# Architecture

[[README|Knowledge Base Home]] > Architecture

Ather OS is structured as a future full-stack system with a Python [[Backend]] execution engine and a future [[Frontend]] dashboard. The current repository implements a local backend path from HTTP workflow submission through validation, scheduling, deterministic provider execution, event persistence, and replay-backed status retrieval.

## Current Architecture

```mermaid
flowchart TD
    Docs["Root vision docs"] --> Backend["backend/ Python package"]
    Docs --> Frontend["frontend/ placeholder"]
    Backend --> DAG["dag/models.py"]
    Backend --> Validator["dag/validators.py"]
    Backend --> Queue["queue/"]
    Backend --> API["api/app.py"]
    Backend --> Provider["providers/"]
    Backend --> Worker["worker/"]
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
    API --> Lifecycle
    API --> Worker
    Worker --> Provider
    Lifecycle --> State
    State --> Events["events.py"]
    State --> Store["store.py"]
    State --> SQLite["sqlite.py"]
    Checkpoint --> Projections["models.py"]
    Checkpoint --> Replay["replay.py"]
```

The active code paths include [[DAG Models]], structural validation under [[DAG Validator]], append-only event persistence under [[State Store]], event replay under [[Checkpoint Engine]], local in-memory task scheduling under [[Queue Broker]], a deterministic provider, a sequential [[Worker]], and a FastAPI application. [[Queue Lifecycle Service]] connects queue transitions with the event store; the API composes those pieces into a synchronous local request flow. There is still no provider router or frontend application code.

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

- [[04_APIs|API Layer]]: implemented in `backend/src/ather_os/api/app.py` with submission and status routes.
- [[Response Cache]]: package exists at `backend/src/ather_os/cache`, but no interface or implementation exists.
- [[Checkpoint Engine]]: implemented with workflow/task status projection models and pure event replay logic.
- [[Configuration]]: package exists at `backend/src/ather_os/config`, but no settings model or environment loading exists.
- [[DAG Models]]: implemented in `backend/src/ather_os/dag/models.py`.
- [[DAG Validator]]: implemented in `backend/src/ather_os/dag/validators.py`.
- [[Provider Router]]: `TaskProvider` protocol and deterministic `MockProvider` are implemented; routing is not.
- [[Queue Broker]]: implemented with a minimal protocol, dependency-aware in-memory queue, and [[Queue Lifecycle Service]] for local event emission.
- [[State Store]]: implemented with lifecycle event models, a minimal storage protocol, and a local SQLite event store.
- [[Worker]]: `WorkflowWorker` executes queued tasks sequentially through a provider.

## Data Flow

Current data flow starts when the API receives a [[Workflow Model]]. [[Queue Lifecycle Service]] validates and submits it to [[Queue Broker]], appends lifecycle events to [[State Store]], and lets [[Worker]] claim and execute ready tasks with the deterministic provider. Stored events are replayed by [[Checkpoint Engine]] into workflow/task snapshots returned by the API.

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

- httpx
- Pytest

Pydantic, FastAPI, and the Python standard library are used by the current source code. The [[State Store]] uses the standard `sqlite3` module. Uvicorn runs the local API, and httpx supports API tests.

## Related

- [[00_Project_Overview|Project Overview]]
- [[02_Folder_Structure|Folder Structure]]
- [[03_Database|Database]]
- [[04_APIs|APIs]]
- [[06_State_Management|State Management]]
- [[10_Current_Status|Current Status]]
