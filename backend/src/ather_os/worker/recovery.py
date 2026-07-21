from uuid import UUID

from ather_os.checkpoint import (
    TaskStatus,
    WorkflowSnapshot,
    WorkflowStatus,
    WorkflowStatusQuery,
)
from ather_os.providers.provider import TaskProvider
from ather_os.queue.lifecycle import WorkflowQueueService
from ather_os.state.events import WorkflowFailed, WorkflowSubmitted
from ather_os.state.store import StateStore
from ather_os.worker.loop import WorkflowWorker


class WorkflowRecoveryError(ValueError):
    """Raised when persisted events cannot restore a runnable workflow."""


class WorkflowRecovery:
    """Rebuild local queue state from persisted workflow lifecycle events."""

    def __init__(
        self,
        state_store: StateStore,
        queue_service: WorkflowQueueService,
        provider: TaskProvider,
        status_query: WorkflowStatusQuery,
    ) -> None:
        self._state_store = state_store
        self._queue_service = queue_service
        self._status_query = status_query
        self._worker = WorkflowWorker(queue_service, provider, status_query)

    def recover_workflow(self, workflow_id: UUID) -> WorkflowSnapshot:
        """Resume an unfinished workflow using at-least-once task execution."""

        events = self._state_store.list_events(workflow_id)
        snapshot = self._status_query.get_workflow(workflow_id)
        if snapshot.status != WorkflowStatus.PENDING:
            return snapshot

        failed_task = next(
            (task for task in snapshot.tasks.values() if task.status == TaskStatus.FAILED),
            None,
        )
        if failed_task is not None:
            error = failed_task.error or "Recovered a failed task without an error."
            self._state_store.append_event(
                WorkflowFailed(workflow_id=workflow_id, error=error)
            )
            return self._status_query.get_workflow(workflow_id)

        submitted = events[0]
        if not isinstance(submitted, WorkflowSubmitted) or submitted.workflow is None:
            raise WorkflowRecoveryError(
                "Workflow recovery requires a workflow_submitted event with a workflow definition."
            )

        completed_task_ids = {
            task.task_id
            for task in snapshot.tasks.values()
            if task.status == TaskStatus.COMPLETED
        }
        queued_task_ids = [
            task.task_id
            for task in snapshot.tasks.values()
            if task.status == TaskStatus.QUEUED
        ]
        interrupted_task_ids = [
            task.task_id
            for task in snapshot.tasks.values()
            if task.status == TaskStatus.RUNNING
        ]
        prior_attempts = {
            task.task_id: task.attempt
            for task in snapshot.tasks.values()
            if task.attempt > 0
        }

        self._queue_service.restore_workflow(
            submitted.workflow,
            completed_task_ids,
            queued_task_ids,
            interrupted_task_ids,
        )
        return self._worker.run_workflow(workflow_id, prior_attempts)
