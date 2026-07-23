# Provider Router

[[README|Knowledge Base Home]] > Provider Router

Implemented in `backend/src/ather_os/providers/router.py`.

`ProviderRouter` defines one decision: `provider_for(task)` returns the
`TaskProvider` that should execute a task. `RoutedTaskProvider` adapts that
decision to the worker's existing `execute(task)` boundary.

Phase 0 currently uses `SingleProviderRouter`, which selects the one configured
local provider for every task. This keeps the current mock-provider behavior
unchanged while giving a future multi-provider policy one explicit replacement
point.

The response cache wraps the routed provider. Because the present router always
selects one provider, the existing task-only cache key remains valid. A future
router that can select different output-producing providers must include provider
identity in the cache key before sharing cache entries between them.

## Related

- [[05_Components|Components]]
- [[Response Cache]]
- [[Worker]]
- [[09_Roadmap|Roadmap]]
