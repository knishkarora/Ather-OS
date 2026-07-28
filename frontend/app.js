const taskDetails = {
  discover: {
    title: "Discover provider options",
    status: "✓ Completed",
    statusClass: "completed",
    attempt: "Attempt 1",
    description: "Map the available local and hosted provider choices.",
    type: "Research",
    dependencies: "None",
    timeout: "Not configured",
    output: "A focused list of provider candidates is ready for comparison.",
  },
  constraints: {
    title: "Capture constraints",
    status: "✓ Completed",
    statusClass: "completed",
    attempt: "Attempt 1",
    description: "Summarize reliability, timeout, and recovery requirements.",
    type: "Analysis",
    dependencies: "Discover provider options",
    timeout: "30 seconds",
    output: "The local execution boundary, retries, cooperative deadlines, and recovery limits are documented.",
  },
  compare: {
    title: "Compare trade-offs",
    status: "◌ Running",
    statusClass: "running",
    attempt: "Attempt 1",
    description: "Turn the findings into a short, useful decision brief.",
    type: "Synthesis",
    dependencies: "2 completed tasks",
    timeout: "60 seconds",
    output: "The provider is still working. A completed output will appear here when the task finishes.",
  },
  recommend: {
    title: "Prepare recommendation",
    status: "○ Queued",
    statusClass: "queued",
    attempt: "Waiting",
    description: "Deliver the final provider recommendation and next step.",
    type: "Recommendation",
    dependencies: "Compare trade-offs",
    timeout: "Not configured",
    output: "This task will start after the comparison task completes.",
  },
};

const title = document.querySelector("#inspector-title");
const status = document.querySelector(".inspector-status .status-pill");
const attempt = document.querySelector("#attempt-label");
const description = document.querySelector("#task-description");
const type = document.querySelector("#task-type");
const dependencies = document.querySelector("#task-dependencies");
const timeout = document.querySelector("#task-timeout");
const output = document.querySelector("#task-output");

document.querySelectorAll(".task-card").forEach((card) => {
  card.addEventListener("click", () => {
    const task = taskDetails[card.dataset.task];
    document.querySelectorAll(".task-card").forEach((item) => item.classList.remove("is-selected"));
    card.classList.add("is-selected");
    title.textContent = task.title;
    status.textContent = task.status;
    status.className = `status-pill ${task.statusClass}`;
    attempt.textContent = task.attempt;
    description.textContent = task.description;
    type.textContent = task.type;
    dependencies.textContent = task.dependencies;
    timeout.textContent = task.timeout;
    output.textContent = task.output;
  });
});
