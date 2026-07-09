from pathlib import Path

import pytest

from ather_os.dag import DagValidationError
from ather_os.dag.validate_workflow import main, validate_workflow_file


SAMPLES_DIR = Path(__file__).resolve().parents[1] / "samples"


def test_valid_sample_workflow_file_passes_validation() -> None:
    workflow = validate_workflow_file(SAMPLES_DIR / "valid_research_workflow.json")

    assert workflow.goal == "Research and summarize a local backend execution engine design."
    assert len(workflow.tasks) == 3


def test_invalid_cycle_sample_workflow_file_fails_validation() -> None:
    with pytest.raises(DagValidationError, match="dependency cycle"):
        validate_workflow_file(SAMPLES_DIR / "invalid_cycle_workflow.json")


def test_invalid_unknown_dependency_sample_workflow_file_fails_validation() -> None:
    with pytest.raises(DagValidationError, match="unknown task IDs"):
        validate_workflow_file(SAMPLES_DIR / "invalid_unknown_dependency_workflow.json")


def test_validate_workflow_command_returns_zero_for_valid_sample(capsys: pytest.CaptureFixture[str]) -> None:
    result = main([str(SAMPLES_DIR / "valid_research_workflow.json")])

    captured = capsys.readouterr()

    assert result == 0
    assert "Valid workflow:" in captured.out


def test_validate_workflow_command_returns_one_for_invalid_sample(
    capsys: pytest.CaptureFixture[str],
) -> None:
    result = main([str(SAMPLES_DIR / "invalid_cycle_workflow.json")])

    captured = capsys.readouterr()

    assert result == 1
    assert "Invalid workflow:" in captured.err
