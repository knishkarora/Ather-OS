import sqlite3
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

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection
