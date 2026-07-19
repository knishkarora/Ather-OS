# Queue Lifecycle Service

[[README|Knowledge Base Home]] > Queue Lifecycle Service

`WorkflowQueueService` is the small application-layer boundary between [[Queue Broker]] scheduling and append-only [[State Store]] lifecycle events.

## Implemented Code

`backend/src/ather_os/queue/lifecycle.py` contains `WorkflowQueueService`. It receives existing `QueueBroker` and `StateStore` implementations through its constructor; it does not add another storage or scheduling abstraction.

## Lifecycle Operations

- `submit_workflow(workflow)` queues the validated workflow, then records `workflow_submitted` and a `task_queued` event for each initially ready task.
- `claim_next_task(workflow_id, attempt=1)` claims the next ready task, then records `task_started`.
- `complete_task(workflow_id, task_id, output)` records a valid task output and emits `task_completed` plus `task_queued` events for newly unblocked tasks.

This creates one consistent event order for the local process while leaving dependency decisions inside [[Queue Broker]].

## Current Limits

- Queue memory and event storage are not transactional together. A process failure during an operation can leave them out of sync until future recovery work exists.
- The service does not execute tasks, retry them, handle failures, emit terminal workflow events, or reconstruct queue state from stored events.
- A [[Worker]] will call the claim and completion operations when local execution begins.

## Related

- [[Queue Broker]]
- [[State Store]]
- [[Checkpoint Engine]]
- [[Worker]]
- [[11_Tasks|Tasks]]
