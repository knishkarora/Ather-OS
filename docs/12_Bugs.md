# Bugs

[[README|Knowledge Base Home]] > Bugs

This file tracks known bugs, mismatches, and risks in the current repository.

## Documentation Mismatch

`AtherOS_Project_Master_Document.md` says Stage 0 is built and lists several implemented features. The actual codebase implements the DAG foundation, sample validation, local [[State Store]], checkpoint replay, explicit local recovery, a deterministic mock provider, a sequential in-process worker, and a small local API, but not the full engine.

Impact: future contributors or AI agents may assume cache, provider routing, asynchronous APIs, or full restart recovery code exists.

Related: [[10_Current_Status|Current Status]], [[09_Roadmap|Roadmap]]

## Limited Tests

`backend/pyproject.toml` configures pytest, and the DAG, state-store, checkpoint replay, queue, mock provider, local worker, explicit recovery, and synchronous API have focused tests. Cache, provider routing, retry, asynchronous API, and automatic/concurrent recovery coverage is still missing.

Impact: DAG schema, graph validation, state event persistence, replay behavior, and basic local execution are protected, but future service and recovery behavior is not covered yet.

Related: [[11_Tasks|Tasks]], [[05_Components|Components]]

## Installed Tools Not On PATH

Running `pytest` directly failed in the shell. Running `.\.venv\Scripts\pytest.exe` worked.

Impact: setup instructions should tell developers to activate the virtual environment or call local scripts explicitly.

Related: [[10_Current_Status|Current Status]]

## No Runtime Entry Point

The API's default SQLite path is a local working-directory file, and configuration has not been introduced yet.

Impact: local runs are useful for development but do not yet have environment-specific database configuration.

Related: [[04_APIs|APIs]], [[11_Tasks|Tasks]]

## Related

- [[10_Current_Status|Current Status]]
- [[11_Tasks|Tasks]]
- [[14_Changelog|Changelog]]
