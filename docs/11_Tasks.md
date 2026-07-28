# Tasks

[[README|Knowledge Base Home]] > Tasks

This task list is based on the audited current implementation.

## Documentation Tasks

- Keep this knowledge base updated after every meaningful code change.
- Update [[14_Changelog|Changelog]] when features are added.
- Move stale roadmap claims into [[09_Roadmap|Roadmap]] if source code does not support them.

## Backend Foundation Tasks

- Add provider idempotency keys before allowing automatic recovery with a
  caller-supplied provider.
- Define multi-provider routing policy and provider-aware cache keys only when a second provider is introduced.

## Frontend Tasks

- Gather feedback on Stage 1 of [[Frontend Delivery Plan]].
- Build the local-state workflow builder in Stage 2.
- Add workflow submission and status data in Stage 3.
- Add execution trace and explicit recovery in Stage 4.

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
