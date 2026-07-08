# Bugs

[[README|Knowledge Base Home]] > Bugs

This file tracks known bugs, mismatches, and risks in the current repository.

## Documentation Mismatch

`AtherOS_Project_Master_Document.txt` says Stage 0 is built and lists several implemented features. The actual codebase only implements [[DAG Models]] and package placeholders.

Impact: future contributors or AI agents may assume non-existent APIs, storage, cache, worker, or recovery code exists.

Related: [[10_Current_Status|Current Status]], [[09_Roadmap|Roadmap]]

## No Tests

`backend/pyproject.toml` configures pytest and `backend/tests/__init__.py` exists, but there are no actual tests. Running the local pytest executable collects 0 tests and exits with code 1.

Impact: schema behavior and future changes are not protected.

Related: [[11_Tasks|Tasks]], [[05_Components|Components]]

## DAG Structure Not Validated

[[Task Model]] accepts dependency UUIDs, but [[Workflow Model]] does not validate that dependencies reference existing tasks, avoid cycles, avoid self-dependencies, or form a reachable graph.

Impact: invalid workflow graphs can pass Pydantic validation.

Related: [[DAG Models]], [[06_State_Management|State Management]]

## Installed Tools Not On PATH

Running `pytest` directly failed in the shell. Running `.\.venv\Scripts\pytest.exe` worked.

Impact: setup instructions should tell developers to activate the virtual environment or call local scripts explicitly.

Related: [[10_Current_Status|Current Status]]

## No Runtime Entry Point

FastAPI and Uvicorn are dependencies, but there is no app module or command to start a server.

Impact: the backend cannot currently run as an API service.

Related: [[04_APIs|APIs]], [[11_Tasks|Tasks]]

## Related

- [[10_Current_Status|Current Status]]
- [[11_Tasks|Tasks]]
- [[14_Changelog|Changelog]]
