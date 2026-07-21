# Ather OS Backend

The backend is the execution engine of Ather OS.

For Phase 0, this side of the project will contain the local-only engine:

- DAG validation
- sample workflow validation
- event-sourced state storage
- checkpoint recovery
- response caching
- mock provider routing
- in-process task worker
- FastAPI endpoints for submitting and inspecting workflows

The backend should be designed so local Phase 0 pieces can later be replaced
by remote Phase 1 pieces without rewriting the core engine.

## Validate a Sample Workflow

From `backend/`:

```powershell
.\.venv\Scripts\python.exe -m ather_os.dag.validate_workflow .\samples\valid_research_workflow.json
```

## Run the Local API

From `backend/`:

```powershell
.\.venv\Scripts\uvicorn.exe ather_os.api.app:app --reload
```

The local API uses `ather-os.sqlite3` for its append-only event log.

- `POST /workflows` validates and executes a workflow with the deterministic mock provider.
- `GET /workflows/{workflow_id}` returns the persisted replayed workflow snapshot.
- `POST /workflows/{workflow_id}/recover` rebuilds local queue state and resumes an unfinished workflow.
