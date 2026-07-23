# Tasks

[[README|Knowledge Base Home]] > Tasks

This task list is based on the audited current implementation.

## Documentation Tasks

- Keep this knowledge base updated after every meaningful code change.
- Update [[14_Changelog|Changelog]] when features are added.
- Move stale roadmap claims into [[09_Roadmap|Roadmap]] if source code does not support them.

## Immediate Engineering Tasks

- Add response caching around provider execution.

## Backend Foundation Tasks

- Define [[Provider Router]] interface.
- Add asynchronous execution and workflow event inspection routes.
- Design automatic recovery only after task ownership, retry-budget, and timeout policies are explicit.

## Frontend Tasks

- Decide frontend framework.
- Add basic app structure.
- Add workflow submission view after API exists.
- Add workflow status view after state projections exist.
- Add execution trace view after event logs exist.

## Quality Tasks

- Continue expanding automated tests as backend modules are added.
- Add linting/formatting decision.
- Add CI after tests exist.
- Add explicit developer setup instructions.
- Decide whether local `.venv` should remain purely local and untracked.

## Related

- [[10_Current_Status|Current Status]]
- [[09_Roadmap|Roadmap]]
- [[12_Bugs|Bugs]]
- [[13_Decisions|Decisions]]
