from uuid import UUID

from ather_os.checkpoint.models import WorkflowSnapshot
from ather_os.checkpoint.replay import replay_workflow
from ather_os.state.store import StateStore


class WorkflowStatusQuery:
    """Load the current workflow state by replaying its stored events."""

    def __init__(self, state_store: StateStore) -> None:
        self._state_store = state_store

    def get_workflow(self, workflow_id: UUID) -> WorkflowSnapshot:
        """Return the current snapshot for one submitted workflow."""

        return replay_workflow(self._state_store.list_events(workflow_id))
