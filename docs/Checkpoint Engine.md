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

## Current Limits

- Replay is pure in-memory logic; it does not query [[State Store]] by itself.
- There is no API endpoint for workflow or task status yet.
- Queue scheduling exists in [[Queue Broker]], but replay is not integrated with it yet.
- There is no worker recovery loop yet.

## Related

- [[State Store]]
- [[06_State_Management|State Management]]
- [[03_Database|Database]]
- [[Queue Broker]]
- [[Worker]]
