# Roadmap

[[README|Knowledge Base Home]] > Roadmap

This roadmap distinguishes actual repository state from product vision.

## Current Foundation

Implemented:

- Backend Python project setup.
- Backend package skeleton.
- Pydantic [[DAG Models]].
- Placeholder [[Frontend]] folder.
- Root project and journey documentation.

## Next Logical Work

1. Add DAG structural validation for cycles, unknown dependencies, self-dependencies, and reachability.
2. Add tests for [[Workflow Model]], [[Task Model]], [[TaskType]], [[QualityTier]], and future validators.
3. Define local [[State Store]] interface.
4. Implement event schema for workflow/task lifecycle.
5. Add SQLite local event storage.
6. Implement [[Checkpoint Engine]] replay.
7. Add [[Queue Broker]] for dependency-aware task scheduling.
8. Add mock [[Provider Router]] and mock provider.
9. Add in-process [[Worker]] execution loop.
10. Add basic [[04_APIs|APIs]] once the backend engine has testable behavior.

## Phase 0 Vision

The project documents describe Phase 0 as a local backend engine with:

- Validated workflow DAGs.
- Event-sourced state.
- Checkpoint recovery.
- Response caching.
- Mock provider execution.
- In-process worker.
- Small API for running and inspecting workflows.

Only the schema part of this currently exists.

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
