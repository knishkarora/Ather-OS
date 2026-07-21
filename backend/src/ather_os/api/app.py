from pathlib import Path
from uuid import UUID

from fastapi import FastAPI, HTTPException, status

from ather_os.checkpoint import CheckpointReplayError, WorkflowSnapshot, WorkflowStatusQuery
from ather_os.dag import DagValidationError, Workflow
from ather_os.providers import MockProvider, TaskProvider
from ather_os.queue import InMemoryQueueBroker, QueueBrokerError, WorkflowQueueService
from ather_os.state import SQLiteStateStore
from ather_os.worker import WorkflowRecovery, WorkflowRecoveryError, WorkflowWorker


def create_app(
    database_path: str | Path = "ather-os.sqlite3",
    provider: TaskProvider | None = None,
) -> FastAPI:
    """Create the local Ather OS API and its single-process dependencies."""

    state_store = SQLiteStateStore(database_path)
    queue_service = WorkflowQueueService(InMemoryQueueBroker(), state_store)
    status_query = WorkflowStatusQuery(state_store)
    task_provider = provider or MockProvider()
    worker = WorkflowWorker(queue_service, task_provider, status_query)
    recovery = WorkflowRecovery(
        state_store, queue_service, task_provider, status_query
    )

    app = FastAPI(title="Ather OS", version="0.1.0")
    app.state.state_store = state_store
    app.state.queue_service = queue_service
    app.state.status_query = status_query
    app.state.worker = worker
    app.state.recovery = recovery

    @app.post(
        "/workflows",
        response_model=WorkflowSnapshot,
        status_code=status.HTTP_201_CREATED,
    )
    def submit_workflow(workflow: Workflow) -> WorkflowSnapshot:
        """Validate, execute, and return the current snapshot of a workflow."""

        if state_store.list_events(workflow.workflow_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Workflow {workflow.workflow_id} already exists.",
            )

        try:
            queue_service.submit_workflow(workflow)
        except DagValidationError as error:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=str(error),
            ) from error
        except QueueBrokerError as error:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(error),
            ) from error

        return worker.run_workflow(workflow.workflow_id)

    @app.get("/workflows/{workflow_id}", response_model=WorkflowSnapshot)
    def get_workflow(workflow_id: UUID) -> WorkflowSnapshot:
        """Return the persisted replayed status for one workflow."""

        try:
            return status_query.get_workflow(workflow_id)
        except CheckpointReplayError as error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Workflow {workflow_id} was not found.",
            ) from error

    @app.post("/workflows/{workflow_id}/recover", response_model=WorkflowSnapshot)
    def recover_workflow(workflow_id: UUID) -> WorkflowSnapshot:
        """Restore local queue state from events and resume an unfinished workflow."""

        try:
            return recovery.recover_workflow(workflow_id)
        except CheckpointReplayError as error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Workflow {workflow_id} was not found.",
            ) from error
        except WorkflowRecoveryError as error:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=str(error),
            ) from error

    return app


app = create_app()
