# Changelog

[[README|Knowledge Base Home]] > Changelog

This changelog records repository state changes that are visible from the audited files.

## 2026-08-17

- Fixed Groq fallback model configuration in `backend/.env` from non-existent `openai/gpt-oss-120b` to valid Groq model `llama-3.3-70b-versatile`, resolving `HTTP 403 Forbidden` error on fallback calls.
- Increased NVIDIA NIM read operation socket timeout from 45s to 60s in `backend/src/ather_os/providers/llm.py` and added `User-Agent: AtherOS/1.0` headers with detailed HTTP error body extraction.
- Added **Workflow Deliverables & Results Inspector View** in `App.jsx` showing full generated model responses for all workflow phases with code formatting (`pre`/`code`) and single-click copy buttons.
- Updated task status card color palette:
  - **Executing**: Warm Pulsing Amber/Yellow (`border-amber-300 bg-amber-100`)
  - **Completed**: Mint/Emerald Green (`border-emerald-300 bg-emerald-50`)
  - **Queued / Waiting**: Soft Lavender/Bluish-Purple (`border-indigo-200 bg-indigo-50` / `border-purple-200 bg-purple-50`)
  - **Failed**: Coral Red (`border-red-300 bg-red-50`)
- Populated `backend/.env` securely with NVIDIA NIM (`nvapi-...`) and Groq (`gsk_...`) API keys without hardcoding secrets in Python source code.
- Configured task-specific model routing:
  - `research`, `analysis`, `writing`, `validation` -> NVIDIA NIM (`meta/llama-3.3-70b-instruct`).
  - `code_generation` -> NVIDIA NIM (`meta/llama-3.2-3b-instruct`).
  - Fallback -> Groq API (`openai/gpt-oss-120b`).
- Ensured `.env` is listed in `.gitignore` to prevent secret exposure on GitHub.
- Added `LLMProvider` in `backend/src/ather_os/providers/llm.py` with multi-provider routing and Groq fallback.
- Completed Stage 5 frontend polish and bug fixes in React workflow workspace.
- Added client-side DAG validator (`dagValidation.js`) enforcing cycle detection via Kahn's algorithm, self-dependency checks, unknown dependency validation, and single root task constraints.
- Fixed `TaskEditor` select option value bug for `task_type` (`code_generation`) to prevent `422 Unprocessable Content` API errors.
- Added explicit `estimated_tokens` input field and sanitized retry/timeout inputs.
- Enhanced contrast for alert banners, error notices, and active navigation links.
- Added responsive mobile drawer navigation and active section tracking (`#workspace`, `#builder`, `#run-status`).

## 2026-08-12

- Migrated the frontend from manual DOM manipulation to a minimal React and
  Vite workspace, retaining Tailwind CSS and avoiding a router, UI library, or
  external client-state package.
- Completed the Stage 4 recovery slice with a visible recovery action for
  unfinished workflows, append-ordered trace rendering, and explicit
  at-least-once execution wording.
- Added the Vite development-server origins to the local API CORS allowlist.
- Completed the Stage 3 frontend polling loop: submitted workflows now refresh
  their replayed status and append-ordered lifecycle trace until reaching a
  terminal state.
- Updated workspace copy and frontend setup documentation to describe the
  live local API integration accurately.

## 2026-08-03

- Reworked the Stage 2 frontend navigation into a full-width dark product bar.
- Added a live workspace summary for the local workflow draft and made the
  execution activity surface discoverable before the first run.

## 2026-07-28

- Added SQLite unfinished-workflow discovery and atomic workflow leases.
- Added FastAPI startup recovery for unfinished workflows when the default
  deterministic mock provider is configured; caller-supplied providers remain
  explicit-recovery only.
- Added lease contention/expiry and startup recovery coverage; the backend
  suite now has 93 passing tests.
- Updated [[Automatic Recovery Plan]] and related architecture documentation.
- Added [[UI Direction]] and preserved the user-provided frontend inspiration
  assets for the staged frontend implementation.
- Added the dependency-free Stage 1 [[Frontend]] workflow workspace and
  [[Frontend Delivery Plan]] for feedback-driven UI delivery.
- Refined Stage 1 after feedback: product navigation now sits at the page top,
  with stronger typography, contrast, and task-state surfaces.
- Migrated the frontend styling to Tailwind CSS and added the Stage 2 local
  workflow builder with task editing, dependency controls, and structural
  review feedback.

## 2026-07-26

- Added [[Provider Timeout Policy]], selecting cooperative provider deadlines
  over unsafe thread cancellation and deferring process isolation until a
  non-cooperative provider is introduced.
- Added [[Execution Recovery Policy]] to define process-local ownership,
  retry-budget meaning, timeout prerequisites, and the gates for automatic
  startup recovery.
- Added `task_attempt_failed`, replay support, local queue requeueing, and
  sequential worker retry-budget enforcement using the existing
  `Task.max_retries` field.
- Added retry and recovery coverage; the backend suite now has 81 passing
  tests.
- Updated the roadmap and task list so provider cancellation/isolation and
  timeout policy are the next slice.

## 2026-07-23

- Changed `POST /workflows` to persist and queue workflows before executing the
  existing worker as a FastAPI background task; it now returns `202 Accepted`
  with the initial replayed snapshot.
- Added `GET /workflows/{workflow_id}/events` for append-ordered lifecycle
  event inspection and focused API coverage; the backend suite now has 75
  passing tests.
- Added `ProviderRouter`, `SingleProviderRouter`, and `RoutedTaskProvider` to
  separate provider selection from worker execution without changing local
  one-provider behavior; added focused router tests.
- Added a process-local `InMemoryResponseCache` and `CachedTaskProvider` around provider execution.
- Cache keys cover output-affecting task fields, successful outputs are reused across equivalent tasks, and provider failures are not cached.
- Added cache unit tests and API wiring coverage; the backend suite now has 71 passing tests.
- Updated architecture, components, API, state-management, roadmap, status, task, and decision documentation for the completed caching slice.
- Added `WorkflowRecovery` to rebuild an in-memory workflow queue from persisted lifecycle events and resume unfinished local workflows.
- Requeues interrupted running tasks with incremented attempts, preserves completed outputs, and writes missing terminal workflow events after interrupted finalization.
- Added `POST /workflows/{workflow_id}/recover` and focused API/recovery tests.
- Updated the knowledge base and journey documentation for the completed recovery slice.

## 2026-07-21

- Added the FastAPI application in `backend/src/ather_os/api/app.py` with synchronous workflow submission and persisted replay-backed status routes.
- Added API tests for successful execution, status retrieval after app recreation, invalid graphs, missing workflows, and duplicate IDs.
- Added `httpx` as an explicit development dependency for FastAPI endpoint tests.
- Updated the backend README and API, roadmap, status, tasks, bugs, and journey documentation for the completed API slice.

## 2026-07-21

- Added `TaskProvider` and deterministic `MockProvider` under `backend/src/ather_os/providers/`.
- Added `WorkflowWorker` under `backend/src/ather_os/worker/` to execute dependency-ready tasks through [[Queue Lifecycle Service]].
- Added terminal task/workflow failure recording and final workflow completion recording to [[Queue Lifecycle Service]].
- Added replay-backed `WorkflowStatusQuery` for current workflow/task snapshots from a [[State Store]].
- Added execution tests covering dependency ordering, successful completion, and provider failure; the backend suite now has 57 passing tests.
- Updated roadmap, tasks, current status, and bugs documentation to reflect the completed local execution slice.

## 2026-07-19

- Added [[Queue Lifecycle Service]] in `backend/src/ather_os/queue/lifecycle.py` to coordinate local queue transitions with append-only lifecycle events.
- Added pytest coverage for submission, task claim/completion, dependency unblocking event order, and invalid completion handling.
- Updated the knowledge base so the next engineering step is an in-process [[Worker]] loop using the lifecycle service.
- Added the minimal [[Queue Broker]] protocol in `backend/src/ather_os/queue/broker.py`.
- Added dependency-aware `InMemoryQueueBroker` in `backend/src/ather_os/queue/memory.py` using only standard Python data structures.
- Added pytest coverage for queue submission, task claiming, dependency unblocking, duplicate workflow submission, and unknown workflow/task errors.
- Added [[Queue Broker]] documentation and updated architecture, components, state management, current status, and tasks docs so the next backend step is worker integration.

## 2026-07-13

- Added typed workflow/task lifecycle events in `backend/src/ather_os/state/events.py`.
- Added the minimal [[State Store]] protocol in `backend/src/ather_os/state/store.py`.
- Added `SQLiteStateStore` in `backend/src/ather_os/state/sqlite.py` using Python's standard `sqlite3` module.
- Added pytest coverage for lifecycle event validation, event JSON parsing, SQLite append ordering, workflow filtering, persistence across store instances, and duplicate event IDs.
- Added [[State Store]] documentation and updated architecture, database, state management, roadmap, tasks, decisions, current status, and folder structure docs to reflect the implemented persistence foundation.
- Added [[Checkpoint Engine]] projection models in `backend/src/ather_os/checkpoint/models.py`.
- Added `replay_workflow(events)` in `backend/src/ather_os/checkpoint/replay.py`.
- Added pytest coverage for workflow submission replay, task queue/start/completion/failure replay, workflow completion/failure replay, and invalid event logs.
- Added [[Checkpoint Engine]] documentation and updated the knowledge base so the next backend step is now [[Queue Broker]] scheduling.

## 2026-07-09

- Renamed and reformatted the project master document as `AtherOS_Project_Master_Document.md` for easier Markdown viewing.
- Added pytest coverage for [[DAG Models]] field constraints in `backend/tests/test_dag_models.py`.
- Covered task type and quality tier values, default quality, prompt and goal minimum lengths, token bounds, retry bounds, and workflow task count limits.
- Updated [[10_Current_Status|Current Status]] and [[11_Tasks|Tasks]] so the knowledge base reflects the expanded DAG foundation test coverage.
- Added sample workflow JSON files under `backend/samples/`.
- Added a minimal workflow validation command in `backend/src/ather_os/dag/validate_workflow.py`.
- Added pytest coverage for valid and invalid workflow samples in `backend/tests/test_validate_workflow_command.py`.
- Updated [[09_Roadmap|Roadmap]] and [[11_Tasks|Tasks]] so the next backend step is now the local [[State Store]] interface.

## 2026-07-08

- Added [[DAG Validator]] in `backend/src/ather_os/dag/validators.py`.
- Added `DagValidationError` and `validate_workflow_graph(workflow: Workflow) -> None`.
- Added pytest coverage for duplicate task IDs, unknown dependencies, self-dependencies, dependency cycles, multiple roots, disconnected roots, and valid connected DAGs.
- Updated documentation to mark DAG structural validation as implemented.
- Added `/docs` Obsidian knowledge base.
- Documented actual current implementation across overview, architecture, folder structure, database, APIs, components, state management, authentication, UI, roadmap, current status, tasks, bugs, decisions, and changelog.
- Recorded that [[DAG Models]] are the only substantive implemented domain logic.
- Recorded that [[04_APIs|APIs]], [[03_Database|Database]], [[Checkpoint Engine]], [[Response Cache]], [[Provider Router]], [[Queue Broker]], [[State Store]], [[Worker]], [[Frontend]], and [[07_Authentication|Authentication]] are not implemented yet.

## Earlier Repository State

Based on `JOURNEY.md`, the initial project shape was created on Sunday, 17 May:

- Root `README.md`.
- `JOURNEY.md`.
- `backend/` and `frontend/` folders.
- `backend/pyproject.toml`.
- Backend package skeleton under `backend/src/ather_os/`.
- Initial [[DAG Models]] in `backend/src/ather_os/dag/models.py`.
- Backend virtual environment and installed dependencies.

## Related

- [[10_Current_Status|Current Status]]
- [[11_Tasks|Tasks]]
- [[13_Decisions|Decisions]]
