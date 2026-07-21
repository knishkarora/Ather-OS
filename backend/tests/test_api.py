from uuid import UUID

from fastapi.testclient import TestClient

from ather_os.api import create_app


WORKFLOW_ID = "00000000-0000-0000-0000-000000000001"
TASK_A = "00000000-0000-0000-0000-000000000101"
TASK_B = "00000000-0000-0000-0000-000000000102"
UNKNOWN_WORKFLOW_ID = UUID("00000000-0000-0000-0000-000000009999")


def test_submit_workflow_executes_it_and_returns_completed_snapshot(tmp_path) -> None:
    client = TestClient(create_app(tmp_path / "ather-os.sqlite3"))

    response = client.post("/workflows", json=_workflow_payload())

    assert response.status_code == 201
    body = response.json()
    assert body["workflow_id"] == WORKFLOW_ID
    assert body["status"] == "completed"
    assert body["tasks"][TASK_A]["status"] == "completed"
    assert body["tasks"][TASK_B]["status"] == "completed"
    assert body["tasks"][TASK_B]["output"] == "Mock research output: Summarize findings"


def test_get_workflow_replays_persisted_snapshot_across_app_instances(tmp_path) -> None:
    database_path = tmp_path / "ather-os.sqlite3"
    first_client = TestClient(create_app(database_path))
    first_client.post("/workflows", json=_workflow_payload())
    second_client = TestClient(create_app(database_path))

    response = second_client.get(f"/workflows/{WORKFLOW_ID}")

    assert response.status_code == 200
    assert response.json()["status"] == "completed"


def test_submit_rejects_invalid_workflow_graph(tmp_path) -> None:
    client = TestClient(create_app(tmp_path / "ather-os.sqlite3"))
    payload = _workflow_payload()
    payload["tasks"].append(
        {
            "task_id": "00000000-0000-0000-0000-000000000103",
            "type": "research",
            "prompt": "Another root",
            "dependencies": [],
            "estimated_tokens": 100,
        }
    )

    response = client.post("/workflows", json=payload)

    assert response.status_code == 422
    assert "exactly one root" in response.json()["detail"]


def test_get_unknown_workflow_returns_not_found(tmp_path) -> None:
    client = TestClient(create_app(tmp_path / "ather-os.sqlite3"))

    response = client.get(f"/workflows/{UNKNOWN_WORKFLOW_ID}")

    assert response.status_code == 404


def test_submit_rejects_existing_workflow_id(tmp_path) -> None:
    client = TestClient(create_app(tmp_path / "ather-os.sqlite3"))
    client.post("/workflows", json=_workflow_payload())

    response = client.post("/workflows", json=_workflow_payload())

    assert response.status_code == 409


def _workflow_payload() -> dict:
    return {
        "workflow_id": WORKFLOW_ID,
        "goal": "Research and summarize",
        "tasks": [
            {
                "task_id": TASK_A,
                "type": "research",
                "prompt": "Find relevant facts",
                "dependencies": [],
                "estimated_tokens": 100,
            },
            {
                "task_id": TASK_B,
                "type": "research",
                "prompt": "Summarize findings",
                "dependencies": [TASK_A],
                "estimated_tokens": 100,
            },
        ],
    }
