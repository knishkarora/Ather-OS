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

The backend introduced package boundaries for API, cache, checkpoint, config, providers, queue, state, and worker early. [[State Store]] now has implementation; the other boundaries are still placeholders.

Evidence: package directories under `backend/src/ather_os`.

Related: [[02_Folder_Structure|Folder Structure]], [[01_Architecture|Architecture]]

## Use Append-Only Events for Local State

[[State Store]] persists workflow and task lifecycle changes as events instead of mutable workflow/task rows.

Reason: Phase 0 needs crash recovery and replay later. An append-only event log gives [[Checkpoint Engine]] a simple source of truth without introducing projections before they are needed.

Related: [[03_Database|Database]], [[06_State_Management|State Management]], [[State Store]]

## Use Standard Library SQLite for Local Event Storage

`SQLiteStateStore` uses Python's built-in `sqlite3` module.

Reason: the project values minimal dependencies, and local SQLite is enough for the first durable event log. Heavier database libraries can wait until the schema or query surface actually needs them.

Related: [[03_Database|Database]], [[State Store]]

## Keep Checkpoint Replay Pure

[[Checkpoint Engine]] replays a list of already-loaded events instead of querying [[State Store]] directly.

Reason: keeping replay pure makes it easy to test and keeps storage concerns separate from projection concerns. Future APIs, workers, or recovery code can decide where events come from, then reuse the same replay function.

Related: [[Checkpoint Engine]], [[State Store]], [[06_State_Management|State Management]]

## Use Explicit At-Least-Once Local Recovery

`WorkflowRecovery` reconstructs a fresh in-memory queue from the persisted event
stream only when `POST /workflows/{workflow_id}/recover` is called. A task that
was running when the process stopped is requeued and receives the next attempt number.

Reason: a `task_started` event cannot prove the provider did not finish before
the interruption. Re-executing is the smallest honest Phase 0 guarantee;
leases, idempotency keys, and automatic startup recovery would add policy that
the single-process engine does not yet need.

Related: [[Checkpoint Engine]], [[Queue Lifecycle Service]], [[Worker]], [[04_APIs|APIs]]

## Use Process-Local Response Caching

`CachedTaskProvider` uses `InMemoryResponseCache` to cache only successful
provider outputs by task type, prompt, context needs, and quality tier.

Reason: this removes duplicate local provider calls without adding a database,
expiry policy, or invalidation system before those needs exist. Cache contents
are intentionally excluded from the event log and recovery contract.

Related: [[Response Cache]], [[Worker]], [[Provider Router]]

## Keep Frontend Placeholder

The frontend folder exists before UI implementation.

Evidence: `frontend/README.md`.

Related: [[08_UI_System|UI System]], [[Frontend]]

## Open Decisions

- Which DAG validator module and API should be used?
- Should FastAPI be introduced before or after the local engine works without HTTP?
- How should local mode handle authentication?
- Which frontend framework should be used?

## Related

- [[00_Project_Overview|Project Overview]]
- [[09_Roadmap|Roadmap]]
- [[11_Tasks|Tasks]]
- [[10_Current_Status|Current Status]]
