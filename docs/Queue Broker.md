# Queue Broker

[[README|Knowledge Base Home]] > Queue Broker

The queue broker decides which workflow tasks are ready to execute based on completed dependencies.

## Implemented Code

The queue package now contains:

- `backend/src/ather_os/queue/broker.py`: minimal `QueueBroker` protocol.
- `backend/src/ather_os/queue/memory.py`: dependency-aware `InMemoryQueueBroker`.

## Queue Contract

`QueueBroker` exposes:

- `submit_workflow(workflow: Workflow) -> list[Task]`
- `mark_task_completed(workflow_id: UUID, task_id: UUID) -> list[Task]`
- `claim_next_task(workflow_id: UUID) -> Task | None`

The contract stays intentionally small. It does not persist state, execute tasks, retry failures, or mark workflows complete.

## Lifecycle Integration

[[Queue Lifecycle Service]] composes a `QueueBroker` with a [[State Store]]. It appends `workflow_submitted`, `task_queued`, `task_started`, and `task_completed` events around local queue operations. The broker remains focused only on dependency-aware scheduling.

## In-Memory Scheduling

`InMemoryQueueBroker` validates submitted workflows with [[DAG Validator]], stores tasks in process memory, and queues only tasks whose dependencies are complete.

Scheduling rules:

- Submitting a workflow queues the root task immediately.
- Completing a task queues any dependents whose full dependency list is now complete.
- Claimed and completed tasks are not requeued.
- Submitting the same workflow twice raises `QueueBrokerError`.
- Completing an unknown workflow or unknown task raises `QueueBrokerError`.

## Current Limits

- Queue state is in-memory only and disappears when the process exits.
- There is no [[Worker]] loop to claim and execute tasks yet.
- There is no retry, lease, timeout, priority, or concurrency policy yet.

## Related

- [[DAG Validator]]
- [[State Store]]
- [[Queue Lifecycle Service]]
- [[Checkpoint Engine]]
- [[Worker]]
- [[11_Tasks|Tasks]]
