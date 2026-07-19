from uuid import UUID

import pytest

from ather_os.dag import Task, TaskType, Workflow
from ather_os.queue import InMemoryQueueBroker, QueueBrokerError, WorkflowQueueService
from ather_os.state import TaskCompleted, TaskQueued, TaskStarted, WorkflowSubmitted


WORKFLOW_ID = UUID("00000000-0000-0000-0000-000000000001")
TASK_A = UUID("00000000-0000-0000-0000-000000000101")
TASK_B = UUID("00000000-0000-0000-0000-000000000102")
TASK_C = UUID("00000000-0000-0000-0000-000000000103")
UNKNOWN_TASK = UUID("00000000-0000-0000-0000-000000009999")


class MemoryStateStore:
    """Test double that keeps appended events in memory."""

    def __init__(self) -> None:
        self.events: list = []

    def append_event(self, event) -> None:
        self.events.append(event)

    def list_events(self, workflow_id: UUID) -> list:
        return [event for event in self.events if event.workflow_id == workflow_id]


def test_submission_records_workflow_and_initially_queued_task() -> None:
    state_store = MemoryStateStore()
    service = WorkflowQueueService(InMemoryQueueBroker(), state_store)

    ready_tasks = service.submit_workflow(_workflow())

    assert [task.task_id for task in ready_tasks] == [TASK_A]
    submitted, queued = state_store.events
    assert isinstance(submitted, WorkflowSubmitted)
    assert submitted.workflow_id == WORKFLOW_ID
    assert submitted.goal == "Test workflow"
    assert submitted.task_ids == [TASK_A, TASK_B, TASK_C]
    assert isinstance(queued, TaskQueued)
    assert queued.task_id == TASK_A


def test_claiming_and_completing_task_records_lifecycle_events() -> None:
    state_store = MemoryStateStore()
    service = WorkflowQueueService(InMemoryQueueBroker(), state_store)
    service.submit_workflow(_workflow())

    claimed_task = service.claim_next_task(WORKFLOW_ID, attempt=2)
    ready_tasks = service.complete_task(WORKFLOW_ID, TASK_A, "Finished task A")

    assert claimed_task is not None
    assert claimed_task.task_id == TASK_A
    assert [task.task_id for task in ready_tasks] == [TASK_B, TASK_C]
    started, completed, first_queued, second_queued = state_store.events[2:]
    assert isinstance(started, TaskStarted)
    assert started.task_id == TASK_A
    assert started.attempt == 2
    assert isinstance(completed, TaskCompleted)
    assert completed.task_id == TASK_A
    assert completed.output == "Finished task A"
    assert isinstance(first_queued, TaskQueued)
    assert first_queued.task_id == TASK_B
    assert isinstance(second_queued, TaskQueued)
    assert second_queued.task_id == TASK_C


def test_invalid_completion_does_not_append_event() -> None:
    state_store = MemoryStateStore()
    service = WorkflowQueueService(InMemoryQueueBroker(), state_store)
    service.submit_workflow(_workflow())

    with pytest.raises(QueueBrokerError, match="not part of workflow"):
        service.complete_task(WORKFLOW_ID, UNKNOWN_TASK, "Unexpected task")

    assert len(state_store.events) == 2


def _workflow() -> Workflow:
    return Workflow(
        workflow_id=WORKFLOW_ID,
        goal="Test workflow",
        tasks=[
            _task(TASK_A),
            _task(TASK_B, dependencies=[TASK_A]),
            _task(TASK_C, dependencies=[TASK_A]),
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
