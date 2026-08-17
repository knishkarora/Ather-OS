/**
 * Structural validator for Ather OS DAG workflows.
 * Validates graph properties matching backend DAG Validator rules.
 */

export function validateDag(tasks, goal) {
  const errors = [];
  const warnings = [];

  // 1. Goal validation
  if (!goal || !goal.trim()) {
    errors.push("Workflow goal cannot be empty.");
  }

  // 2. Task count validation
  if (!tasks || tasks.length === 0) {
    errors.push("Workflow must contain at least one task.");
    return { isValid: false, errors, warnings };
  }

  if (tasks.length > 20) {
    errors.push("Workflow cannot contain more than 20 tasks.");
  }

  const taskMap = new Map(tasks.map((t) => [t.id, t]));

  // 3. Task content & self-dependency validation
  tasks.forEach((task, idx) => {
    const taskNum = idx + 1;
    if (!task.title || !task.title.trim()) {
      errors.push(`Task ${taskNum} needs a title.`);
    }
    if (!task.prompt || !task.prompt.trim()) {
      errors.push(`Task ${taskNum} ("${task.title || "Untitled"}") needs a prompt.`);
    }
    if (task.estimated_tokens && (task.estimated_tokens < 1 || task.estimated_tokens > 8000)) {
      errors.push(`Task ${taskNum} estimated tokens must be between 1 and 8000.`);
    }
    if (task.retries < 0) {
      errors.push(`Task ${taskNum} retries cannot be negative.`);
    }
    if (task.timeout && Number(task.timeout) < 1) {
      errors.push(`Task ${taskNum} timeout must be at least 1 second.`);
    }

    // Check self-dependency
    if (task.dependencies.includes(task.id)) {
      errors.push(`Task "${task.title || `Task ${task.id}`}" cannot depend on itself.`);
    }

    // Check unknown dependencies
    task.dependencies.forEach((depId) => {
      if (!taskMap.has(depId)) {
        errors.push(`Task "${task.title || `Task ${task.id}`}" references an unknown dependency.`);
      }
    });
  });

  // 4. Root task validation (Must have exactly 1 root task with no dependencies)
  const rootTasks = tasks.filter((t) => !t.dependencies || t.dependencies.length === 0);
  if (rootTasks.length === 0) {
    errors.push("Workflow must have at least one starting task with no dependencies.");
  } else if (rootTasks.length > 1) {
    errors.push(`Workflow must have exactly one starting task (found ${rootTasks.length} starting tasks).`);
  }

  // 5. Cycle Detection using Kahn's Algorithm / In-degree BFS
  if (errors.length === 0) {
    const inDegree = new Map();
    const adj = new Map();

    tasks.forEach((t) => {
      inDegree.set(t.id, 0);
      adj.set(t.id, []);
    });

    tasks.forEach((t) => {
      t.dependencies.forEach((depId) => {
        if (adj.has(depId)) {
          adj.get(depId).push(t.id);
          inDegree.set(t.id, (inDegree.get(t.id) || 0) + 1);
        }
      });
    });

    const queue = [];
    inDegree.forEach((degree, id) => {
      if (degree === 0) queue.push(id);
    });

    let visitedCount = 0;
    while (queue.length > 0) {
      const currentId = queue.shift();
      visitedCount++;

      const neighbors = adj.get(currentId) || [];
      neighbors.forEach((neighborId) => {
        inDegree.set(neighborId, inDegree.get(neighborId) - 1);
        if (inDegree.get(neighborId) === 0) {
          queue.push(neighborId);
        }
      });
    }

    if (visitedCount < tasks.length) {
      errors.push("Dependency cycle detected! Tasks cannot depend on each other in a loop.");
    }
  }

  return {
    isValid: errors.length === 0,
    errors,
    warnings,
  };
}
