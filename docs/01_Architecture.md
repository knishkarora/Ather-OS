# Architecture

[[README|Knowledge Base Home]] > Architecture

Ather OS is structured as a future full-stack system with a Python [[Backend]] execution engine and a future [[Frontend]] dashboard. The current repository implements the earliest backend domain schema layer and structural workflow graph validation.

## Current Architecture

```mermaid
flowchart TD
    Docs["Root vision docs"] --> Backend["backend/ Python package"]
    Docs --> Frontend["frontend/ placeholder"]
    Backend --> DAG["dag/models.py"]
    Backend --> Validator["dag/validators.py"]
    DAG --> Workflow["Workflow Model"]
    Workflow --> Task["Task Model"]
    Task --> TaskType["TaskType enum"]
    Task --> QualityTier["QualityTier enum"]
    Validator --> Workflow
```

The active code paths are importable schema code under [[DAG Models]] and structural validation under [[DAG Validator]]. There is no running API app, no database adapter, no queue, no worker, no provider router, and no frontend application code yet.

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

This diagram is architectural intent, not current runtime behavior. Today, only [[DAG Models]] and [[DAG Validator]] exist as real implementation.

## Module Responsibilities

- [[04_APIs|API Layer]]: package exists at `backend/src/ather_os/api`, but contains only a docstring.
- [[Response Cache]]: package exists at `backend/src/ather_os/cache`, but no interface or implementation exists.
- [[Checkpoint Engine]]: package exists at `backend/src/ather_os/checkpoint`, but no event replay logic exists.
- [[Configuration]]: package exists at `backend/src/ather_os/config`, but no settings model or environment loading exists.
- [[DAG Models]]: implemented in `backend/src/ather_os/dag/models.py`.
- [[DAG Validator]]: implemented in `backend/src/ather_os/dag/validators.py`.
- [[Provider Router]]: package exists at `backend/src/ather_os/providers`, but no router or mock provider exists.
- [[Queue Broker]]: package exists at `backend/src/ather_os/queue`, but no queue implementation exists.
- [[State Store]]: package exists at `backend/src/ather_os/state`, but no database implementation exists.
- [[Worker]]: package exists at `backend/src/ather_os/worker`, but no execution loop exists.

## Data Flow

Current data flow is limited to in-memory validation when a developer instantiates [[Workflow Model]] or [[Task Model]] through Pydantic, then calls [[DAG Validator]] to validate dependency structure. There is no persisted state or API request flow.

Planned data flow is documented as:

1. User submits a goal through [[04_APIs|APIs]] or future [[Frontend]].
2. Orchestrator creates or receives a [[Workflow Model]].
3. Each [[Task Model]] declares dependencies and context needs.
4. [[Queue Broker]] schedules executable tasks.
5. [[Worker]] executes tasks through [[Provider Router]].
6. [[State Store]] appends task events.
7. [[Checkpoint Engine]] replays events after restart.

## Dependencies

Current runtime dependencies from `backend/pyproject.toml`:

- FastAPI
- Pydantic
- Uvicorn

Current development dependency:

- Pytest

Only Pydantic and the Python standard library are used by the current source code. FastAPI and Uvicorn are installed for planned [[04_APIs|API]] work but are not imported by application code.

## Related

- [[00_Project_Overview|Project Overview]]
- [[02_Folder_Structure|Folder Structure]]
- [[03_Database|Database]]
- [[04_APIs|APIs]]
- [[06_State_Management|State Management]]
- [[10_Current_Status|Current Status]]
