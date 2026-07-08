# Decisions

[[README|Knowledge Base Home]] > Decisions

This file records architectural decisions that are visible in the repository today.

## Use Python Backend

The backend is a Python package named `ather-os-backend`.

Evidence: `backend/pyproject.toml` and `backend/src/ather_os`.

Related: [[Backend]], [[01_Architecture|Architecture]]

## Use Pydantic for Domain Schemas

[[DAG Models]] use Pydantic `BaseModel` and `Field` constraints.

Evidence: `backend/src/ather_os/dag/models.py`.

Related: [[05_Components|Components]], [[06_State_Management|State Management]]

## Use UUID Identifiers

[[Workflow Model]] and [[Task Model]] use UUID fields for workflow and task identity.

Evidence: `workflow_id: UUID`, `task_id: UUID`, and `dependencies: list[UUID]`.

Related: [[03_Database|Database]], [[DAG Models]]

## Limit Workflows to 20 Tasks

[[Workflow Model]] restricts `tasks` to minimum 1 and maximum 20.

Evidence: `tasks: list[Task] = Field(min_length=1, max_length=20)`.

Related: [[Task Model]], [[09_Roadmap|Roadmap]]

## Validate DAG Structure Outside Pydantic Models

Structural graph validation lives in `backend/src/ather_os/dag/validators.py` instead of inside [[Workflow Model]].

Reason: field validation and graph validation are different responsibilities. Keeping [[DAG Validator]] separate makes it easier for future [[04_APIs|APIs]], sample loaders, tests, and workers to explicitly validate workflow structure at ingestion time.

Related: [[DAG Models]], [[05_Components|Components]], [[06_State_Management|State Management]]

## Require One Connected Root Task

[[DAG Validator]] requires exactly one task with no dependencies and requires all tasks to be reachable from that root through dependency edges.

Reason: the project vision describes a root workflow DAG with no orphaned tasks. This rule gives future [[Queue Broker]] and [[Worker]] logic a clear executable graph.

Related: [[Task Model]], [[Workflow Model]], [[11_Tasks|Tasks]]

## Preserve Backend Package Boundaries Early

The backend contains empty packages for API, cache, checkpoint, config, providers, queue, state, and worker before implementation.

Evidence: package directories under `backend/src/ather_os`.

Related: [[02_Folder_Structure|Folder Structure]], [[01_Architecture|Architecture]]

## Keep Frontend Placeholder

The frontend folder exists before UI implementation.

Evidence: `frontend/README.md`.

Related: [[08_UI_System|UI System]], [[Frontend]]

## Open Decisions

- Which DAG validator module and API should be used?
- Which database library should implement local SQLite storage?
- Should FastAPI be introduced before or after the local engine works without HTTP?
- How should local mode handle authentication?
- Which frontend framework should be used?

## Related

- [[00_Project_Overview|Project Overview]]
- [[09_Roadmap|Roadmap]]
- [[11_Tasks|Tasks]]
- [[10_Current_Status|Current Status]]
