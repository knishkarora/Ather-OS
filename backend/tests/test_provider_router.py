from uuid import UUID

from ather_os.dag import Task, TaskType
from ather_os.providers import RoutedTaskProvider, SingleProviderRouter


TASK_ID = UUID("00000000-0000-0000-0000-000000000101")


def test_single_provider_router_selects_its_configured_provider() -> None:
    provider = RecordingProvider()
    router = SingleProviderRouter(provider)

    selected_provider = router.provider_for(_task())

    assert selected_provider is provider


def test_routed_task_provider_executes_the_selected_provider() -> None:
    provider = RecordingProvider()
    routed_provider = RoutedTaskProvider(SingleProviderRouter(provider))

    assert routed_provider.execute(_task()) == "Routed output"
    assert provider.executed_task_ids == [TASK_ID]


class RecordingProvider:
    def __init__(self) -> None:
        self.executed_task_ids: list[UUID] = []

    def execute(self, task: Task) -> str:
        self.executed_task_ids.append(task.task_id)
        return "Routed output"


def _task() -> Task:
    return Task(
        task_id=TASK_ID,
        type=TaskType.RESEARCH,
        prompt="Find relevant facts",
        estimated_tokens=100,
    )
