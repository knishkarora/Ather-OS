from uuid import UUID

from ather_os.checkpoint import TaskStatus, WorkflowStatus, WorkflowStatusQuery
from ather_os.dag import Task, TaskType, Workflow
from ather_os.providers import MockProvider
from ather_os.queue import InMemoryQueueBroker, WorkflowQueueService
from ather_os.state import TaskAttemptFailed, TaskFailed
from ather_os.worker import WorkflowWorker


WORKFLOW_ID = UUID("00000000-0000-0000-0000-000000000001")
TASK_A = UUID("00000000-0000-0000-0000-000000000101")
TASK_B = UUID("00000000-0000-0000-0000-000000000102")
TASK_C = UUID("00000000-0000-0000-0000-000000000103")
TASK_D = UUID("00000000-0000-0000-0000-000000000104")


class MemoryStateStore:
    def __init__(self) -> None:
        self.events: list = []

    def append_event(self, event) -> None:
        self.events.append(event)

    def list_events(self, workflow_id: UUID) -> list:
        return [event for event in self.events if event.workflow_id == workflow_id]


def test_worker_executes_dag_in_dependency_order_and_completes_workflow() -> None:
    state_store = MemoryStateStore()
    service = WorkflowQueueService(InMemoryQueueBroker(), state_store)
    provider = RecordingMockProvider()
    worker = WorkflowWorker(service, provider, WorkflowStatusQuery(state_store))
    service.submit_workflow(_workflow())

    snapshot = worker.run_workflow(WORKFLOW_ID)

    assert provider.executed_task_ids == [TASK_A, TASK_B, TASK_C, TASK_D]
    assert snapshot.status == WorkflowStatus.COMPLETED
    assert all(task.status == TaskStatus.COMPLETED for task in snapshot.tasks.values())
    assert snapshot.tasks[TASK_D].output == "Mock research output: Run task 00000000-0000-0000-0000-000000000104"


def test_worker_records_failure_and_does_not_run_blocked_tasks() -> None:
    state_store = MemoryStateStore()
    service = WorkflowQueueService(InMemoryQueueBroker(), state_store)
    provider = RecordingMockProvider(failing_task_ids=[TASK_A])
    worker = WorkflowWorker(service, provider, WorkflowStatusQuery(state_store))
    workflow = _workflow()
    workflow.tasks[0].max_retries = 0
    service.submit_workflow(workflow)

    snapshot = worker.run_workflow(WORKFLOW_ID)

    assert provider.executed_task_ids == [TASK_A]
    assert snapshot.status == WorkflowStatus.FAILED
    assert snapshot.tasks[TASK_A].status == TaskStatus.FAILED
    assert snapshot.tasks[TASK_A].error == "Mock provider failed task 00000000-0000-0000-0000-000000000101."
    assert snapshot.tasks[TASK_B].status == TaskStatus.PENDING


def test_worker_retries_until_a_task_succeeds() -> None:
    state_store = MemoryStateStore()
    service = WorkflowQueueService(InMemoryQueueBroker(), state_store)
    provider = FlakyMockProvider(failures_before_success=2)
    worker = WorkflowWorker(service, provider, WorkflowStatusQuery(state_store))
    workflow = Workflow(
        workflow_id=WORKFLOW_ID,
        goal="Retry workflow execution",
        tasks=[_task(TASK_A, max_retries=2)],
    )
    service.submit_workflow(workflow)

    snapshot = worker.run_workflow(WORKFLOW_ID)

    assert provider.executed_task_ids == [TASK_A, TASK_A, TASK_A]
    assert snapshot.status == WorkflowStatus.COMPLETED
    assert snapshot.tasks[TASK_A].attempt == 3
    assert len([event for event in state_store.events if isinstance(event, TaskAttemptFailed)]) == 2
    assert not any(isinstance(event, TaskFailed) for event in state_store.events)


def test_worker_fails_after_retry_budget_is_exhausted() -> None:
    state_store = MemoryStateStore()
    service = WorkflowQueueService(InMemoryQueueBroker(), state_store)
    provider = RecordingMockProvider(failing_task_ids=[TASK_A])
    worker = WorkflowWorker(service, provider, WorkflowStatusQuery(state_store))
    workflow = Workflow(
        workflow_id=WORKFLOW_ID,
        goal="Exhaust retry budget",
        tasks=[_task(TASK_A, max_retries=1)],
    )
    service.submit_workflow(workflow)

    snapshot = worker.run_workflow(WORKFLOW_ID)

    assert provider.executed_task_ids == [TASK_A, TASK_A]
    assert snapshot.status == WorkflowStatus.FAILED
    assert len([event for event in state_store.events if isinstance(event, TaskAttemptFailed)]) == 1
    assert isinstance(state_store.events[-2], TaskFailed)


class RecordingMockProvider(MockProvider):
    def __init__(self, failing_task_ids: list[UUID] | None = None) -> None:
        super().__init__(failing_task_ids or [])
        self.executed_task_ids: list[UUID] = []

    def execute(self, task: Task) -> str:
        self.executed_task_ids.append(task.task_id)
        return super().execute(task)


class FlakyMockProvider(RecordingMockProvider):
    def __init__(self, failures_before_success: int) -> None:
        super().__init__()
        self._failures_remaining = failures_before_success

    def execute(self, task: Task) -> str:
        self.executed_task_ids.append(task.task_id)
        if self._failures_remaining:
            self._failures_remaining -= 1
            raise RuntimeError(f"Temporary failure for {task.task_id}")
        return MockProvider.execute(self, task)


def _workflow() -> Workflow:
    return Workflow(
        workflow_id=WORKFLOW_ID,
        goal="Test workflow execution",
        tasks=[
            _task(TASK_A),
            _task(TASK_B, dependencies=[TASK_A]),
            _task(TASK_C, dependencies=[TASK_A]),
            _task(TASK_D, dependencies=[TASK_B, TASK_C]),
        ],
    )


def _task(
    task_id: UUID,
    dependencies: list[UUID] | None = None,
    max_retries: int = 2,
) -> Task:
    return Task(
        task_id=task_id,
        type=TaskType.RESEARCH,
        prompt=f"Run task {task_id}",
        dependencies=dependencies or [],
        estimated_tokens=100,
        max_retries=max_retries,
    )
