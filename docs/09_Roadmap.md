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
- Placeholder [[Frontend]] folder.
- Root project and journey documentation.

## Next Logical Work

1. Add [[Queue Broker]] for dependency-aware task scheduling.
2. Add mock [[Provider Router]] and mock provider.
3. Add in-process [[Worker]] execution loop.
4. Add basic [[04_APIs|APIs]] once the backend engine has testable behavior.

## Phase 0 Vision

The project documents describe Phase 0 as a local backend engine with:

- Validated workflow DAGs. Schema validation, structural validation, sample JSON files, and a local validation command are now implemented; execution is not.
- Event-sourced state. The local append-only [[State Store]] now exists.
- Checkpoint recovery. In-memory replay and status projections now exist; worker restart behavior does not.
- Response caching.
- Mock provider execution.
- In-process worker.
- Small API for running and inspecting workflows.

The schema, graph validation, local event storage, and checkpoint replay parts currently exist.

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
