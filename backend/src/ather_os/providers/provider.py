from datetime import datetime
from typing import Protocol

from ather_os.dag.models import Task


class TaskProvider(Protocol):
    """Execute one workflow task and return its final output."""

    def execute(self, task: Task, deadline: datetime | None = None) -> str:
        """Run the task before its deadline or raise an execution error."""


class ProviderTimeoutError(TimeoutError):
    """Raised by a provider that cannot finish before a supplied deadline."""
