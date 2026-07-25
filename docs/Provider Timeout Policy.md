# Provider Timeout Policy

[[README|Knowledge Base Home]] > Provider Timeout Policy

This policy defines how Ather OS will add task deadlines without pretending
that a generic synchronous Python call can be forcibly cancelled. It is a
design contract; timeout fields, events, and enforcement are not implemented.

## Decision

The next timeout implementation will use **cooperative provider cancellation**.
Each provider receives a task deadline and must configure its own network or
SDK request timeout so it either returns an output before the deadline or raises
a dedicated timeout error. The worker will not use a thread to impose a timeout,
because Python cannot safely stop a running thread and a late provider result
could race with a retry.

Providers that cannot honor a deadline are not eligible for timed execution in
local mode. If such a provider is needed later, it must run in a separately
owned process that can be terminated; that isolation model is deliberately
deferred because it introduces process lifecycle, serialization, and output
handoff policy beyond the current sequential worker.

## Why This Is the Smallest Honest Design

- **Omission:** the deterministic `MockProvider` completes immediately, so no
  timeout mechanism is needed for the current local engine.
- **Reuse:** the `TaskProvider` protocol is the established execution boundary; timeout
  information belongs there rather than in the worker, queue, or API layer.
- **Native first:** real HTTP/SDK providers should use their request-level
  deadline support. No timeout library, thread manager, or task subprocess is
  needed for cooperative providers.
- **Isolation later:** a child process is the only generic force-stop option,
  but it is not free or necessary until a non-cooperative provider is added.

## Future Provider Contract

The future `TaskProvider` contract should receive an absolute deadline rather
than a worker-managed sleep duration. An absolute deadline prevents time spent
in routing, cache lookup, or retry setup from extending a task's allowed wall
clock time.

Conceptually:

```python
execute(task: Task, deadline: datetime | None) -> str
```

When the deadline cannot be met, the provider raises a dedicated
`ProviderTimeoutError`. It must not return a successful output after reporting
that timeout. Decorators and routers must pass the deadline through unchanged:

```mermaid
flowchart LR
    Worker --> Cache["CachedTaskProvider"]
    Cache --> Router["RoutedTaskProvider"]
    Router --> Provider["Concrete provider"]
    Provider --> Deadline["Provider request deadline"]
```

A cache hit returns immediately and does not create provider work, so it is not
a timeout candidate. A cache miss must forward the deadline to the selected
provider.

## Timeout Lifecycle Contract

The timeout configuration must be explicit on a task before enforcement is
added. The proposed local field is an optional positive `timeout_seconds`; no
configured value means no deadline. This avoids inventing a global default
before real provider latency is known.

When a provider raises `ProviderTimeoutError`, the worker should append a new
`task_attempt_timed_out` event containing:

- task ID
- attempt number
- configured timeout in seconds
- a concise error message

Checkpoint replay should treat that event like `task_attempt_failed`: the task
remains queueable while retry budget remains. After the final allowed attempt,
the existing terminal `task_failed` and `workflow_failed` events are recorded.
Timeouts and ordinary provider exceptions therefore share the current immediate,
sequential retry budget.

## Required Implementation Sequence

1. Add optional `timeout_seconds` validation to [[Task Model]].
2. Add the deadline argument and `ProviderTimeoutError` to `TaskProvider`,
   then forward it through cache and routing decorators.
3. Extend the mock provider with a controllable cooperative timeout for tests.
4. Add `task_attempt_timed_out` parsing and checkpoint replay.
5. Let [[Worker]] calculate the deadline and apply existing retry-budget logic.
6. Add focused tests for cache hits, timeout retries, exhausted budgets, and
   recovery from a persisted timeout event.

## Non-Goals

- No thread-based cancellation.
- No process-per-task execution or forced termination.
- No default timeout value.
- No automatic startup recovery or multi-worker leases.

## Related

- [[05_Components|Components]]
- [[Provider Router]]
- [[Response Cache]]
- [[Worker]]
- [[Execution Recovery Policy]]
- [[Checkpoint Engine]]
- [[11_Tasks|Tasks]]
