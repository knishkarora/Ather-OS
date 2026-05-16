# Ather OS Backend

The backend is the execution engine of Ather OS.

For Phase 0, this side of the project will contain the local-only engine:

- DAG validation
- event-sourced state storage
- checkpoint recovery
- response caching
- mock provider routing
- in-process task worker
- FastAPI endpoints for submitting and inspecting workflows

The backend should be designed so local Phase 0 pieces can later be replaced
by remote Phase 1 pieces without rewriting the core engine.

