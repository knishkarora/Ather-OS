# Execution Recovery Policy

[[README|Knowledge Base Home]] > Execution Recovery Policy

This policy defines the boundary that must exist before Ather OS adds retry
handling, task timeouts, automatic startup recovery, or more than one worker.
It describes the current local mode and the contract for the next implementation
slice; it does not claim those features are implemented.

## Current Local Contract

- One FastAPI process owns the background tasks it submits while that process is
  alive.
- Ownership is process-local and is not written to the event store. A second
  process must not point at the same SQLite event database and execute work.
- A provider exception retries immediately until its task's retry budget is
  exhausted, then the worker emits `task_failed` followed by `workflow_failed`.
- A process interruption after `task_started` is handled only by the explicit
  recovery route. The task is requeued and may execute again, so recovery is
  at-least-once.
- Provider calls have no timeout or cancellation boundary. A task may therefore
  remain `running` until the process exits or the provider returns.

## Retry Contract

`Task.max_retries` means the number of executions allowed *after* the initial
attempt. A task with `max_retries=2` may therefore start at most three times.

Retryable failure uses `task_attempt_failed`, which records the attempt number
and error while keeping the replayed task queueable. The local worker then
appends `task_queued` and retries immediately while another attempt is allowed.
It appends the existing terminal `task_failed` and `workflow_failed` events only
after the budget is exhausted. The current provider boundary has no
non-retryable error type, so every provider exception follows this budget.

There is no backoff policy. Local retries are immediate and sequential; delayed
retry belongs with a durable scheduler, not the in-memory broker.

## Timeout Contract for the Next Slice

Timeout enforcement requires a provider boundary that can actually stop or
isolate work. The current synchronous `TaskProvider.execute` interface cannot
reliably cancel a running call, so recording a timeout today could cause a late
provider result to be recorded after the task was retried.

Before timeouts are enabled, the provider contract must define cancellation or
execution isolation, and timeout lifecycle events must include an attempt
number. A timed-out attempt follows the same retry-budget rules as another
retryable failure.

## Automatic Recovery Prerequisites

Automatic startup recovery remains deferred until all of these are true:

1. The state store can enumerate unfinished workflows without scanning an
   application-owned SQLite table from outside its interface.
2. A persisted ownership or lease rule prevents two processes from recovering
   the same workflow concurrently.
3. The worker has retry and timeout semantics that distinguish a recoverable
   attempt from a terminal task failure.
4. Provider work has an idempotency strategy, because a persisted
   `task_started` event cannot prove whether the provider finished before a
   crash.

For the current single-process engine, explicit recovery is the truthful and
safe operation. It keeps duplicate execution visible to the caller rather than
silently creating it at startup.

## Implementation Order

1. Define provider cancellation/isolation and add timeout handling.
2. Add durable lease ownership and unfinished-workflow discovery.
3. Add automatic startup recovery only after those contracts are covered by
   concurrent-recovery tests.

## Related

- [[Checkpoint Engine]]
- [[Queue Lifecycle Service]]
- [[Queue Broker]]
- [[Worker]]
- [[State Store]]
- [[04_APIs|APIs]]
- [[13_Decisions|Decisions]]
- [[11_Tasks|Tasks]]
