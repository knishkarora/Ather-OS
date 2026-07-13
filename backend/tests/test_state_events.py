from uuid import UUID

import pytest
from pydantic import ValidationError

from ather_os.state import (
    TaskCompleted,
    TaskFailed,
    TaskStarted,
    WorkflowEventType,
    WorkflowFailed,
    WorkflowSubmitted,
)
from ather_os.state.events import parse_workflow_event


WORKFLOW_ID = UUID("00000000-0000-0000-0000-000000000001")
TASK_A = UUID("00000000-0000-0000-0000-000000000101")


def test_workflow_submitted_records_goal_and_task_ids() -> None:
    event = WorkflowSubmitted(
        workflow_id=WORKFLOW_ID,
        goal="Research durable local execution",
        task_ids=[TASK_A],
    )

    assert event.event_type == WorkflowEventType.WORKFLOW_SUBMITTED
    assert event.workflow_id == WORKFLOW_ID
    assert event.task_ids == [TASK_A]


def test_task_started_rejects_invalid_attempt() -> None:
    with pytest.raises(ValidationError):
        TaskStarted(workflow_id=WORKFLOW_ID, task_id=TASK_A, attempt=0)


@pytest.mark.parametrize(
    ("event_class", "kwargs", "field_name"),
    [
        (TaskCompleted, {"task_id": TASK_A}, "output"),
        (TaskFailed, {"task_id": TASK_A}, "error"),
        (WorkflowFailed, {}, "error"),
    ],
)
def test_terminal_events_reject_empty_detail(
    event_class: type,
    kwargs: dict,
    field_name: str,
) -> None:
    with pytest.raises(ValidationError):
        event_class(workflow_id=WORKFLOW_ID, **kwargs, **{field_name: ""})


def test_parse_workflow_event_restores_specific_event_type() -> None:
    event = TaskCompleted(
        workflow_id=WORKFLOW_ID,
        task_id=TASK_A,
        output="Finished research summary",
    )

    parsed = parse_workflow_event(event.model_dump_json())

    assert parsed == event
    assert isinstance(parsed, TaskCompleted)
