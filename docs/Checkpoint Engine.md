# Checkpoint Engine

[[README|Knowledge Base Home]] > Checkpoint Engine

The checkpoint engine replays stored workflow lifecycle events into the current workflow/task state.

## Implemented Code

The checkpoint package now contains:

- `backend/src/ather_os/checkpoint/models.py`: projection models and status enums.
- `backend/src/ather_os/checkpoint/replay.py`: event replay function.

## Replay API

`replay_workflow(events: list[WorkflowEvent]) -> WorkflowSnapshot`

The function expects append-ordered events from [[State Store]]. It returns a `WorkflowSnapshot` containing:

- `workflow_id`
- `goal`
- workflow `status`
- task snapshots by task ID
- optional workflow `error`

## Status Models

Workflow statuses:

- `pending`
- `completed`
- `failed`

Task statuses:

- `pending`
- `queued`
- `running`
- `completed`
- `failed`

Each task snapshot stores the task ID, current status, latest attempt number, optional output, and optional error.

## Replay Rules

- Replay must start with `workflow_submitted`.
- Submitted task IDs become `pending` task snapshots.
- `task_queued` marks a task as `queued`.
- `task_started` marks a task as `running` and records the attempt number.
- `task_completed` marks a task as `completed` and records output.
- `task_failed` marks a task as `failed` and records error text.
- `workflow_completed` marks the workflow as `completed`.
- `workflow_failed` marks the workflow as `failed` and records error text.

Replay raises `CheckpointReplayError` for empty event lists, event logs that do not start with `workflow_submitted`, mixed workflow IDs, or task events for unknown task IDs.

## Recovery

`WorkflowRecovery` in `backend/src/ather_os/worker/recovery.py` uses the replayed
snapshot plus the persisted `workflow_submitted` definition to rebuild the
in-memory queue after a process restart. It preserves completed task outputs,
requeues tasks that were queued or running at interruption, and resumes them
with an incremented attempt number. If every task was already completed, it
appends the missing `workflow_completed` event; if a task had failed before the
terminal workflow event was written, it appends `workflow_failed` instead.

Recovery is deliberately at-least-once: a task that was `running` when the
process stopped can be executed again because no durable completion event
exists for that attempt.

## Current Limits

- Replay is pure in-memory logic; it does not query [[State Store]] by itself.
- Recovery is explicit through `POST /workflows/{workflow_id}/recover`; normal
  submission is queued for process-local background execution.
- Queue scheduling is restored only in the new local process; it is not a
  distributed lease or ownership mechanism.
- There is no timeout, retry budget enforcement, or automatic startup recovery.

## Related

- [[State Store]]
- [[06_State_Management|State Management]]
- [[03_Database|Database]]
- [[Queue Broker]]
- [[Worker]]
