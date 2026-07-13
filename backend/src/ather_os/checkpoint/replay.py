from uuid import UUID

from ather_os.checkpoint.models import (
    TaskSnapshot,
    TaskStatus,
    WorkflowSnapshot,
    WorkflowStatus,
)
from ather_os.state.events import (
    TaskCompleted,
    TaskFailed,
    TaskQueued,
    TaskStarted,
    WorkflowCompleted,
    WorkflowEvent,
    WorkflowFailed,
    WorkflowSubmitted,
)


class CheckpointReplayError(ValueError):
    """Raised when stored workflow events cannot be replayed."""


def replay_workflow(events: list[WorkflowEvent]) -> WorkflowSnapshot:
    """Reconstruct the current workflow snapshot from append-ordered events."""

    if not events:
        raise CheckpointReplayError("Cannot replay an empty workflow event list.")

    submitted = events[0]
    if not isinstance(submitted, WorkflowSubmitted):
        raise CheckpointReplayError("Workflow replay must start with workflow_submitted.")

    snapshot = WorkflowSnapshot(
        workflow_id=submitted.workflow_id,
        goal=submitted.goal,
        tasks={
            task_id: TaskSnapshot(task_id=task_id)
            for task_id in submitted.task_ids
        },
    )

    for event in events[1:]:
        _validate_workflow_id(snapshot.workflow_id, event)

        if isinstance(event, TaskQueued):
            task = _task(snapshot, event.task_id)
            task.status = TaskStatus.QUEUED
        elif isinstance(event, TaskStarted):
            task = _task(snapshot, event.task_id)
            task.status = TaskStatus.RUNNING
            task.attempt = event.attempt
            task.error = None
        elif isinstance(event, TaskCompleted):
            task = _task(snapshot, event.task_id)
            task.status = TaskStatus.COMPLETED
            task.output = event.output
            task.error = None
        elif isinstance(event, TaskFailed):
            task = _task(snapshot, event.task_id)
            task.status = TaskStatus.FAILED
            task.error = event.error
        elif isinstance(event, WorkflowCompleted):
            snapshot.status = WorkflowStatus.COMPLETED
            snapshot.error = None
        elif isinstance(event, WorkflowFailed):
            snapshot.status = WorkflowStatus.FAILED
            snapshot.error = event.error

    return snapshot


def _validate_workflow_id(workflow_id: UUID, event: WorkflowEvent) -> None:
    if event.workflow_id != workflow_id:
        raise CheckpointReplayError(
            f"Event {event.event_id} belongs to workflow {event.workflow_id}, not {workflow_id}."
        )


def _task(snapshot: WorkflowSnapshot, task_id: UUID) -> TaskSnapshot:
    try:
        return snapshot.tasks[task_id]
    except KeyError as exc:
        raise CheckpointReplayError(f"Event references unknown task {task_id}.") from exc
