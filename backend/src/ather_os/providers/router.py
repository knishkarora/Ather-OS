from typing import Protocol

from ather_os.dag.models import Task
from ather_os.providers.provider import TaskProvider


class ProviderRouter(Protocol):
    """Choose the provider that should execute one task."""

    def provider_for(self, task: Task) -> TaskProvider:
        """Return the provider selected for the task."""


class SingleProviderRouter:
    """Route every local task to one provider until routing policy is needed."""

    def __init__(self, provider: TaskProvider) -> None:
        self._provider = provider

    def provider_for(self, task: Task) -> TaskProvider:
        return self._provider


class RoutedTaskProvider:
    """Adapt a router to the worker's existing TaskProvider boundary."""

    def __init__(self, router: ProviderRouter) -> None:
        self._router = router

    def execute(self, task: Task) -> str:
        return self._router.provider_for(task).execute(task)
