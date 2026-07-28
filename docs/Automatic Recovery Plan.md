# Automatic Recovery Plan

[[README|Knowledge Base Home]] > Automatic Recovery Plan

This plan is implemented for the deterministic mock-provider local mode.

## Goal

Safely resume unfinished local workflows when the API process starts, without
allowing two local processes to execute the same workflow at once.

## Proposed Minimal Contract

- Keep execution single-process and local; do not introduce a distributed
  worker, scheduler, or new dependency.
- Extend [[State Store]] with unfinished-workflow discovery based on the
  append-only event log.
- Add a small SQLite lease table keyed by workflow ID with an owner ID and an
  expiry time. Acquiring an expired or unowned lease must be atomic.
- On application startup, discover pending workflows, acquire their leases,
  and pass only successfully claimed workflows to [[Worker|Workflow Recovery]].
- Continue to treat an interrupted `task_started` as at-least-once work. The
  existing recovery path already requeues it with the next attempt number.
- Keep automatic recovery disabled for caller-supplied providers until the
  provider contract includes a caller-supplied idempotency key.

## Slice Boundaries

Included:

- State-store discovery and lease APIs with SQLite implementation.
- Startup recovery wiring in the FastAPI application.
- Lease contention, expiry, terminal-workflow exclusion, and restart recovery
  tests using the deterministic mock provider.
- Documentation for the local ownership guarantee and its limits.

Deferred:

- Multiple active workers, remote leases, retry backoff, and a real provider
  registry.
- Exactly-once execution. Local recovery remains at-least-once.
- Automatic execution of providers that cannot provide idempotency.

## Acceptance Criteria

1. A fresh app instance discovers only workflows whose replayed status is
   pending.
2. Two app instances using one SQLite database cannot both recover the same
   workflow while its lease is valid.
3. A lease becomes recoverable after expiry, and terminal workflows are never
   resubmitted.
4. Recovery preserves completed task outputs and re-executes interrupted work
   according to the existing retry and timeout rules.
5. The full backend test suite passes without new dependencies.

## Implemented Safety Boundary

The default deterministic mock provider is treated as side-effect-free, so it
automatically recovers unfinished workflows at FastAPI startup. A
caller-supplied provider continues to require the explicit recovery route until
the provider contract gains idempotency keys.

## Related

- [[Execution Recovery Policy]]
- [[State Store]]
- [[Checkpoint Engine]]
- [[Worker]]
- [[04_APIs|APIs]]
- [[09_Roadmap|Roadmap]]
