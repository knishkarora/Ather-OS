import sqlite3
from datetime import UTC, datetime, timedelta
from uuid import UUID

import pytest

from ather_os.state import (
    SQLiteStateStore,
    TaskCompleted,
    TaskQueued,
    WorkflowCompleted,
    WorkflowSubmitted,
)


WORKFLOW_ID = UUID("00000000-0000-0000-0000-000000000001")
OTHER_WORKFLOW_ID = UUID("00000000-0000-0000-0000-000000000002")
TASK_A = UUID("00000000-0000-0000-0000-000000000101")


def test_sqlite_state_store_returns_events_in_append_order(tmp_path) -> None:
    store = SQLiteStateStore(tmp_path / "ather-os.sqlite3")
    submitted = WorkflowSubmitted(
        workflow_id=WORKFLOW_ID,
        goal="Test workflow",
        task_ids=[TASK_A],
    )
    queued = TaskQueued(workflow_id=WORKFLOW_ID, task_id=TASK_A)
    completed = TaskCompleted(
        workflow_id=WORKFLOW_ID,
        task_id=TASK_A,
        output="Task output",
    )
    workflow_completed = WorkflowCompleted(workflow_id=WORKFLOW_ID)

    store.append_event(submitted)
    store.append_event(queued)
    store.append_event(completed)
    store.append_event(workflow_completed)

    assert store.list_events(WORKFLOW_ID) == [
        submitted,
        queued,
        completed,
        workflow_completed,
    ]


def test_sqlite_state_store_filters_by_workflow_id(tmp_path) -> None:
    store = SQLiteStateStore(tmp_path / "ather-os.sqlite3")
    expected = WorkflowSubmitted(
        workflow_id=WORKFLOW_ID,
        goal="Target workflow",
        task_ids=[TASK_A],
    )
    other = WorkflowSubmitted(
        workflow_id=OTHER_WORKFLOW_ID,
        goal="Other workflow",
        task_ids=[TASK_A],
    )

    store.append_event(expected)
    store.append_event(other)

    assert store.list_events(WORKFLOW_ID) == [expected]


def test_sqlite_state_store_persists_between_instances(tmp_path) -> None:
    database_path = tmp_path / "ather-os.sqlite3"
    event = TaskQueued(workflow_id=WORKFLOW_ID, task_id=TASK_A)

    SQLiteStateStore(database_path).append_event(event)

    assert SQLiteStateStore(database_path).list_events(WORKFLOW_ID) == [event]


def test_sqlite_state_store_rejects_duplicate_event_ids(tmp_path) -> None:
    store = SQLiteStateStore(tmp_path / "ather-os.sqlite3")
    event = TaskQueued(workflow_id=WORKFLOW_ID, task_id=TASK_A)

    store.append_event(event)

    with pytest.raises(sqlite3.IntegrityError):
        store.append_event(event)


def test_sqlite_state_store_discovers_unfinished_workflows_and_leases_them(tmp_path) -> None:
    store = SQLiteStateStore(tmp_path / "ather-os.sqlite3")
    store.append_event(
        WorkflowSubmitted(
            workflow_id=WORKFLOW_ID,
            goal="Finished workflow",
            task_ids=[TASK_A],
        )
    )
    store.append_event(WorkflowCompleted(workflow_id=WORKFLOW_ID))
    store.append_event(
        WorkflowSubmitted(
            workflow_id=OTHER_WORKFLOW_ID,
            goal="Unfinished workflow",
            task_ids=[TASK_A],
        )
    )

    now = datetime(2026, 7, 28, tzinfo=UTC)
    first_owner = UUID("00000000-0000-0000-0000-000000000010")
    second_owner = UUID("00000000-0000-0000-0000-000000000020")

    assert store.list_unfinished_workflow_ids() == [OTHER_WORKFLOW_ID]
    assert store.try_acquire_workflow_lease(
        OTHER_WORKFLOW_ID, first_owner, now + timedelta(minutes=1), now
    )
    assert not store.try_acquire_workflow_lease(
        OTHER_WORKFLOW_ID, second_owner, now + timedelta(minutes=2), now
    )
    assert store.try_acquire_workflow_lease(
        OTHER_WORKFLOW_ID,
        second_owner,
        now + timedelta(minutes=3),
        now + timedelta(minutes=1),
    )
