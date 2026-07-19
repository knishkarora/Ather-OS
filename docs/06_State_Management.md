# State Management

[[README|Knowledge Base Home]] > State Management

State management is partially implemented.

## Current State

The backend now has an append-only local [[State Store]] foundation:

- Typed lifecycle event models in `backend/src/ather_os/state/events.py`.
- A minimal `StateStore` protocol in `backend/src/ather_os/state/store.py`.
- A SQLite-backed implementation in `backend/src/ather_os/state/sqlite.py`.
- [[Checkpoint Engine]] projection models and event replay in `backend/src/ather_os/checkpoint`.
- [[Queue Lifecycle Service]] coordination between local queue transitions and lifecycle events.

There is still no frontend state management, worker loop, queue recovery, or API state endpoint.

[[Workflow Model]] and [[Task Model]] instances are still validated in memory before state is persisted. Pydantic validates field shape, and [[DAG Validator]] validates dependency structure before future stateful execution systems rely on it.

## Backend State Boundaries

The repository contains package placeholders for planned state-related systems:

- [[State Store]] at `backend/src/ather_os/state`
- [[Checkpoint Engine]] at `backend/src/ather_os/checkpoint`
- [[Queue Broker]] at `backend/src/ather_os/queue`
- [[Response Cache]] at `backend/src/ather_os/cache`

[[State Store]], [[Checkpoint Engine]], and [[Queue Broker]] have real implementation. The cache package currently contains only an `__init__.py` docstring.

## Intended Event-Sourced Flow

The project vision describes append-only task events and replay:

```mermaid
flowchart LR
    Worker["Future Worker"] --> Lifecycle["Queue Lifecycle Service"]
    Lifecycle --> Queue["Queue Broker"]
    Lifecycle --> StateStore["State Store"]
    StateStore --> Replay["Checkpoint Replay"]
    Replay --> WorkflowState["Reconstructed Workflow State"]
```

The append-event and list-events portions are implemented in [[State Store]]. In-memory replay is implemented in [[Checkpoint Engine]]. [[Queue Lifecycle Service]] now emits submission, queue, start, and successful completion events while delegating readiness decisions to [[Queue Broker]].

## Frontend State

Not applicable. The [[Frontend]] has no application code or state library.

## Relationships

- [[Task Model]] currently stores `dependencies`, `context_needs`, retry budget, quality tier, and estimated token count.
- [[Workflow Model]] groups tasks under a workflow ID and goal.
- [[DAG Validator]] verifies that workflow dependencies are executable before future state transitions are recorded.
- [[State Store]] persists workflow and task lifecycle events.
- [[Checkpoint Engine]] reconstructs current workflow/task status from persisted events.
- [[Queue Broker]] determines which [[Task Model]] instances are executable based on completed dependencies.
- [[Queue Lifecycle Service]] coordinates the local queue with append-only events, without claiming durable queue recovery yet.

## Missing State Work

- Add workflow status query.
- Add task status query.
- Add tests for future recovery behavior.

## Related

- [[03_Database|Database]]
- [[05_Components|Components]]
- [[01_Architecture|Architecture]]
- [[11_Tasks|Tasks]]
