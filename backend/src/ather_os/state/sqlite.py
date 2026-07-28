import sqlite3
from datetime import datetime
from pathlib import Path
from uuid import UUID

from ather_os.state.events import WorkflowEvent, parse_workflow_event


class SQLiteStateStore:
    """SQLite-backed append-only workflow event store."""

    def __init__(self, database_path: str | Path) -> None:
        self.database_path = Path(database_path)
        self._initialize()

    def append_event(self, event: WorkflowEvent) -> None:
        payload = event.model_dump_json()
        task_id = getattr(event, "task_id", None)

        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO workflow_events (
                    event_id,
                    workflow_id,
                    task_id,
                    event_type,
                    occurred_at,
                    payload
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    str(event.event_id),
                    str(event.workflow_id),
                    str(task_id) if task_id else None,
                    event.event_type,
                    event.occurred_at.isoformat(),
                    payload,
                ),
            )

    def list_events(self, workflow_id: UUID) -> list[WorkflowEvent]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT payload
                FROM workflow_events
                WHERE workflow_id = ?
                ORDER BY sequence
                """,
                (str(workflow_id),),
            ).fetchall()

        return [parse_workflow_event(row["payload"]) for row in rows]

    def list_unfinished_workflow_ids(self) -> list[UUID]:
        """Return workflows that have not reached a terminal event."""

        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT DISTINCT submitted.workflow_id
                FROM workflow_events AS submitted
                WHERE submitted.event_type = 'workflow_submitted'
                AND NOT EXISTS (
                    SELECT 1
                    FROM workflow_events AS terminal
                    WHERE terminal.workflow_id = submitted.workflow_id
                    AND terminal.event_type IN ('workflow_completed', 'workflow_failed')
                )
                ORDER BY submitted.sequence
                """
            ).fetchall()

        return [UUID(row["workflow_id"]) for row in rows]

    def try_acquire_workflow_lease(
        self,
        workflow_id: UUID,
        owner_id: UUID,
        expires_at: datetime,
        now: datetime,
    ) -> bool:
        """Atomically claim a workflow when its existing lease has expired."""

        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO workflow_leases (workflow_id, owner_id, expires_at)
                VALUES (?, ?, ?)
                ON CONFLICT(workflow_id) DO UPDATE SET
                    owner_id = excluded.owner_id,
                    expires_at = excluded.expires_at
                WHERE workflow_leases.expires_at <= ?
                """,
                (
                    str(workflow_id),
                    str(owner_id),
                    expires_at.isoformat(),
                    now.isoformat(),
                ),
            )

        return cursor.rowcount == 1

    def _initialize(self) -> None:
        self.database_path.parent.mkdir(parents=True, exist_ok=True)

        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS workflow_events (
                    sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id TEXT NOT NULL UNIQUE,
                    workflow_id TEXT NOT NULL,
                    task_id TEXT,
                    event_type TEXT NOT NULL,
                    occurred_at TEXT NOT NULL,
                    payload TEXT NOT NULL
                )
                """
            )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_workflow_events_workflow_id
                ON workflow_events (workflow_id, sequence)
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS workflow_leases (
                    workflow_id TEXT PRIMARY KEY,
                    owner_id TEXT NOT NULL,
                    expires_at TEXT NOT NULL
                )
                """
            )

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection
