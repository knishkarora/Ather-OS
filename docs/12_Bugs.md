# Bugs

[[README|Knowledge Base Home]] > Bugs

This file tracks known bugs, mismatches, and risks in the current repository.

## Documentation Mismatch

`AtherOS_Project_Master_Document.md` says Stage 0 is built and lists several implemented features. The actual codebase implements the DAG foundation, sample validation, local [[State Store]] foundation, and [[Checkpoint Engine]] replay foundation, but not the full engine.

Impact: future contributors or AI agents may assume non-existent APIs, cache, worker, provider routing, or full restart recovery code exists.

Related: [[10_Current_Status|Current Status]], [[09_Roadmap|Roadmap]]

## Limited Tests

`backend/pyproject.toml` configures pytest, and the DAG, state-store, and checkpoint replay foundations now have focused tests. Future engine tests are still missing because queue, worker, cache, provider router, and API are not implemented yet.

Impact: DAG schema, graph validation, state event persistence, and replay behavior are protected, but future execution behavior is not covered yet.

Related: [[11_Tasks|Tasks]], [[05_Components|Components]]

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
