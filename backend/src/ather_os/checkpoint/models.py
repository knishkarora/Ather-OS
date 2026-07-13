from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel


class WorkflowStatus(StrEnum):
    """Current lifecycle status for a replayed workflow."""

    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskStatus(StrEnum):
    """Current lifecycle status for a replayed task."""

    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskSnapshot(BaseModel):
    """Current replayed state for one task."""

    task_id: UUID
    status: TaskStatus = TaskStatus.PENDING
    attempt: int = 0
    output: str | None = None
    error: str | None = None


class WorkflowSnapshot(BaseModel):
    """Current replayed state for one workflow."""

    workflow_id: UUID
    goal: str
    status: WorkflowStatus = WorkflowStatus.PENDING
    tasks: dict[UUID, TaskSnapshot]
    error: str | None = None
