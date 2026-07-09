from uuid import UUID

import pytest
from pydantic import ValidationError

from ather_os.dag import QualityTier, Task, TaskType, Workflow


WORKFLOW_ID = UUID("00000000-0000-0000-0000-000000000001")
TASK_A = UUID("00000000-0000-0000-0000-000000000101")


def test_task_accepts_supported_type_and_quality_values() -> None:
    task = _task(type=TaskType.CODE_GENERATION, quality_tier=QualityTier.POLISHED)

    assert task.type == TaskType.CODE_GENERATION
    assert task.quality_tier == QualityTier.POLISHED


def test_task_defaults_to_standard_quality_tier() -> None:
    task = _task()

    assert task.quality_tier == QualityTier.STANDARD


def test_task_rejects_empty_prompt() -> None:
    with pytest.raises(ValidationError):
        _task(prompt="")


@pytest.mark.parametrize("estimated_tokens", [1, 8000])
def test_task_accepts_valid_estimated_token_bounds(estimated_tokens: int) -> None:
    task = _task(estimated_tokens=estimated_tokens)

    assert task.estimated_tokens == estimated_tokens


@pytest.mark.parametrize("estimated_tokens", [0, 8001])
def test_task_rejects_invalid_estimated_token_bounds(estimated_tokens: int) -> None:
    with pytest.raises(ValidationError):
        _task(estimated_tokens=estimated_tokens)


def test_task_rejects_negative_max_retries() -> None:
    with pytest.raises(ValidationError):
        _task(max_retries=-1)


def test_workflow_rejects_empty_goal() -> None:
    with pytest.raises(ValidationError):
        Workflow(workflow_id=WORKFLOW_ID, goal="", tasks=[_task()])


def test_workflow_rejects_empty_task_list() -> None:
    with pytest.raises(ValidationError):
        Workflow(workflow_id=WORKFLOW_ID, goal="Test workflow", tasks=[])


def test_workflow_accepts_twenty_tasks() -> None:
    tasks = [_task(task_id=_task_id(index)) for index in range(20)]

    workflow = Workflow(workflow_id=WORKFLOW_ID, goal="Test workflow", tasks=tasks)

    assert len(workflow.tasks) == 20


def test_workflow_rejects_more_than_twenty_tasks() -> None:
    tasks = [_task(task_id=_task_id(index)) for index in range(21)]

    with pytest.raises(ValidationError):
        Workflow(workflow_id=WORKFLOW_ID, goal="Test workflow", tasks=tasks)


def _task(
    task_id: UUID = TASK_A,
    type: TaskType = TaskType.RESEARCH,
    prompt: str = "Run task",
    estimated_tokens: int = 100,
    quality_tier: QualityTier = QualityTier.STANDARD,
    max_retries: int = 2,
) -> Task:
    return Task(
        task_id=task_id,
        type=type,
        prompt=prompt,
        estimated_tokens=estimated_tokens,
        quality_tier=quality_tier,
        max_retries=max_retries,
    )


def _task_id(index: int) -> UUID:
    return UUID(f"00000000-0000-0000-0000-{index + 101:012d}")
