from uuid import UUID

from ather_os.checkpoint import TaskStatus, WorkflowStatus, WorkflowStatusQuery
from ather_os.dag import Task, TaskType, Workflow
from ather_os.providers import MockProvider
from ather_os.queue import InMemoryQueueBroker, WorkflowQueueService
from ather_os.state import (
    SQLiteStateStore,
    TaskCompleted,
    TaskFailed,
    TaskQueued,
    TaskStarted,
    WorkflowCompleted,
    WorkflowSubmitted,
)
from ather_os.worker import WorkflowRecovery


WORKFLOW_ID = UUID("00000000-0000-0000-0000-000000000001")
TASK_A = UUID("00000000-0000-0000-0000-000000000101")
TASK_B = UUID("00000000-0000-0000-0000-000000000102")


def test_recovery_requeues_interrupted_task_and_increments_attempt(tmp_path) -> None:
    database_path = tmp_path / "ather-os.sqlite3"
    first_store = SQLiteStateStore(database_path)
    first_service = WorkflowQueueService(InMemoryQueueBroker(), first_store)
    first_service.submit_workflow(_workflow())
    first_service.claim_next_task(WORKFLOW_ID)

    second_store = SQLiteStateStore(database_path)
    second_service = WorkflowQueueService(InMemoryQueueBroker(), second_store)
    provider = RecordingMockProvider()
    snapshot = WorkflowRecovery(
        second_store,
        second_service,
        provider,
        WorkflowStatusQuery(second_store),
    ).recover_workflow(WORKFLOW_ID)

    started = [
        event
        for event in second_store.list_events(WORKFLOW_ID)
        if isinstance(event, TaskStarted) and event.task_id == TASK_A
    ]
    queued = [
        event
        for event in second_store.list_events(WORKFLOW_ID)
        if isinstance(event, TaskQueued) and event.task_id == TASK_A
    ]

    assert provider.executed_task_ids == [TASK_A, TASK_B]
    assert snapshot.status == WorkflowStatus.COMPLETED
    assert snapshot.tasks[TASK_A].attempt == 2
    assert [event.attempt for event in started] == [1, 2]
    assert len(queued) == 2


def test_recovery_keeps_completed_tasks_and_resumes_existing_queue(tmp_path) -> None:
    database_path = tmp_path / "ather-os.sqlite3"
    first_store = SQLiteStateStore(database_path)
    first_service = WorkflowQueueService(InMemoryQueueBroker(), first_store)
    first_service.submit_workflow(_workflow())
    first_service.claim_next_task(WORKFLOW_ID)
    first_service.complete_task(WORKFLOW_ID, TASK_A, "Original task output")

    second_store = SQLiteStateStore(database_path)
    second_service = WorkflowQueueService(InMemoryQueueBroker(), second_store)
    provider = RecordingMockProvider()
    snapshot = WorkflowRecovery(
        second_store,
        second_service,
        provider,
        WorkflowStatusQuery(second_store),
    ).recover_workflow(WORKFLOW_ID)

    assert provider.executed_task_ids == [TASK_B]
    assert snapshot.status == WorkflowStatus.COMPLETED
    assert snapshot.tasks[TASK_A].status == TaskStatus.COMPLETED
    assert snapshot.tasks[TASK_A].output == "Original task output"


def test_recovery_finalizes_completed_workflow_after_interrupted_terminal_event(tmp_path) -> None:
    store = SQLiteStateStore(tmp_path / "ather-os.sqlite3")
    workflow = Workflow(
        workflow_id=WORKFLOW_ID,
        goal="Recover completed workflow",
        tasks=[_task(TASK_A)],
    )
    store.append_event(
        WorkflowSubmitted(
            workflow_id=WORKFLOW_ID,
            goal=workflow.goal,
            task_ids=[TASK_A],
            workflow=workflow,
        )
    )
    store.append_event(
        TaskCompleted(
            workflow_id=WORKFLOW_ID,
            task_id=TASK_A,
            output="Completed before interruption",
        )
    )

    snapshot = WorkflowRecovery(
        store,
        WorkflowQueueService(InMemoryQueueBroker(), store),
        RecordingMockProvider(),
        WorkflowStatusQuery(store),
    ).recover_workflow(WORKFLOW_ID)

    assert snapshot.status == WorkflowStatus.COMPLETED
    assert isinstance(store.list_events(WORKFLOW_ID)[-1], WorkflowCompleted)


def test_recovery_finalizes_failed_workflow_after_interrupted_terminal_event(tmp_path) -> None:
    store = SQLiteStateStore(tmp_path / "ather-os.sqlite3")
    workflow = Workflow(
        workflow_id=WORKFLOW_ID,
        goal="Recover failed workflow",
        tasks=[_task(TASK_A)],
    )
    store.append_event(
        WorkflowSubmitted(
            workflow_id=WORKFLOW_ID,
            goal=workflow.goal,
            task_ids=[TASK_A],
            workflow=workflow,
        )
    )
    store.append_event(
        TaskFailed(workflow_id=WORKFLOW_ID, task_id=TASK_A, error="Provider stopped")
    )

    snapshot = WorkflowRecovery(
        store,
        WorkflowQueueService(InMemoryQueueBroker(), store),
        RecordingMockProvider(),
        WorkflowStatusQuery(store),
    ).recover_workflow(WORKFLOW_ID)

    assert snapshot.status == WorkflowStatus.FAILED
    assert snapshot.error == "Provider stopped"


class RecordingMockProvider(MockProvider):
    def __init__(self) -> None:
        super().__init__()
        self.executed_task_ids: list[UUID] = []

    def execute(self, task: Task) -> str:
        self.executed_task_ids.append(task.task_id)
        return super().execute(task)


def _workflow() -> Workflow:
    return Workflow(
        workflow_id=WORKFLOW_ID,
        goal="Recover workflow execution",
        tasks=[
            _task(TASK_A),
            _task(TASK_B, dependencies=[TASK_A]),
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
