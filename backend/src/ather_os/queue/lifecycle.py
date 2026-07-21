from uuid import UUID

from ather_os.dag.models import Task, Workflow
from ather_os.queue.broker import QueueBroker
from ather_os.state.events import (
    TaskCompleted,
    TaskFailed,
    TaskQueued,
    TaskStarted,
    WorkflowCompleted,
    WorkflowFailed,
    WorkflowSubmitted,
)
from ather_os.state.store import StateStore


class WorkflowQueueService:
    """Coordinate queue scheduling with append-only workflow events."""

    def __init__(self, broker: QueueBroker, state_store: StateStore) -> None:
        self._broker = broker
        self._state_store = state_store

    def submit_workflow(self, workflow: Workflow) -> list[Task]:
        """Queue a workflow and record its submission plus initially ready tasks."""

        ready_tasks = self._broker.submit_workflow(workflow)
        self._state_store.append_event(
            WorkflowSubmitted(
                workflow_id=workflow.workflow_id,
                goal=workflow.goal,
                task_ids=[task.task_id for task in workflow.tasks],
            )
        )
        self._append_queued_tasks(workflow.workflow_id, ready_tasks)
        return ready_tasks

    def claim_next_task(self, workflow_id: UUID, attempt: int = 1) -> Task | None:
        """Claim the next task and record the beginning of its attempt."""

        task = self._broker.claim_next_task(workflow_id)
        if task is None:
            return None

        self._state_store.append_event(
            TaskStarted(
                workflow_id=workflow_id,
                task_id=task.task_id,
                attempt=attempt,
            )
        )
        return task

    def complete_task(
        self, workflow_id: UUID, task_id: UUID, output: str
    ) -> list[Task]:
        """Record a task output and queue any dependents it unblocks."""

        completed_event = TaskCompleted(
            workflow_id=workflow_id,
            task_id=task_id,
            output=output,
        )
        ready_tasks = self._broker.mark_task_completed(workflow_id, task_id)
        self._state_store.append_event(completed_event)
        self._append_queued_tasks(workflow_id, ready_tasks)
        if self._broker.is_workflow_complete(workflow_id):
            self._state_store.append_event(WorkflowCompleted(workflow_id=workflow_id))
        return ready_tasks

    def fail_task(self, workflow_id: UUID, task_id: UUID, error: str) -> None:
        """Record a terminal task failure and stop the workflow."""

        self._broker.mark_task_failed(workflow_id, task_id)
        self._state_store.append_event(
            TaskFailed(workflow_id=workflow_id, task_id=task_id, error=error)
        )
        self._state_store.append_event(WorkflowFailed(workflow_id=workflow_id, error=error))

    def _append_queued_tasks(self, workflow_id: UUID, tasks: list[Task]) -> None:
        for task in tasks:
            self._state_store.append_event(
                TaskQueued(workflow_id=workflow_id, task_id=task.task_id)
            )
