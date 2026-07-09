"""Command helpers for validating workflow JSON files."""

from argparse import ArgumentParser
from pathlib import Path
import sys
from typing import Sequence

from pydantic import ValidationError

from ather_os.dag.models import Workflow
from ather_os.dag.validators import DagValidationError, validate_workflow_graph


def load_workflow_file(path: Path) -> Workflow:
    """Load a workflow JSON file into the DAG model."""

    return Workflow.model_validate_json(path.read_text(encoding="utf-8"))


def validate_workflow_file(path: Path) -> Workflow:
    """Load and structurally validate a workflow JSON file."""

    workflow = load_workflow_file(path)
    validate_workflow_graph(workflow)
    return workflow


def main(argv: Sequence[str] | None = None) -> int:
    parser = ArgumentParser(description="Validate an Ather OS workflow JSON file.")
    parser.add_argument("path", type=Path, help="Path to a workflow JSON file.")
    args = parser.parse_args(argv)

    try:
        workflow = validate_workflow_file(args.path)
    except (OSError, ValidationError, DagValidationError) as exc:
        print(f"Invalid workflow: {exc}", file=sys.stderr)
        return 1

    print(f"Valid workflow: {workflow.workflow_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
