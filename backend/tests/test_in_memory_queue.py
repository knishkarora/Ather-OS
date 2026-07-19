from uuid import UUID

import pytest

from ather_os.dag import Task, TaskType, Workflow
from ather_os.queue import InMemoryQueueBroker, QueueBrokerError


WORKFLOW_ID = UUID("00000000-0000-0000-0000-000000000001")
OTHER_WORKFLOW_ID = UUID("00000000-0000-0000-0000-000000000002")
TASK_A = UUID("00000000-0000-0000-0000-000000000101")
TASK_B = UUID("00000000-0000-0000-0000-000000000102")
TASK_C = UUID("00000000-0000-0000-0000-000000000103")
TASK_D = UUID("00000000-0000-0000-0000-000000000104")
UNKNOWN_TASK = UUID("00000000-0000-0000-0000-000000009999")


def test_submitting_workflow_queues_root_task_only() -> None:
    broker = InMemoryQueueBroker()

    ready_tasks = broker.submit_workflow(_workflow())

    assert [task.task_id for task in ready_tasks] == [TASK_A]


def test_claim_next_task_returns_ready_tasks_in_queue_order() -> None:
    broker = InMemoryQueueBroker()
    broker.submit_workflow(_workflow())

    first_task = broker.claim_next_task(WORKFLOW_ID)
    second_task = broker.claim_next_task(WORKFLOW_ID)

    assert first_task is not None
    assert first_task.task_id == TASK_A
    assert second_task is None


def test_completing_task_queues_newly_unblocked_dependents() -> None:
    broker = InMemoryQueueBroker()
    broker.submit_workflow(_workflow())
    broker.claim_next_task(WORKFLOW_ID)

    ready_tasks = broker.mark_task_completed(WORKFLOW_ID, TASK_A)

    assert [task.task_id for task in ready_tasks] == [TASK_B, TASK_C]
    assert broker.claim_next_task(WORKFLOW_ID).task_id == TASK_B
    assert broker.claim_next_task(WORKFLOW_ID).task_id == TASK_C


def test_task_waits_until_all_dependencies_complete() -> None:
    broker = InMemoryQueueBroker()
    broker.submit_workflow(_workflow())

    broker.mark_task_completed(WORKFLOW_ID, TASK_A)
    broker.claim_next_task(WORKFLOW_ID)
    broker.claim_next_task(WORKFLOW_ID)

    assert broker.mark_task_completed(WORKFLOW_ID, TASK_B) == []

    ready_tasks = broker.mark_task_completed(WORKFLOW_ID, TASK_C)

    assert [task.task_id for task in ready_tasks] == [TASK_D]


def test_completing_same_task_twice_does_not_requeue_dependents() -> None:
    broker = InMemoryQueueBroker()
    broker.submit_workflow(_workflow())

    first_ready_tasks = broker.mark_task_completed(WORKFLOW_ID, TASK_A)
    second_ready_tasks = broker.mark_task_completed(WORKFLOW_ID, TASK_A)

    assert [task.task_id for task in first_ready_tasks] == [TASK_B, TASK_C]
    assert second_ready_tasks == []


def test_rejects_duplicate_workflow_submission() -> None:
    broker = InMemoryQueueBroker()
    workflow = _workflow()
    broker.submit_workflow(workflow)

    with pytest.raises(QueueBrokerError, match="already queued"):
        broker.submit_workflow(workflow)


def test_rejects_unknown_workflow_completion() -> None:
    broker = InMemoryQueueBroker()

    with pytest.raises(QueueBrokerError, match="not queued"):
        broker.mark_task_completed(OTHER_WORKFLOW_ID, TASK_A)


def test_rejects_unknown_task_completion() -> None:
    broker = InMemoryQueueBroker()
    broker.submit_workflow(_workflow())

    with pytest.raises(QueueBrokerError, match="not part of workflow"):
        broker.mark_task_completed(WORKFLOW_ID, UNKNOWN_TASK)


def _workflow() -> Workflow:
    return Workflow(
        workflow_id=WORKFLOW_ID,
        goal="Test workflow",
        tasks=[
            _task(TASK_A),
            _task(TASK_B, dependencies=[TASK_A]),
            _task(TASK_C, dependencies=[TASK_A]),
            _task(TASK_D, dependencies=[TASK_B, TASK_C]),
        ],
    )


def _task(task_id: UUID, dependencies: list[UUID] | None = None) -> Task:
    return Task(
        task_id=task_id,
        type=TaskType.RESEARCH,
        prompt=f"Run task {task_id}",
        dependencies=dependencies or [],
        estimated_tokens=100,
    )
