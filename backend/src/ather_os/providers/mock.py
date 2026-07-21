from collections.abc import Iterable
from uuid import UUID

from ather_os.dag.models import Task


class MockProvider:
    """Deterministic local provider for exercising workflow execution."""

    def __init__(self, failing_task_ids: Iterable[UUID] = ()) -> None:
        self._failing_task_ids = set(failing_task_ids)

    def execute(self, task: Task) -> str:
        if task.task_id in self._failing_task_ids:
            raise RuntimeError(f"Mock provider failed task {task.task_id}.")

        return f"Mock {task.type.value} output: {task.prompt}"
