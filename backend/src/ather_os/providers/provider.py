from typing import Protocol

from ather_os.dag.models import Task


class TaskProvider(Protocol):
    """Execute one workflow task and return its final output."""

    def execute(self, task: Task) -> str:
        """Run the task or raise an exception when execution fails."""
