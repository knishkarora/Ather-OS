# Tasks

[[README|Knowledge Base Home]] > Tasks

This task list is based on the audited current implementation.

## Documentation Tasks

- Keep this knowledge base updated after every meaningful code change.
- Update [[14_Changelog|Changelog]] when features are added.
- Move stale roadmap claims into [[09_Roadmap|Roadmap]] if source code does not support them.

## Immediate Engineering Tasks

- Add tests for [[DAG Models]].
- Add DAG structural validator for dependency IDs, cycles, self-dependencies, and reachability.
- Decide whether validator belongs in `backend/src/ather_os/dag/validators.py` or another local pattern.
- Add sample workflow JSON files under `backend/samples/`.
- Add a minimal command or script to validate a sample workflow.

## Backend Foundation Tasks

- Define [[State Store]] interface.
- Define event models for task lifecycle.
- Implement SQLite local event store.
- Implement [[Checkpoint Engine]] replay.
- Define [[Queue Broker]] interface.
- Implement in-memory local queue.
- Define [[Provider Router]] interface.
- Implement mock provider.
- Implement local [[Worker]] execution loop.
- Add FastAPI app under [[04_APIs|APIs]].

## Frontend Tasks

- Decide frontend framework.
- Add basic app structure.
- Add workflow submission view after API exists.
- Add workflow status view after state projections exist.
- Add execution trace view after event logs exist.

## Quality Tasks

- Add automated tests.
- Add linting/formatting decision.
- Add CI after tests exist.
- Add explicit developer setup instructions.
- Decide whether local `.venv` should remain purely local and untracked.

## Related

- [[10_Current_Status|Current Status]]
- [[09_Roadmap|Roadmap]]
- [[12_Bugs|Bugs]]
- [[13_Decisions|Decisions]]
