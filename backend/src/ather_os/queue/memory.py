from dataclasses import dataclass, field
from uuid import UUID

from ather_os.dag.models import Task, Workflow
from ather_os.dag.validators import validate_workflow_graph


class QueueBrokerError(ValueError):
    """Raised when queue state cannot satisfy the requested operation."""


@dataclass
class _WorkflowQueue:
    tasks_by_id: dict[UUID, Task]
    completed_task_ids: set[UUID] = field(default_factory=set)
    queued_task_ids: set[UUID] = field(default_factory=set)
    claimed_task_ids: set[UUID] = field(default_factory=set)
    ready_task_ids: list[UUID] = field(default_factory=list)


class InMemoryQueueBroker:
    """Dependency-aware in-memory queue for a single local process."""

    def __init__(self) -> None:
        self._workflows: dict[UUID, _WorkflowQueue] = {}

    def submit_workflow(self, workflow: Workflow) -> list[Task]:
        validate_workflow_graph(workflow)

        if workflow.workflow_id in self._workflows:
            raise QueueBrokerError(f"Workflow {workflow.workflow_id} is already queued.")

        queue = _WorkflowQueue(tasks_by_id={task.task_id: task for task in workflow.tasks})
        self._workflows[workflow.workflow_id] = queue
        return self._queue_ready_tasks(queue)

    def mark_task_completed(self, workflow_id: UUID, task_id: UUID) -> list[Task]:
        queue = self._get_queue(workflow_id)
        self._ensure_known_task(queue, workflow_id, task_id)

        queue.claimed_task_ids.discard(task_id)
        queue.queued_task_ids.discard(task_id)
        if task_id in queue.completed_task_ids:
            return []

        queue.completed_task_ids.add(task_id)
        return self._queue_ready_tasks(queue)

    def claim_next_task(self, workflow_id: UUID) -> Task | None:
        queue = self._get_queue(workflow_id)

        while queue.ready_task_ids:
            task_id = queue.ready_task_ids.pop(0)
            if task_id in queue.completed_task_ids:
                continue

            queue.queued_task_ids.discard(task_id)
            queue.claimed_task_ids.add(task_id)
            return queue.tasks_by_id[task_id]

        return None

    def _queue_ready_tasks(self, queue: _WorkflowQueue) -> list[Task]:
        newly_ready: list[Task] = []

        for task in queue.tasks_by_id.values():
            inactive_task_ids = (
                queue.completed_task_ids | queue.queued_task_ids | queue.claimed_task_ids
            )
            if task.task_id in inactive_task_ids:
                continue

            if all(dependency_id in queue.completed_task_ids for dependency_id in task.dependencies):
                queue.queued_task_ids.add(task.task_id)
                queue.ready_task_ids.append(task.task_id)
                newly_ready.append(task)

        return newly_ready

    def _get_queue(self, workflow_id: UUID) -> _WorkflowQueue:
        try:
            return self._workflows[workflow_id]
        except KeyError as error:
            raise QueueBrokerError(f"Workflow {workflow_id} is not queued.") from error

    def _ensure_known_task(
        self, queue: _WorkflowQueue, workflow_id: UUID, task_id: UUID
    ) -> None:
        if task_id not in queue.tasks_by_id:
            raise QueueBrokerError(f"Task {task_id} is not part of workflow {workflow_id}.")
