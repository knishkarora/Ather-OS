from collections.abc import Iterable
from datetime import datetime
from uuid import UUID

from ather_os.dag.models import Task
from ather_os.providers.provider import ProviderTimeoutError


class MockProvider:
    """Deterministic local provider for exercising workflow execution."""

    def __init__(
        self,
        failing_task_ids: Iterable[UUID] = (),
        timed_out_task_ids: Iterable[UUID] = (),
    ) -> None:
        self._failing_task_ids = set(failing_task_ids)
        self._timed_out_task_ids = set(timed_out_task_ids)

    def execute(self, task: Task, deadline: datetime | None = None) -> str:
        if deadline is not None and task.task_id in self._timed_out_task_ids:
            raise ProviderTimeoutError(f"Mock provider timed out task {task.task_id}.")
        if task.task_id in self._failing_task_ids:
            raise RuntimeError(f"Mock provider failed task {task.task_id}.")

        return f"Mock {task.type.value} output: {task.prompt}"
