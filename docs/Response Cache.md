# Response Cache

[[README|Knowledge Base Home]] > Response Cache

Implemented in `backend/src/ather_os/cache/store.py` and
`backend/src/ather_os/providers/cached.py`.

`InMemoryResponseCache` stores successful provider outputs for the lifetime of
one FastAPI application instance. `CachedTaskProvider` wraps the configured
`TaskProvider` before the [[Worker]] or [[Checkpoint Engine]] recovery path uses
it.

The cache key is a SHA-256 hash of a task's type, prompt, context needs, and
quality tier. It intentionally excludes workflow and task IDs, allowing
equivalent work in separate workflows to reuse a response. Provider exceptions
are propagated and never cached.

This is a local optimization, not workflow state: contents are not written to
SQLite, included in lifecycle events, or restored by [[Checkpoint Engine]].

## Related

- [[Provider Router]]
- [[Worker]]
- [[State Store]]
- [[05_Components|Components]]
