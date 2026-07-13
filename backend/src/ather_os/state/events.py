from datetime import UTC, datetime
from enum import StrEnum
import json
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class WorkflowEventType(StrEnum):
    """Event names stored in the append-only workflow event log."""

    WORKFLOW_SUBMITTED = "workflow_submitted"
    TASK_QUEUED = "task_queued"
    TASK_STARTED = "task_started"
    TASK_COMPLETED = "task_completed"
    TASK_FAILED = "task_failed"
    WORKFLOW_COMPLETED = "workflow_completed"
    WORKFLOW_FAILED = "workflow_failed"


class EventBase(BaseModel):
    """Common metadata for every workflow lifecycle event."""

    event_id: UUID = Field(default_factory=uuid4)
    workflow_id: UUID
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class WorkflowSubmitted(EventBase):
    """Recorded when a validated workflow enters local execution."""

    event_type: Literal[WorkflowEventType.WORKFLOW_SUBMITTED] = (
        WorkflowEventType.WORKFLOW_SUBMITTED
    )
    goal: str = Field(min_length=1)
    task_ids: list[UUID] = Field(min_length=1)


class TaskQueued(EventBase):
    """Recorded when a task becomes ready to execute."""

    event_type: Literal[WorkflowEventType.TASK_QUEUED] = WorkflowEventType.TASK_QUEUED
    task_id: UUID


class TaskStarted(EventBase):
    """Recorded when a worker begins a task attempt."""

    event_type: Literal[WorkflowEventType.TASK_STARTED] = WorkflowEventType.TASK_STARTED
    task_id: UUID
    attempt: int = Field(default=1, ge=1)


class TaskCompleted(EventBase):
    """Recorded when a task produces its final output."""

    event_type: Literal[WorkflowEventType.TASK_COMPLETED] = WorkflowEventType.TASK_COMPLETED
    task_id: UUID
    output: str = Field(min_length=1)


class TaskFailed(EventBase):
    """Recorded when a task attempt fails."""

    event_type: Literal[WorkflowEventType.TASK_FAILED] = WorkflowEventType.TASK_FAILED
    task_id: UUID
    error: str = Field(min_length=1)


class WorkflowCompleted(EventBase):
    """Recorded when every required task has completed."""

    event_type: Literal[WorkflowEventType.WORKFLOW_COMPLETED] = (
        WorkflowEventType.WORKFLOW_COMPLETED
    )


class WorkflowFailed(EventBase):
    """Recorded when the workflow cannot continue."""

    event_type: Literal[WorkflowEventType.WORKFLOW_FAILED] = WorkflowEventType.WORKFLOW_FAILED
    error: str = Field(min_length=1)


WorkflowEvent = (
    WorkflowSubmitted
    | TaskQueued
    | TaskStarted
    | TaskCompleted
    | TaskFailed
    | WorkflowCompleted
    | WorkflowFailed
)


EVENT_MODELS: dict[WorkflowEventType, type[EventBase]] = {
    WorkflowEventType.WORKFLOW_SUBMITTED: WorkflowSubmitted,
    WorkflowEventType.TASK_QUEUED: TaskQueued,
    WorkflowEventType.TASK_STARTED: TaskStarted,
    WorkflowEventType.TASK_COMPLETED: TaskCompleted,
    WorkflowEventType.TASK_FAILED: TaskFailed,
    WorkflowEventType.WORKFLOW_COMPLETED: WorkflowCompleted,
    WorkflowEventType.WORKFLOW_FAILED: WorkflowFailed,
}


def parse_workflow_event(payload: str) -> WorkflowEvent:
    """Rebuild a typed workflow event from its stored JSON payload."""

    event_type = WorkflowEventType(json.loads(payload)["event_type"])
    return EVENT_MODELS[event_type].model_validate_json(payload)
