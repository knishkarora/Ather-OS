# Project Overview

[[README|Knowledge Base Home]] > Project Overview

Ather OS is intended to become a resilient, cost-aware autonomous AI execution engine. The product vision is captured in `AtherOS_Project_Master_Document.md` and summarized in the root `README.md`: a system that decomposes high-level goals into workflow DAGs, executes tasks through providers, records append-only events, and resumes after failure.

The repository is currently in an early Phase 0 foundation state. The implemented backend code consists of the Python package skeleton, Pydantic [[DAG Models]] in `backend/src/ather_os/dag/models.py`, structural [[DAG Validator]] logic in `backend/src/ather_os/dag/validators.py`, sample workflow JSON files, a small workflow validation command, a local append-only [[State Store]], [[Checkpoint Engine]] replay, in-memory [[Queue Broker]] scheduling, and [[Queue Lifecycle Service]] event coordination.

## Current Scope

- [[Backend]] exists as a Python project under `backend/`.
- [[Frontend]] exists only as a placeholder folder with a README.
- [[DAG Models]] are implemented with Pydantic validation constraints.
- [[DAG Validator]] is implemented for duplicate task IDs, unknown dependencies, self-dependencies, cycles, and connected-root validation.
- Sample workflow JSON files exist under `backend/samples/`.
- A minimal workflow validation command exists at `backend/src/ather_os/dag/validate_workflow.py`.
- [[State Store]] has typed lifecycle events, a storage protocol, and a SQLite implementation.
- [[Checkpoint Engine]] has workflow/task status projection models and event replay.
- [[Queue Broker]] has a minimal scheduling protocol and dependency-aware in-memory implementation.
- [[Queue Lifecycle Service]] records local submission, queue, start, and successful completion events around queue operations.
- [[04_APIs|APIs]], [[Provider Router]], [[Worker]], and [[Response Cache]] have package folders or documented intent, but no executable implementation yet.
- [[07_Authentication|Authentication]] is not implemented and is not referenced by code.

## Product Intent

The intended system is an execution substrate rather than a prompt framework. The planned architecture includes:

- Workflow ingestion through [[04_APIs|APIs]].
- Strict [[DAG Models]] and graph validation through [[DAG Validator]].
- Event-sourced [[03_Database|Database]] state.
- [[Checkpoint Engine]] replay and crash recovery.
- [[Provider Router]] selection for cost-aware model routing.
- [[Worker]] execution loops.
- A future [[Frontend]] dashboard for workflow visibility.

## Implementation Boundary

The master document describes several features as Stage 0 built, including storage, event sourcing, checkpoint recovery, response caching, mock provider routing, a worker, and REST API endpoints. The audited repository now contains the local storage/event-sourcing foundation, in-memory checkpoint replay, and event-coordinated in-memory queue scheduling, but cache, provider routing, worker, and REST API endpoints are still roadmap/planned work unless source code exists.

See [[10_Current_Status|Current Status]], [[09_Roadmap|Roadmap]], and [[12_Bugs|Bugs]] for the precise gap between vision documents and actual code.

## Related

- [[01_Architecture|Architecture]]
- [[02_Folder_Structure|Folder Structure]]
- [[10_Current_Status|Current Status]]
- [[11_Tasks|Tasks]]
- [[13_Decisions|Decisions]]
