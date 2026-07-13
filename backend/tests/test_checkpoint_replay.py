from uuid import UUID

import pytest

from ather_os.checkpoint import (
    CheckpointReplayError,
    TaskStatus,
    WorkflowStatus,
    replay_workflow,
)
from ather_os.state import (
    TaskCompleted,
    TaskFailed,
    TaskQueued,
    TaskStarted,
    WorkflowCompleted,
    WorkflowFailed,
    WorkflowSubmitted,
)


WORKFLOW_ID = UUID("00000000-0000-0000-0000-000000000001")
OTHER_WORKFLOW_ID = UUID("00000000-0000-0000-0000-000000000002")
TASK_A = UUID("00000000-0000-0000-0000-000000000101")
TASK_B = UUID("00000000-0000-0000-0000-000000000102")
UNKNOWN_TASK = UUID("00000000-0000-0000-0000-000000000999")


def test_replay_submitted_workflow_starts_pending() -> None:
    snapshot = replay_workflow([_submitted()])

    assert snapshot.workflow_id == WORKFLOW_ID
    assert snapshot.goal == "Test checkpoint replay"
    assert snapshot.status == WorkflowStatus.PENDING
    assert snapshot.tasks[TASK_A].status == TaskStatus.PENDING
    assert snapshot.tasks[TASK_B].status == TaskStatus.PENDING


def test_replay_task_lifecycle_updates_task_status() -> None:
    snapshot = replay_workflow(
        [
            _submitted(),
            TaskQueued(workflow_id=WORKFLOW_ID, task_id=TASK_A),
            TaskStarted(workflow_id=WORKFLOW_ID, task_id=TASK_A, attempt=2),
            TaskCompleted(
                workflow_id=WORKFLOW_ID,
                task_id=TASK_A,
                output="Finished task",
            ),
        ]
    )

    task = snapshot.tasks[TASK_A]

    assert task.status == TaskStatus.COMPLETED
    assert task.attempt == 2
    assert task.output == "Finished task"
    assert task.error is None


def test_replay_failed_task_marks_task_failed() -> None:
    snapshot = replay_workflow(
        [
            _submitted(),
            TaskStarted(workflow_id=WORKFLOW_ID, task_id=TASK_A),
            TaskFailed(workflow_id=WORKFLOW_ID, task_id=TASK_A, error="Provider failed"),
        ]
    )

    task = snapshot.tasks[TASK_A]

    assert task.status == TaskStatus.FAILED
    assert task.error == "Provider failed"


def test_replay_completed_workflow_marks_workflow_complete() -> None:
    snapshot = replay_workflow([_submitted(), WorkflowCompleted(workflow_id=WORKFLOW_ID)])

    assert snapshot.status == WorkflowStatus.COMPLETED
    assert snapshot.error is None


def test_replay_failed_workflow_marks_workflow_failed() -> None:
    snapshot = replay_workflow(
        [
            _submitted(),
            WorkflowFailed(workflow_id=WORKFLOW_ID, error="No executable tasks remain"),
        ]
    )

    assert snapshot.status == WorkflowStatus.FAILED
    assert snapshot.error == "No executable tasks remain"


def test_replay_rejects_empty_event_list() -> None:
    with pytest.raises(CheckpointReplayError):
        replay_workflow([])


def test_replay_rejects_event_log_without_submission() -> None:
    with pytest.raises(CheckpointReplayError):
        replay_workflow([TaskQueued(workflow_id=WORKFLOW_ID, task_id=TASK_A)])


def test_replay_rejects_mixed_workflow_events() -> None:
    with pytest.raises(CheckpointReplayError):
        replay_workflow(
            [
                _submitted(),
                WorkflowFailed(workflow_id=OTHER_WORKFLOW_ID, error="Wrong workflow"),
            ]
        )


def test_replay_rejects_unknown_task_events() -> None:
    with pytest.raises(CheckpointReplayError):
        replay_workflow(
            [
                _submitted(),
                TaskQueued(workflow_id=WORKFLOW_ID, task_id=UNKNOWN_TASK),
            ]
        )


def _submitted() -> WorkflowSubmitted:
    return WorkflowSubmitted(
        workflow_id=WORKFLOW_ID,
        goal="Test checkpoint replay",
        task_ids=[TASK_A, TASK_B],
    )
