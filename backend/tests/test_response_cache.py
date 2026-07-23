from uuid import UUID

from ather_os.cache import InMemoryResponseCache
from ather_os.dag import QualityTier, Task, TaskType
from ather_os.providers import CachedTaskProvider, task_cache_key


FIRST_TASK_ID = UUID("00000000-0000-0000-0000-000000000101")
SECOND_TASK_ID = UUID("00000000-0000-0000-0000-000000000102")


def test_cached_provider_reuses_equivalent_task_output() -> None:
    provider = RecordingProvider()
    cached_provider = CachedTaskProvider(provider, InMemoryResponseCache())

    first_output = cached_provider.execute(_task(FIRST_TASK_ID))
    second_output = cached_provider.execute(_task(SECOND_TASK_ID))

    assert first_output == second_output == "Provider output 1"
    assert provider.calls == 1


def test_cached_provider_does_not_store_provider_failures() -> None:
    provider = FailingThenSuccessfulProvider()
    cached_provider = CachedTaskProvider(provider, InMemoryResponseCache())
    task = _task(FIRST_TASK_ID)

    try:
        cached_provider.execute(task)
    except RuntimeError as error:
        assert str(error) == "Provider unavailable"
    else:
        raise AssertionError("Expected the provider failure to be propagated.")

    assert cached_provider.execute(task) == "Recovered output"
    assert provider.calls == 2


def test_task_cache_key_changes_when_output_affecting_fields_change() -> None:
    task = _task(FIRST_TASK_ID)
    changed_task = task.model_copy(update={"quality_tier": QualityTier.POLISHED})

    assert task_cache_key(task) != task_cache_key(changed_task)


class RecordingProvider:
    def __init__(self) -> None:
        self.calls = 0

    def execute(self, task: Task) -> str:
        self.calls += 1
        return f"Provider output {self.calls}"


class FailingThenSuccessfulProvider:
    def __init__(self) -> None:
        self.calls = 0

    def execute(self, task: Task) -> str:
        self.calls += 1
        if self.calls == 1:
            raise RuntimeError("Provider unavailable")
        return "Recovered output"


def _task(task_id: UUID) -> Task:
    return Task(
        task_id=task_id,
        type=TaskType.RESEARCH,
        prompt="Find relevant facts",
        context_needs=["source list"],
        estimated_tokens=100,
    )
