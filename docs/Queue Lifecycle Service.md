# Queue Lifecycle Service

[[README|Knowledge Base Home]] > Queue Lifecycle Service

`WorkflowQueueService` is the small application-layer boundary between [[Queue Broker]] scheduling and append-only [[State Store]] lifecycle events.

## Implemented Code

`backend/src/ather_os/queue/lifecycle.py` contains `WorkflowQueueService`. It receives existing `QueueBroker` and `StateStore` implementations through its constructor; it does not add another storage or scheduling abstraction.

## Lifecycle Operations

- `submit_workflow(workflow)` queues the validated workflow, then records `workflow_submitted` and a `task_queued` event for each initially ready task.
- `claim_next_task(workflow_id, attempt=1)` claims the next ready task, then records `task_started`.
- `complete_task(workflow_id, task_id, output)` records a valid task output and emits `task_completed` plus `task_queued` events for newly unblocked tasks.
- `restore_workflow(workflow, completed_task_ids, queued_task_ids, interrupted_task_ids)` rebuilds volatile queue state from a replayed snapshot. Interrupted tasks receive a new `task_queued` event before execution resumes.

This creates one consistent event order for the local process while leaving dependency decisions inside [[Queue Broker]].

## Current Limits

- Queue memory and event storage are not transactional together. A process failure during an operation can leave them out of sync until future recovery work exists.
- The service does not execute tasks or choose retry policy; [[Worker]] owns execution and [[Checkpoint Engine]] recovery supplies restored state.
- Queue and event-store writes remain non-transactional. Recovery reconciles the supported interruption states, but it does not provide distributed guarantees.

## Related

- [[Queue Broker]]
- [[State Store]]
- [[Checkpoint Engine]]
- [[Worker]]
- [[11_Tasks|Tasks]]
