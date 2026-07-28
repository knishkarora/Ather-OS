# Frontend Delivery Plan

[[README|Knowledge Base Home]] > [[08_UI_System|UI System]] > Frontend Delivery Plan

The frontend will be built in small reviewable stages. Each stage ends with
user feedback before the next stage adds more behavior or visual commitment.

## Stage 1 — Workflow Workspace Foundation

**Status: implemented, awaiting feedback.**

Create a dependency-free static workflow workspace in `frontend/` using local
demo data. It establishes the application frame, navigation, workflow metrics,
connected task cards, status color language, a selected-task inspector, and a
compact activity feed.

The task cards are clickable so reviewers can assess the inspector interaction.
There is no API client, workflow submission, persistence, or production
workflow data in this stage.

**Feedback requested:** visual hierarchy, dark-shell/light-canvas balance,
card shape, spacing, state colors, density, and the information shown in the
task inspector.

## Stage 2 — Workflow Builder

Build the workflow submission and task-editing flow using local browser state.
This includes the goal, tasks, dependencies, retry/timeout settings, and
client-side structural feedback. It does not submit work to the backend yet.

**Feedback gate:** workflow creation should feel clear before API validation is
added.

## Stage 3 — Live Workflow Data

Add a minimal native API client for `POST /workflows` and
`GET /workflows/{workflow_id}`. Replace the Stage 1 demo data with backend
snapshots, including loading, empty, completed, and failed states.

**Feedback gate:** status language and live updates should be understandable
without reading event internals.

## Stage 4 — Trace and Recovery

Add the append-ordered event trace from `GET /workflows/{workflow_id}/events`
and the explicit recovery action from `POST /workflows/{workflow_id}/recover`.
The UI will clearly explain at-least-once recovery rather than hiding it.

**Feedback gate:** users should be able to diagnose a workflow from the UI.

## Stage 5 — Product Polish

Apply feedback across the completed views: responsive behavior, keyboard and
screen-reader access, empty/error states, motion restraint, and visual
consistency. Framework or component-library adoption is reconsidered only if
the finished design shows a real need.

## Technology Decision

Stages 1–2 use native HTML, CSS, and JavaScript. This follows the project’s
zero-dependency rule and keeps visual iteration quick. A framework is not ruled
out; it is deliberately deferred until the UI design and interaction scope make
its value clear.

## Related

- [[UI Direction]]
- [[04_APIs|APIs]]
- [[08_UI_System|UI System]]
- [[Frontend]]
