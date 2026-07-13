from typing import Protocol
from uuid import UUID

from ather_os.state.events import WorkflowEvent


class StateStore(Protocol):
    """Append-only workflow lifecycle event storage."""

    def append_event(self, event: WorkflowEvent) -> None:
        """Persist one workflow event."""

    def list_events(self, workflow_id: UUID) -> list[WorkflowEvent]:
        """Return stored events for a workflow in append order."""
