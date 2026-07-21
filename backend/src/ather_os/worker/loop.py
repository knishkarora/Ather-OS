from uuid import UUID

from ather_os.checkpoint.models import WorkflowSnapshot
from ather_os.checkpoint.query import WorkflowStatusQuery
from ather_os.providers.provider import TaskProvider
from ather_os.queue.lifecycle import WorkflowQueueService


class WorkflowWorker:
    """Execute all currently runnable tasks for one local workflow."""

    def __init__(
        self,
        queue_service: WorkflowQueueService,
        provider: TaskProvider,
        status_query: WorkflowStatusQuery,
    ) -> None:
        self._queue_service = queue_service
        self._provider = provider
        self._status_query = status_query

    def run_workflow(
        self, workflow_id: UUID, prior_attempts: dict[UUID, int] | None = None
    ) -> WorkflowSnapshot:
        """Run queued tasks until the workflow completes, fails, or becomes idle."""

        attempts = prior_attempts or {}
        while task := self._queue_service.claim_next_task(
            workflow_id, prior_attempts=attempts
        ):
            attempts[task.task_id] = attempts.get(task.task_id, 0) + 1
            try:
                output = self._provider.execute(task)
            except Exception as error:
                self._queue_service.fail_task(workflow_id, task.task_id, str(error))
                break
            self._queue_service.complete_task(workflow_id, task.task_id, output)

        return self._status_query.get_workflow(workflow_id)
