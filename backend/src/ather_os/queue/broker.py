from typing import Protocol
from uuid import UUID

from ather_os.dag.models import Task, Workflow


class QueueBroker(Protocol):
    """Minimal task scheduling contract for local workflow execution."""

    def submit_workflow(self, workflow: Workflow) -> list[Task]:
        """Add a workflow and return tasks ready to run immediately."""

    def mark_task_completed(self, workflow_id: UUID, task_id: UUID) -> list[Task]:
        """Mark a task complete and return newly unblocked tasks."""

    def claim_next_task(self, workflow_id: UUID) -> Task | None:
        """Return the next queued task for a workflow, if one is available."""

