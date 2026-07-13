# Ather OS Journey

This file records the learning journey behind Ather OS.

It is not meant to track every tiny edit. Instead, it will be updated at useful
checkpoints: when a meaningful project structure, module, feature, or design
decision is completed.

## Why This File Exists

Ather OS is being built as a learning project, not as a rushed hackathon build.
That means the reasoning matters as much as the final code.

This journey file will help capture:

- what was built at each checkpoint
- why that step came next
- which design choices were made
- what challenges or confusions came up
- how each piece connects to the larger architecture

## Current Direction

The long-term vision is an autonomous AI execution engine that can break a goal
into tasks, execute those tasks reliably, recover from failure, control cost,
and provide a clear audit trail.

The first focus is Phase 0: a local backend engine with no real LLM calls and no
remote infrastructure. Phase 0 will prove the foundation first:

- a validated workflow DAG
- event-sourced task state
- checkpoint recovery
- response caching
- mock provider execution
- an in-process worker
- a small API for running and inspecting workflows

## Day 1: Sunday, 17 May

We started by giving Ather OS its first real project shape.

What we completed:

- added `backend/` for the execution engine
- added `frontend/` for the future user interface
- added the root `README.md`
- created `JOURNEY.md` to record meaningful learning checkpoints
- created the backend Python project setup with `pyproject.toml`
- added the backend package skeleton under `backend/src/ather_os/`
- created the first real logic file: `backend/src/ather_os/dag/models.py`
- created a backend virtual environment
- installed FastAPI, Pydantic, Uvicorn, and Pytest
- confirmed that the DAG models can be imported successfully

The main lesson from today: before writing complex logic, a serious project
needs shape. The folder structure, package setup, and first models are not
flashy, but they create the ground where the real engine can grow.

Session ended at 3:44 a.m.

## Milestone: Wednesday, 8 July 2026

We added the first real structural safety check for Ather OS workflows: a DAG
validator.

What we completed:

- added `backend/src/ather_os/dag/validators.py`
- added `DagValidationError`
- added `validate_workflow_graph(workflow)`
- rejected duplicate task IDs
- rejected unknown dependency IDs
- rejected self-dependencies
- rejected dependency cycles
- required exactly one root task
- rejected disconnected workflow roots
- exported the validator from `ather_os.dag`
- added focused pytest coverage in `backend/tests/test_dag_validators.py`
- confirmed the backend test suite passes with 7 tests
- updated `/docs` so the knowledge base reflects the new implementation

Why this mattered:

The Pydantic models already checked whether a workflow had the right field
shapes, but they could not prove that the graph was executable. This validator
is the first step toward a trustworthy execution engine because future API,
queue, worker, checkpoint, and state-store code can reject invalid workflows
before trying to run them.

The main design decision:

We kept graph validation outside the Pydantic models. That keeps the model layer
simple and makes workflow ingestion explicit: parse the shape first, then
validate the graph structure.

What I learned from this:

Schema validation and system validation are related, but not the same. A JSON
object can have all the right fields and still describe impossible work. The
engine needs both layers.

What I would do differently next time:

Add the validator immediately after the models, before writing any worker or API
code. It is much easier to build execution logic when the graph rules are
already clear.

## Milestone: Monday, 13 July 2026

We added the first durable state foundation for Ather OS: a local append-only
workflow event store.

What we completed:

- added typed lifecycle events in `backend/src/ather_os/state/events.py`
- added a minimal `StateStore` protocol in `backend/src/ather_os/state/store.py`
- added `SQLiteStateStore` in `backend/src/ather_os/state/sqlite.py`
- used Python's built-in `sqlite3` module instead of adding a dependency
- stored full event JSON payloads while also indexing workflow IDs
- added tests for event validation, JSON parsing, append ordering, workflow
  filtering, persistence across store instances, and duplicate event IDs
- confirmed the backend test suite passes with 34 tests
- updated the `/docs` knowledge base so state and database docs now reflect
  actual implementation instead of planned intent

Why this mattered:

The project now has somewhere real to put workflow history. The engine still
does not execute tasks, but future checkpoint replay, queue scheduling, worker
execution, and API status endpoints can now depend on a small durable event log
instead of inventing state storage later.

The main design decision:

We kept the state store deliberately small: append one event and list events for
one workflow. No projections, no deletion, no ORM, no migration layer, and no
status query yet. That keeps the learning surface clear and leaves the next
module, checkpoint replay, with an obvious job.

What I learned from this:

Event sourcing becomes easier to reason about when the first implementation is
plain. A single table with a sequence number, event type, workflow ID, optional
task ID, and JSON payload is enough to prove the storage pattern before building
the more interesting replay logic.

What I would do differently next time:

Start with the event names even earlier. They force useful questions about the
workflow lifecycle: when a task is queued, when an attempt starts, what counts as
completion, and what failure detail needs to be kept for recovery.

Supporting evidence:

- `docs/journey-assets/2026-07-13-state-store-tests.md`

## Future Journey Updates

This file should stay readable. We will not update it after every tiny edit.
Instead, we will update it after meaningful checkpoints, such as:

- a complete module is added
- a feature starts working end to end
- a design decision changes the direction of the project
- a useful test, API call, terminal output, or frontend screen proves progress

Future screenshots and visual proof should go inside:

`docs/journey-assets/`

When we add screenshots later, they can be embedded directly in this file near
the checkpoint they belong to.

---

<p align="center">
  <strong>Journey continues above this line.</strong>
</p>

<p align="center">
  <em>Build slowly. Think clearly. Keep returning to the work.</em>
</p>

<p align="center">
  <sub>End of Ather OS Journey Log</sub>
</p>
