from datetime import datetime
from typing import Protocol
from uuid import UUID

from ather_os.state.events import WorkflowEvent


class StateStore(Protocol):
    """Append-only workflow lifecycle event storage."""

    def append_event(self, event: WorkflowEvent) -> None:
        """Persist one workflow event."""

    def list_events(self, workflow_id: UUID) -> list[WorkflowEvent]:
        """Return stored events for a workflow in append order."""

    def list_unfinished_workflow_ids(self) -> list[UUID]:
        """Return workflows without a terminal lifecycle event."""

    def try_acquire_workflow_lease(
        self,
        workflow_id: UUID,
        owner_id: UUID,
        expires_at: datetime,
        now: datetime,
    ) -> bool:
        """Atomically acquire an expired or unowned local workflow lease."""
