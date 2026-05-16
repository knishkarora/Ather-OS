from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field


class TaskType(StrEnum):
    """The kinds of work a task can represent inside a workflow DAG."""

    RESEARCH = "research"
    CODE_GENERATION = "code_generation"
    WRITING = "writing"
    ANALYSIS = "analysis"
    VALIDATION = "validation"


class QualityTier(StrEnum):
    """The expected quality level for a task output."""

    DRAFT = "draft"
    STANDARD = "standard"
    POLISHED = "polished"


class Task(BaseModel):
    """A single executable node in a workflow DAG."""

    task_id: UUID
    type: TaskType
    prompt: str = Field(min_length=1)
    dependencies: list[UUID] = Field(default_factory=list)
    context_needs: list[str] = Field(default_factory=list)
    estimated_tokens: int = Field(gt=0, le=8000)
    quality_tier: QualityTier = QualityTier.STANDARD
    max_retries: int = Field(default=2, ge=0)


class Workflow(BaseModel):
    """A full workflow made of tasks connected by dependency edges."""

    workflow_id: UUID
    goal: str = Field(min_length=1)
    tasks: list[Task] = Field(min_length=1, max_length=20)

