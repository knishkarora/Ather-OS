from uuid import UUID

import pytest

from ather_os.dag import DagValidationError, Task, TaskType, Workflow, validate_workflow_graph


WORKFLOW_ID = UUID("00000000-0000-0000-0000-000000000001")
TASK_A = UUID("00000000-0000-0000-0000-000000000101")
TASK_B = UUID("00000000-0000-0000-0000-000000000102")
TASK_C = UUID("00000000-0000-0000-0000-000000000103")
TASK_D = UUID("00000000-0000-0000-0000-000000000104")
UNKNOWN_TASK = UUID("00000000-0000-0000-0000-000000009999")


def test_validates_connected_acyclic_workflow() -> None:
    workflow = _workflow(
        [
            _task(TASK_A),
            _task(TASK_B, dependencies=[TASK_A]),
            _task(TASK_C, dependencies=[TASK_A]),
            _task(TASK_D, dependencies=[TASK_B, TASK_C]),
        ]
    )

    validate_workflow_graph(workflow)


def test_rejects_duplicate_task_ids() -> None:
    workflow = _workflow([_task(TASK_A), _task(TASK_A)])

    with pytest.raises(DagValidationError, match="duplicate task IDs"):
        validate_workflow_graph(workflow)


def test_rejects_unknown_dependency_ids() -> None:
    workflow = _workflow([_task(TASK_A), _task(TASK_B, dependencies=[UNKNOWN_TASK])])

    with pytest.raises(DagValidationError, match="unknown task IDs"):
        validate_workflow_graph(workflow)


def test_rejects_self_dependency() -> None:
    workflow = _workflow([_task(TASK_A, dependencies=[TASK_A])])

    with pytest.raises(DagValidationError, match="depends on itself"):
        validate_workflow_graph(workflow)


def test_rejects_dependency_cycle() -> None:
    workflow = _workflow(
        [
            _task(TASK_A, dependencies=[TASK_C]),
            _task(TASK_B, dependencies=[TASK_A]),
            _task(TASK_C, dependencies=[TASK_B]),
        ]
    )

    with pytest.raises(DagValidationError, match="dependency cycle"):
        validate_workflow_graph(workflow)


def test_rejects_multiple_roots() -> None:
    workflow = _workflow([_task(TASK_A), _task(TASK_B)])

    with pytest.raises(DagValidationError, match="exactly one root"):
        validate_workflow_graph(workflow)


def test_rejects_disconnected_subgraph() -> None:
    workflow = _workflow(
        [
            _task(TASK_A),
            _task(TASK_B, dependencies=[TASK_A]),
            _task(TASK_C),
            _task(TASK_D, dependencies=[TASK_C]),
        ]
    )

    with pytest.raises(DagValidationError, match="exactly one root"):
        validate_workflow_graph(workflow)


def _workflow(tasks: list[Task]) -> Workflow:
    return Workflow(workflow_id=WORKFLOW_ID, goal="Test workflow", tasks=tasks)


def _task(task_id: UUID, dependencies: list[UUID] | None = None) -> Task:
    return Task(
        task_id=task_id,
        type=TaskType.RESEARCH,
        prompt=f"Run task {task_id}",
        dependencies=dependencies or [],
        estimated_tokens=100,
    )
