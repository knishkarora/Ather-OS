from uuid import UUID

from ather_os.dag.models import Task, Workflow


class DagValidationError(ValueError):
    """Raised when a workflow is structurally invalid as a DAG."""


def validate_workflow_graph(workflow: Workflow) -> None:
    """Validate task dependency structure inside a workflow."""

    task_ids = [task.task_id for task in workflow.tasks]
    unique_task_ids = set(task_ids)

    if len(unique_task_ids) != len(task_ids):
        raise DagValidationError("Workflow contains duplicate task IDs.")

    tasks_by_id = {task.task_id: task for task in workflow.tasks}

    for task in workflow.tasks:
        dependencies = set(task.dependencies)

        if task.task_id in dependencies:
            raise DagValidationError(f"Task {task.task_id} depends on itself.")

        unknown_dependencies = dependencies - unique_task_ids
        if unknown_dependencies:
            formatted_ids = _format_uuid_list(unknown_dependencies)
            raise DagValidationError(
                f"Task {task.task_id} depends on unknown task IDs: {formatted_ids}."
            )

    _validate_acyclic(tasks_by_id)
    _validate_single_connected_root(workflow)


def _validate_acyclic(tasks_by_id: dict[UUID, Task]) -> None:
    visiting: set[UUID] = set()
    visited: set[UUID] = set()

    def visit(task_id: UUID) -> None:
        if task_id in visited:
            return

        if task_id in visiting:
            raise DagValidationError(f"Workflow contains a dependency cycle at {task_id}.")

        visiting.add(task_id)

        for dependency_id in tasks_by_id[task_id].dependencies:
            visit(dependency_id)

        visiting.remove(task_id)
        visited.add(task_id)

    for task_id in tasks_by_id:
        visit(task_id)


def _validate_single_connected_root(workflow: Workflow) -> None:
    root_ids = [task.task_id for task in workflow.tasks if not task.dependencies]

    if len(root_ids) != 1:
        formatted_ids = _format_uuid_list(root_ids)
        raise DagValidationError(
            f"Workflow must contain exactly one root task; found {len(root_ids)}: {formatted_ids}."
        )

    dependents_by_task_id = {task.task_id: set() for task in workflow.tasks}
    for task in workflow.tasks:
        for dependency_id in task.dependencies:
            dependents_by_task_id[dependency_id].add(task.task_id)

    reachable_ids = set()
    stack = [root_ids[0]]

    while stack:
        task_id = stack.pop()
        if task_id in reachable_ids:
            continue

        reachable_ids.add(task_id)
        stack.extend(dependents_by_task_id[task_id] - reachable_ids)

    all_task_ids = {task.task_id for task in workflow.tasks}
    unreachable_ids = all_task_ids - reachable_ids

    if unreachable_ids:
        formatted_ids = _format_uuid_list(unreachable_ids)
        raise DagValidationError(f"Workflow contains unreachable task IDs: {formatted_ids}.")


def _format_uuid_list(values: set[UUID] | list[UUID]) -> str:
    return ", ".join(str(value) for value in sorted(values, key=str)) or "none"
