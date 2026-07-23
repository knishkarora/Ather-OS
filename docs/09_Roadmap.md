# Roadmap

[[README|Knowledge Base Home]] > Roadmap

This roadmap distinguishes actual repository state from product vision.

## Current Foundation

Implemented:

- Backend Python project setup.
- Backend package skeleton.
- Pydantic [[DAG Models]].
- Structural [[DAG Validator]] with pytest coverage.
- Sample workflow JSON files.
- Minimal workflow validation command with pytest coverage.
- Typed workflow/task lifecycle events.
- Minimal [[State Store]] protocol.
- SQLite append-only event store with pytest coverage.
- [[Checkpoint Engine]] replay and workflow/task status projections with pytest coverage.
- Dependency-aware [[Queue Broker]] scheduling with [[Queue Lifecycle Service]] event coordination.
- Replay-backed workflow/task status queries.
- Deterministic mock provider and in-process [[Worker]] execution with terminal failure recording.
- Process-local [[Response Cache]] around provider execution.
- Placeholder [[Frontend]] folder.
- Root project and journey documentation.

## Next Logical Work

1. Define a provider router once more than the deterministic mock provider is needed.
2. Add asynchronous execution and event inspection routes.
3. Define automatic recovery, task ownership, and retry/timeout policy before running recovery at startup or across multiple workers.

## Phase 0 Vision

The project documents describe Phase 0 as a local backend engine with:

- Validated workflow DAGs. Schema validation, structural validation, sample JSON files, and a local validation command are now implemented; execution is not.
- Event-sourced state. The local append-only [[State Store]] now exists.
- Checkpoint recovery. In-memory replay, status projections, and explicit local worker recovery now exist; automatic startup recovery does not.
- Process-local response caching is implemented; durable or shared caching is deferred.
- Mock provider execution. A deterministic implementation now exists.
- In-process worker. A sequential local implementation now exists; restart recovery does not.
- Small API for running and inspecting workflows.

The schema, graph validation, local event storage, checkpoint replay, explicit recovery, local provider, and worker execution parts currently exist.

## Later Vision

The master document describes future work:

- Real LLM orchestrator.
- Config-driven provider registry.
- Deterministic cost-aware routing.
- Redis rate limiting.
- Remote mode with PostgreSQL and Redis.
- Celery workers.
- Audit dashboard.
- Selective context manager.
- Adaptive routing and cost intelligence.
- Multi-agent collaboration.

These are roadmap items, not implemented features.

## Relationship to Current Status

See [[10_Current_Status|Current Status]] for a code-grounded snapshot and [[12_Bugs|Bugs]] for documentation/code mismatches that could confuse future work.

## Related

- [[00_Project_Overview|Project Overview]]
- [[01_Architecture|Architecture]]
- [[11_Tasks|Tasks]]
- [[13_Decisions|Decisions]]
