# State Store

[[README|Knowledge Base Home]] > State Store

The state store is the append-only persistence layer for workflow lifecycle events.

## Implemented Code

The state package now contains:

- `backend/src/ather_os/state/events.py`: typed Pydantic workflow event models.
- `backend/src/ather_os/state/store.py`: minimal `StateStore` protocol.
- `backend/src/ather_os/state/sqlite.py`: local SQLite implementation.

## Event Models

Implemented event types:

- `workflow_submitted`
- `task_queued`
- `task_started`
- `task_completed`
- `task_failed`
- `workflow_completed`
- `workflow_failed`

Every event has:

- `event_id: UUID`
- `workflow_id: UUID`
- `occurred_at: datetime`
- `event_type`

Task-level events also include `task_id`. Terminal failure/completion events carry the smallest useful detail: task output or error text.

## Store Contract

`StateStore` exposes:

- `append_event(event: WorkflowEvent) -> None`
- `list_events(workflow_id: UUID) -> list[WorkflowEvent]`

The contract intentionally does not expose mutation, deletion, projections, queue behavior, or checkpoint replay. Those belong to future [[Checkpoint Engine]], [[Queue Broker]], and [[Worker]] work.

## SQLite Storage

`SQLiteStateStore` uses Python's standard `sqlite3` module. No new dependency was added.

The table is `workflow_events`:

- `sequence INTEGER PRIMARY KEY AUTOINCREMENT`
- `event_id TEXT NOT NULL UNIQUE`
- `workflow_id TEXT NOT NULL`
- `task_id TEXT`
- `event_type TEXT NOT NULL`
- `occurred_at TEXT NOT NULL`
- `payload TEXT NOT NULL`

Events are returned in append order by `sequence`. The stored JSON payload is parsed back into the specific Pydantic event model.

## Current Limits

- No replay/projection layer yet.
- No workflow status query yet.
- No task status query yet.
- No event idempotency policy beyond the database uniqueness constraint.
- No API, worker, or queue integration yet.

## Related

- [[03_Database|Database]]
- [[06_State_Management|State Management]]
- [[Checkpoint Engine]]
- [[Queue Broker]]
- [[Worker]]
