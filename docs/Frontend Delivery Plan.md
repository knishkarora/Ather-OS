# Frontend Delivery Plan

[[README|Knowledge Base Home]] > [[08_UI_System|UI System]] > Frontend Delivery Plan

The frontend will be built in small reviewable stages. Each stage ends with
user feedback before the next stage adds more behavior or visual commitment.

## Stage 1 — Workflow Workspace Foundation

**Status: implemented and refined.**

Create a dependency-free static workflow workspace in `frontend/` using local
demo data. It establishes the application frame, navigation, workflow metrics,
connected task cards, status color language, a selected-task inspector, and a
compact activity feed.

The task cards are clickable so reviewers can assess the inspector interaction.
There is no API client, workflow submission, persistence, or production
workflow data in this stage.

**Feedback requested:** visual hierarchy, dark top-navigation/light-canvas
balance, card shape, spacing, state colors, density, and the information shown
in the task inspector.

## Stage 2 — Workflow Builder

**Status: implemented, refined after navigation feedback.**

Build the workflow submission and task-editing flow using local browser state.
This includes the goal, tasks, dependencies, retry/timeout settings, and
client-side structural feedback. It does not submit work to the backend yet.

The prototype now opens with a workspace summary and uses a full-width dark
product navigation for Workspace, Builder, and Activity. The summary is not a
separate fake dashboard: it mirrors the active draft and points to the next
real action.

**Feedback gate:** workflow creation should feel clear before API validation is
added.

## Stage 3 — Live Workflow Data

**Status: implemented.**

Add a minimal native API client for `POST /workflows` and
`GET /workflows/{workflow_id}`. Replace the Stage 1 demo data with backend
snapshots, including loading, empty, completed, and failed states.

**Execution-view design:** the live surface uses one dark workflow-status
header, a visible completion bar, state-labelled task cards, and a compact
append-ordered event trace. This keeps the workflow's current state scannable
without presenting the trace as the primary interface.

**Feedback gate:** status language and live updates should be understandable
without reading event internals.

## Stage 4 — Trace and Recovery

Add the append-ordered event trace from `GET /workflows/{workflow_id}/events`
and the explicit recovery action from `POST /workflows/{workflow_id}/recover`.
The UI will clearly explain at-least-once recovery rather than hiding it.

**Status: implemented.** The React workspace polls the live snapshot and
append-ordered trace while a run is active. An unfinished workflow exposes a
recovery action with explicit at-least-once wording before it calls the local
recovery endpoint.

**Feedback gate:** users should be able to diagnose a workflow from the UI.

## Stage 5 — Product Polish

**Status: implemented and verified.**

Applied polish across all workflow workspace views:
- Added client-side DAG validator (`dagValidation.js`) enforcing Kahn's algorithm cycle detection, self-dependency prevention, unknown dependency check, and single-root task constraint before API submission.
- Fixed `TaskEditor` select option value bug for `task_type` (`code_generation`) preventing 422 API errors.
- Enhanced contrast for alert banners and error states.
- Implemented responsive mobile drawer navigation and active section tracking (`#workspace`, `#builder`, `#run-status`).
- Added token estimation input field and validated retries/timeouts.

## Technology Decision

The frontend uses React, Vite, and Tailwind CSS. The initial native prototype
proved the interaction model, but workflow editing, polling, trace rendering,
and recovery now share enough client state that React avoids repeated manual
DOM synchronization. The implementation stays deliberately small: there is no
router, component library, or client-state package.

## Related

- [[UI Direction]]
- [[04_APIs|APIs]]
- [[08_UI_System|UI System]]
- [[Frontend]]
