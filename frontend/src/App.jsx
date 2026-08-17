import { useEffect, useMemo, useRef, useState } from "react";
import { validateDag } from "./utils/dagValidation";

const apiBase = "http://127.0.0.1:8000";
const terminalStates = new Set(["completed", "failed"]);
const initialGoal = "Build an AI-driven student resume skill matcher and placement analytics pipeline.";

const initialTasks = [
  {
    id: 1,
    title: "Skill Trend Research",
    type: "research",
    prompt: "Identify top 5 in-demand technical skills for B.Tech software engineering campus placements (e.g. Python, SQL, Data Structures, Web Development, Cloud). Summarize skill weights.",
    quality: "standard",
    retries: 1,
    timeout: "20",
    estimated_tokens: 300,
    dependencies: [],
  },
  {
    id: 2,
    title: "Build Resume Matcher Script",
    type: "code_generation",
    prompt: "Write a clean Python script using standard libraries (sqlite3, json, re) to parse student skill profiles, calculate job suitability match scores (0-100%), and save top candidate records into SQLite.",
    quality: "polished",
    retries: 2,
    timeout: "30",
    estimated_tokens: 500,
    dependencies: [1],
  },
  {
    id: 3,
    title: "Analyze Matching Algorithm Trade-Offs",
    type: "analysis",
    prompt: "Analyze trade-offs between exact keyword matching vs AI semantic embedding matching for student resume screening in terms of accuracy, speed, and computational cost.",
    quality: "standard",
    retries: 1,
    timeout: "20",
    estimated_tokens: 400,
    dependencies: [2],
  },
  {
    id: 4,
    title: "Validate Pipeline & Data Audit",
    type: "validation",
    prompt: "Verify database schema integrity for candidate scores, validate edge cases (missing student skills, empty fields), and confirm overall pipeline readiness.",
    quality: "polished",
    retries: 1,
    timeout: "20",
    estimated_tokens: 300,
    dependencies: [3],
  },
  {
    id: 5,
    title: "Write Placement Summary Report",
    type: "writing",
    prompt: "Write a concise executive summary draft reporting final candidate match results and strategic recommendations for campus hiring.",
    quality: "polished",
    retries: 1,
    timeout: "20",
    estimated_tokens: 300,
    dependencies: [4],
  },
];

const taskTypes = ["research", "analysis", "writing", "validation", "code_generation"];

function responseMessage(body, fallback) {
  return typeof body?.detail === "string" ? body.detail : fallback;
}

function statusStyle(status) {
  return (
    {
      completed: {
        label: "Complete",
        card: "border-emerald-300 bg-emerald-50/90 text-emerald-950 shadow-xs",
        icon: "bg-emerald-200 text-emerald-900 font-extrabold",
        badge: "bg-emerald-200/80 text-emerald-900 font-black",
        mark: "✓",
      },
      running: {
        label: "Executing",
        card: "border-amber-300 bg-amber-100/90 text-amber-950 animate-pulse shadow-sm",
        icon: "bg-amber-300 text-amber-950 font-black",
        badge: "bg-amber-300 text-amber-950 font-black",
        mark: "↻",
      },
      queued: {
        label: "Queued",
        card: "border-indigo-200 bg-indigo-50/80 text-indigo-950",
        icon: "bg-indigo-200 text-indigo-900 font-bold",
        badge: "bg-indigo-200/80 text-indigo-900 font-bold",
        mark: "→",
      },
      pending: {
        label: "Waiting",
        card: "border-purple-200 bg-purple-50/70 text-purple-950",
        icon: "bg-purple-200 text-purple-900 font-bold",
        badge: "bg-purple-200/80 text-purple-900 font-bold",
        mark: "·",
      },
      failed: {
        label: "Failed",
        card: "border-red-300 bg-red-50 text-red-950 shadow-xs",
        icon: "bg-red-300 text-red-900 font-black",
        badge: "bg-red-200 text-red-900 font-black",
        mark: "!",
      },
    }[status] || {
      label: status,
      card: "border-indigo-200 bg-indigo-50/70 text-indigo-950",
      icon: "bg-indigo-200 text-indigo-900",
      badge: "bg-indigo-200 text-indigo-900",
      mark: "·",
    }
  );
}

function App() {
  const [goal, setGoal] = useState(initialGoal);
  const [tasks, setTasks] = useState(initialTasks);
  const [notice, setNotice] = useState(null);
  const [run, setRun] = useState(null);
  const [events, setEvents] = useState([]);
  const [runTaskLabels, setRunTaskLabels] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isRecovering, setIsRecovering] = useState(false);
  const [activeSection, setActiveSection] = useState("workspace");
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const pollRef = useRef(null);

  const rootCount = useMemo(() => tasks.filter((task) => task.dependencies.length === 0).length, [tasks]);
  const completedCount = run ? Object.values(run.tasks).filter((task) => task.status === "completed").length : 0;
  const failedCount = run ? Object.values(run.tasks).filter((task) => task.status === "failed").length : 0;
  const runTasks = run ? Object.values(run.tasks) : [];
  const progress = runTasks.length ? Math.round(((completedCount + failedCount) / runTasks.length) * 100) : 0;

  useEffect(() => () => window.clearInterval(pollRef.current), []);

  function updateTask(id, field, value) {
    setTasks((current) => current.map((task) => (task.id === id ? { ...task, [field]: value } : task)));
  }

  function toggleDependency(taskId, dependencyId) {
    setTasks((current) =>
      current.map((task) => {
        if (task.id !== taskId) return task;
        const exists = task.dependencies.includes(dependencyId);
        return {
          ...task,
          dependencies: exists ? task.dependencies.filter((id) => id !== dependencyId) : [...task.dependencies, dependencyId],
        };
      })
    );
  }

  function addTask() {
    const id = Math.max(...tasks.map((task) => task.id), 0) + 1;
    const previous = tasks.at(-1);
    setTasks((current) => [
      ...current,
      {
        id,
        title: "Untitled task",
        type: "analysis",
        prompt: "Describe the work this task should perform.",
        quality: "standard",
        retries: 0,
        timeout: "",
        estimated_tokens: 300,
        dependencies: previous ? [previous.id] : [],
      },
    ]);
    setNotice({ tone: "success", text: "Task added. Customise its title, type, and prompt below." });
  }

  function removeTask(id) {
    if (tasks.length <= 1) return;
    setTasks((current) =>
      current
        .filter((task) => task.id !== id)
        .map((task) => ({ ...task, dependencies: task.dependencies.filter((depId) => depId !== id) }))
    );
  }

  function validationErrors() {
    const res = validateDag(tasks, goal);
    return res.errors;
  }

  function reviewWorkflow() {
    const errors = validationErrors();
    if (errors.length > 0) {
      setNotice({ tone: "error", text: errors.join(" ") });
      return false;
    }
    setNotice({ tone: "success", text: "Workflow structure is valid and ready for execution." });
    return true;
  }

  function payload() {
    const workflowId = crypto.randomUUID();
    const idMap = new Map(tasks.map((task) => [task.id, crypto.randomUUID()]));
    return {
      workflow_id: workflowId,
      goal: goal.trim(),
      tasks: tasks.map((task) => ({
        task_id: idMap.get(task.id),
        type: task.type,
        prompt: task.prompt.trim(),
        dependencies: task.dependencies.map((dependency) => idMap.get(dependency)),
        estimated_tokens: Number(task.estimated_tokens) || 300,
        quality_tier: task.quality,
        max_retries: Math.max(0, Number(task.retries) || 0),
        timeout_seconds: task.timeout ? Math.max(1, Number(task.timeout)) : null,
      })),
    };
  }

  async function getJson(path, options) {
    const response = await fetch(`${apiBase}${path}`, options);
    const body = await response.json();
    if (!response.ok) throw new Error(responseMessage(body, "The local engine could not process this request."));
    return body;
  }

  async function refreshRun(workflowId) {
    const [snapshot, trace] = await Promise.all([getJson(`/workflows/${workflowId}`), getJson(`/workflows/${workflowId}/events`)]);
    setRun(snapshot);
    setEvents(trace);
    if (terminalStates.has(snapshot.status)) window.clearInterval(pollRef.current);
    return snapshot;
  }

  function startPolling(workflowId) {
    window.clearInterval(pollRef.current);
    pollRef.current = window.setInterval(() => refreshRun(workflowId).catch((error) => setNotice({ tone: "error", text: error.message })), 700);
  }

  async function submitWorkflow() {
    if (!reviewWorkflow()) return;
    const workflow = payload();
    setIsSubmitting(true);

    const labels = {};
    workflow.tasks.forEach((wfTask, index) => {
      labels[wfTask.task_id] = { ...tasks[index], index: index + 1 };
    });
    setRunTaskLabels(labels);

    try {
      const snapshot = await getJson("/workflows", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(workflow),
      });
      setRun(snapshot);
      setEvents([]);
      document.querySelector("#run-status")?.scrollIntoView({ behavior: "smooth", block: "start" });
      setActiveSection("run-status");
      await refreshRun(workflow.workflow_id);
      startPolling(workflow.workflow_id);
    } catch (error) {
      setRun({
        workflow_id: workflow.workflow_id,
        goal: workflow.goal,
        status: "failed",
        tasks: {},
        error: `${error.message} Ensure local backend is running (uvicorn ather_os.api.app:app --reload).`,
      });
      setEvents([]);
    } finally {
      setIsSubmitting(false);
    }
  }

  async function recoverWorkflow() {
    if (!run || !window.confirm("Recover this unfinished workflow? Interrupted tasks will execute with incremented attempt numbers.")) return;
    setIsRecovering(true);
    try {
      const snapshot = await getJson(`/workflows/${run.workflow_id}/recover`, { method: "POST" });
      setRun(snapshot);
      await refreshRun(run.workflow_id);
      startPolling(run.workflow_id);
      setNotice({ tone: "success", text: "Recovery initiated. The execution view is updating." });
    } catch (error) {
      setNotice({ tone: "error", text: error.message });
    } finally {
      setIsRecovering(false);
    }
  }

  return (
    <main className="min-h-screen bg-canvas text-ink font-sans">
      <header className="sticky top-0 z-30 border-b border-white/10 bg-ink px-5 text-white shadow-md md:px-10">
        <div className="mx-auto flex h-18 max-w-360 items-center justify-between gap-4">
          <div className="flex items-center gap-6">
            <a
              className="flex shrink-0 items-center gap-2.5 text-xl font-extrabold tracking-tight"
              href="#workspace"
              onClick={() => setActiveSection("workspace")}
            >
              <span className="grid size-8 place-items-center rounded-xl bg-mint text-xs font-black text-ink">A</span>
              Ather<span className="text-mint">OS</span>
            </a>
            <nav className="hidden h-full items-center gap-1 sm:flex">
              <a
                className={`nav-link ${activeSection === "workspace" ? "aria-current-page" : ""}`}
                href="#workspace"
                onClick={() => setActiveSection("workspace")}
              >
                Workspace
              </a>
              <a
                className={`nav-link ${activeSection === "builder" ? "aria-current-page" : ""}`}
                href="#builder"
                onClick={() => setActiveSection("builder")}
              >
                Builder
              </a>
              <a
                className={`nav-link ${activeSection === "run-status" ? "aria-current-page" : ""}`}
                href="#run-status"
                onClick={() => setActiveSection("run-status")}
              >
                Activity & Results
              </a>
            </nav>
          </div>

          <div className="flex items-center gap-3">
            <span className="hidden rounded-full border border-white/15 bg-white/10 px-3 py-1.5 text-xs font-semibold text-white/80 md:block">
              Local Engine v0.1.0
            </span>
            <button
              onClick={submitWorkflow}
              disabled={isSubmitting}
              className="rounded-xl bg-mint px-4 py-2.5 text-xs font-extrabold text-ink transition hover:bg-mint/90 disabled:opacity-60"
            >
              {isSubmitting ? "Starting…" : "Run Workflow"}
            </button>
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="grid size-9 place-items-center rounded-lg border border-white/20 text-white sm:hidden"
              aria-label="Toggle menu"
            >
              {mobileMenuOpen ? "✕" : "☰"}
            </button>
          </div>
        </div>

        {mobileMenuOpen && (
          <nav className="flex flex-col gap-2 border-t border-white/10 py-3 sm:hidden">
            <a
              className="px-3 py-2 text-sm font-semibold text-white hover:bg-white/10 rounded-lg"
              href="#workspace"
              onClick={() => {
                setActiveSection("workspace");
                setMobileMenuOpen(false);
              }}
            >
              Workspace
            </a>
            <a
              className="px-3 py-2 text-sm font-semibold text-white hover:bg-white/10 rounded-lg"
              href="#builder"
              onClick={() => {
                setActiveSection("builder");
                setMobileMenuOpen(false);
              }}
            >
              Builder
            </a>
            <a
              className="px-3 py-2 text-sm font-semibold text-white hover:bg-white/10 rounded-lg"
              href="#run-status"
              onClick={() => {
                setActiveSection("run-status");
                setMobileMenuOpen(false);
              }}
            >
              Activity & Results
            </a>
          </nav>
        )}
      </header>

      <section className="mx-auto max-w-360 px-5 py-8 md:px-10 md:py-10" id="workspace">
        <div className="rounded-[2rem] bg-ink px-6 py-8 text-white shadow-xl md:px-9 md:py-9">
          <div className="flex flex-col justify-between gap-6 lg:flex-row lg:items-end">
            <div>
              <p className="text-xs font-extrabold tracking-widest text-mint uppercase">Autonomous AI Workflow Substrate</p>
              <h1 className="mt-2 max-w-2xl text-3xl font-black tracking-tight md:text-5xl">Build & Observe Resilient Workflows</h1>
              <p className="mt-3 max-w-xl text-sm leading-relaxed text-white/70">
                Decompose goals into DAG tasks, execute through local/hosted providers, and monitor state through append-only event traces.
              </p>
            </div>
            <a
              className="w-fit rounded-xl bg-white px-4 py-3 text-xs font-extrabold text-ink transition hover:bg-white/90"
              href="#builder"
              onClick={() => setActiveSection("builder")}
            >
              Edit Workflow Draft ↓
            </a>
          </div>
          <div className="mt-8 grid gap-3 sm:grid-cols-3">
            <Summary label="Current Goal" value={goal || "Untitled workflow"} detail={`${tasks.length} connected ${tasks.length === 1 ? "task" : "tasks"}`} />
            <Summary
              label="Graph Structure"
              value={rootCount === 1 ? "Single Starting Root" : `${rootCount} Root Nodes`}
              detail={rootCount === 1 ? "Valid DAG Graph" : "Requires exactly 1 root task"}
            />
            <Summary label="Execution Engine" value="SQLite + In-Memory Queue" detail="Append-only event sourcing" accent />
          </div>
        </div>

        <div className="mt-10" id="builder">
          <div className="mb-6 flex flex-col justify-between gap-4 lg:flex-row lg:items-end">
            <div>
              <p className="mb-1 text-xs font-extrabold tracking-wider text-ink/60 uppercase">Workflow Builder · Stage 5</p>
              <h2 className="max-w-2xl text-2xl font-black tracking-tight md:text-4xl">Compose Workflow Graph</h2>
              <p className="mt-1 text-sm text-ink/60">Define task inputs, prompt instructions, dependencies, quality constraints, and timeouts.</p>
            </div>
            <button onClick={reviewWorkflow} className="rounded-xl bg-ink px-4 py-2.5 text-xs font-bold text-white transition hover:bg-ink/90">
              Validate Workflow Graph
            </button>
          </div>

          {notice && (
            <div
              className={`mb-6 rounded-2xl border px-4 py-3 text-sm font-semibold shadow-xs ${
                notice.tone === "error" ? "border-red-300 bg-red-50 text-red-900" : "border-mint-strong/30 bg-mint/50 text-mint-strong"
              }`}
              role="alert"
            >
              {notice.text}
            </div>
          )}

          <div className="grid gap-6 xl:grid-cols-[minmax(0,1fr)_380px]">
            <section className="rounded-3xl border border-line bg-white p-5 shadow-sm md:p-7">
              <div className="mb-7 border-b border-line pb-6">
                <p className="text-[10px] font-extrabold tracking-wider text-ink/50 uppercase">01 · Intent</p>
                <h3 className="mt-1 text-lg font-extrabold">Workflow Goal</h3>
                <label className="mt-4 block text-xs font-bold text-ink/70">
                  Target Outcome
                  <textarea
                    value={goal}
                    onChange={(event) => setGoal(event.target.value)}
                    rows="2"
                    className="mt-2 w-full resize-y rounded-2xl border border-line bg-canvas px-4 py-3 text-sm leading-relaxed"
                  />
                </label>
              </div>

              <div className="mb-4 flex items-center justify-between gap-4">
                <div>
                  <p className="text-[10px] font-extrabold tracking-wider text-ink/50 uppercase">02 · Task DAG Nodes</p>
                  <h3 className="mt-1 text-lg font-extrabold">Tasks ({tasks.length})</h3>
                </div>
                <button
                  onClick={addTask}
                  disabled={tasks.length >= 20}
                  className="rounded-xl border border-ink/20 px-3.5 py-2 text-xs font-extrabold text-ink transition hover:bg-canvas disabled:opacity-40"
                >
                  + Add Task
                </button>
              </div>

              <div className="space-y-4">
                {tasks.map((task, index) => (
                  <TaskEditor
                    key={task.id}
                    task={task}
                    index={index}
                    tasks={tasks}
                    onChange={updateTask}
                    onToggleDependency={toggleDependency}
                    onRemove={removeTask}
                  />
                ))}
              </div>
            </section>

            <Preview goal={goal} tasks={tasks} />
          </div>

          <Execution
            run={run}
            events={events}
            taskLabels={runTaskLabels}
            progress={progress}
            completed={completedCount}
            failed={failedCount}
            recovering={isRecovering}
            onRecover={recoverWorkflow}
          />
        </div>
      </section>
    </main>
  );
}

function Summary({ label, value, detail, accent }) {
  return (
    <div className={`rounded-2xl border p-4 ${accent ? "border-mint/30 bg-mint/15" : "border-white/10 bg-white/5"}`}>
      <p className={`text-[10px] font-extrabold tracking-wider uppercase ${accent ? "text-mint" : "text-white/60"}`}>{label}</p>
      <p className="mt-2 truncate text-sm font-extrabold">{value}</p>
      <p className="mt-1 text-xs text-white/60">{detail}</p>
    </div>
  );
}

function TaskEditor({ task, index, tasks, onChange, onToggleDependency, onRemove }) {
  return (
    <article className="rounded-2xl border border-line bg-canvas p-4 md:p-5">
      <div className="mb-3 flex items-center justify-between">
        <span className="text-xs font-extrabold text-ink/60 uppercase">Task {index + 1}</span>
        <button
          disabled={tasks.length <= 1}
          onClick={() => onRemove(task.id)}
          className="text-xs font-bold text-red-600 transition hover:underline disabled:opacity-30 disabled:no-underline"
        >
          Remove Task
        </button>
      </div>

      <div className="grid gap-3 md:grid-cols-[1fr_170px]">
        <Field label="Task Title">
          <input value={task.title} onChange={(event) => onChange(task.id, "title", event.target.value)} className="field" placeholder="Task title" />
        </Field>
        <Field label="Type">
          <select value={task.type} onChange={(event) => onChange(task.id, "type", event.target.value)} className="field">
            {taskTypes.map((type) => (
              <option key={type} value={type}>
                {type.replaceAll("_", " ")}
              </option>
            ))}
          </select>
        </Field>
      </div>

      <Field label="Prompt Instruction" extra="mt-3">
        <textarea
          value={task.prompt}
          onChange={(event) => onChange(task.id, "prompt", event.target.value)}
          rows="2"
          className="field resize-y"
          placeholder="Specific instruction prompt for this task"
        />
      </Field>

      <div className="mt-3 grid gap-3 sm:grid-cols-4">
        <Field label="Quality Tier">
          <select value={task.quality} onChange={(event) => onChange(task.id, "quality", event.target.value)} className="field">
            <option value="draft">draft</option>
            <option value="standard">standard</option>
            <option value="polished">polished</option>
          </select>
        </Field>
        <Field label="Max Retries">
          <input
            type="number"
            min="0"
            max="10"
            value={task.retries}
            onChange={(event) => onChange(task.id, "retries", event.target.value)}
            className="field"
          />
        </Field>
        <Field label="Timeout (sec)">
          <input
            type="number"
            min="1"
            value={task.timeout}
            onChange={(event) => onChange(task.id, "timeout", event.target.value)}
            className="field"
            placeholder="Optional"
          />
        </Field>
        <Field label="Est. Tokens">
          <input
            type="number"
            min="1"
            max="8000"
            value={task.estimated_tokens || 300}
            onChange={(event) => onChange(task.id, "estimated_tokens", event.target.value)}
            className="field"
          />
        </Field>
      </div>

      <fieldset className="mt-4">
        <legend className="text-xs font-bold text-ink/70">Depends On Tasks (DAG Parents)</legend>
        <div className="mt-2 flex flex-wrap gap-2">
          {tasks
            .filter((option) => option.id !== task.id)
            .map((option) => (
              <label key={option.id} className="inline-flex items-center gap-2 rounded-full border border-line bg-white px-3 py-1.5 text-xs font-semibold text-ink cursor-pointer hover:bg-canvas">
                <input
                  type="checkbox"
                  checked={task.dependencies.includes(option.id)}
                  onChange={() => onToggleDependency(task.id, option.id)}
                  className="size-3.5 accent-ink"
                />
                {option.title || `Task ${option.id}`}
              </label>
            ))}
          {tasks.length <= 1 && <span className="text-xs text-ink/40">No other tasks available for dependency.</span>}
        </div>
      </fieldset>
    </article>
  );
}

function Field({ label, children, extra = "" }) {
  return (
    <label className={`block text-xs font-bold text-ink/70 ${extra}`}>
      {label}
      {children}
    </label>
  );
}

function Preview({ goal, tasks }) {
  return (
    <aside className="h-fit rounded-3xl border border-line bg-white p-5 shadow-xs md:p-6">
      <div className="flex items-center justify-between border-b border-line pb-4">
        <div>
          <p className="text-[10px] font-extrabold tracking-wider text-ink/50 uppercase">DAG Topology</p>
          <h3 className="mt-0.5 text-lg font-extrabold">Workflow Structure</h3>
        </div>
        <span className="rounded-full bg-cyan px-3 py-1 text-xs font-extrabold text-ink">{tasks.length} Nodes</span>
      </div>

      <div className="mt-4">
        <p className="text-xs font-bold text-ink/50 uppercase">Goal</p>
        <p className="mt-1 rounded-xl border border-line bg-canvas p-3 text-xs leading-relaxed text-ink/80">{goal.trim() || "Add a goal description."}</p>
      </div>

      <div className="mt-4 space-y-3">
        <p className="text-xs font-bold text-ink/50 uppercase">Tasks Flow</p>
        {tasks.map((task, index) => (
          <div key={task.id} className="rounded-xl border border-line bg-canvas p-3 text-xs">
            <div className="flex items-center gap-2.5">
              <span className={`grid size-6 place-items-center rounded-md text-xs font-black ${index === 0 ? "bg-mint text-mint-strong" : "bg-lilac text-ink"}`}>
                {index + 1}
              </span>
              <div className="min-w-0 flex-1">
                <p className="truncate font-bold text-ink">{task.title || `Task ${task.id}`}</p>
                <p className="mt-0.5 text-[11px] text-ink/55">
                  {task.dependencies.length > 0
                    ? `Depends on ${task.dependencies.map((d) => `Task ${d}`).join(", ")}`
                    : "Root starting node"}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </aside>
  );
}

function Execution({ run, events, taskLabels, progress, completed, failed, recovering, onRecover }) {
  const pending = run?.status === "pending";
  const [copiedId, setCopiedId] = useState(null);

  const completedTasks = run
    ? Object.values(run.tasks).filter((task) => task.output || task.error)
    : [];

  function copyToClipboard(text, taskId) {
    navigator.clipboard.writeText(text);
    setCopiedId(taskId);
    setTimeout(() => setCopiedId(null), 2000);
  }

  return (
    <section id="run-status" className="mt-8 overflow-hidden rounded-3xl border border-line bg-white shadow-sm" aria-live="polite">
      <div className="border-b border-line bg-ink px-5 py-6 text-white md:px-7">
        <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-start">
          <div>
            <p className="text-xs font-extrabold tracking-wider text-mint uppercase">Execution Engine Telemetry</p>
            <h2 className="mt-1 text-xl font-extrabold md:text-2xl">{run?.goal || "No active execution"}</h2>
            <p className="mt-2 max-w-xl text-xs leading-relaxed text-white/70">
              {run?.error || (run ? "Local engine is executing tasks based on dependency readiness." : "Run a workflow to monitor live task status and event replay traces.")}
            </p>
          </div>
          <div className="flex items-center gap-2">
            <span className="rounded-full bg-cyan px-3.5 py-1.5 text-xs font-extrabold text-ink uppercase tracking-wide">
              {run?.status || "Ready"}
            </span>
            {pending && (
              <button
                onClick={onRecover}
                disabled={recovering}
                className="rounded-xl border border-mint/40 bg-mint/10 px-3.5 py-1.5 text-xs font-extrabold text-mint transition hover:bg-mint/20 disabled:opacity-50"
              >
                {recovering ? "Recovering…" : "Recover Execution"}
              </button>
            )}
          </div>
        </div>

        <div className="mt-6 flex items-center gap-3">
          <div className="h-2.5 flex-1 overflow-hidden rounded-full bg-white/15">
            <div style={{ width: `${progress}%` }} className="h-full rounded-full bg-mint transition-all duration-500" />
          </div>
          <span className="text-xs font-bold text-white/80">
            {completed} of {run ? Object.keys(run.tasks).length : 0} Completed ({progress}%)
          </span>
        </div>
      </div>

      <div className="grid gap-6 p-5 lg:grid-cols-[minmax(0,1fr)_320px] md:p-7">
        <div>
          <div className="flex items-center justify-between border-b border-line pb-3">
            <div>
              <p className="text-[10px] font-extrabold tracking-wider text-ink/50 uppercase">Task Snapshot Map</p>
              <h3 className="mt-0.5 text-sm font-bold text-ink">Engine Task States</h3>
            </div>
            <span className="rounded-full bg-canvas px-3 py-1 text-xs font-extrabold text-ink/70">
              {failed > 0 ? `${failed} Failed` : `${completed}/${run ? Object.keys(run.tasks).length : 0} Done`}
            </span>
          </div>

          <div className="mt-4 grid gap-3 md:grid-cols-2">
            {run &&
              Object.values(run.tasks).map((task, index) => {
                const style = statusStyle(task.status);
                const draft = taskLabels[task.task_id];
                return (
                  <article key={task.task_id} className={`rounded-2xl border p-4 transition-all ${style.card}`}>
                    <div className="flex justify-between gap-3">
                      <div className="flex items-center gap-3">
                        <span className={`grid size-8 place-items-center rounded-xl text-sm font-extrabold ${style.icon}`}>{style.mark}</span>
                        <div>
                          <p className="text-xs font-extrabold">{draft?.title || `Task ${index + 1}`}</p>
                          <p className="mt-0.5 text-[11px] opacity-75">
                            Attempt {task.attempt || 0}
                            {draft?.type ? ` · ${draft.type}` : ""}
                          </p>
                        </div>
                      </div>
                      <span className={`rounded-full px-2.5 py-1 text-[11px] h-fit ${style.badge}`}>{style.label}</span>
                    </div>
                    <div className="mt-3 border-t border-current/10 pt-2.5">
                      {task.output && (
                        <p className="text-xs leading-relaxed font-sans bg-white/80 p-2.5 rounded-lg border border-black/10 line-clamp-3">
                          {task.output}
                        </p>
                      )}
                      {task.error && <p className="text-xs leading-relaxed text-red-900 font-semibold bg-red-100/90 p-2.5 rounded-lg">{task.error}</p>}
                      {!task.output && !task.error && <p className="text-xs opacity-60 italic">Waiting for dependencies or execution...</p>}
                    </div>
                  </article>
                );
              })}
            {!run && <p className="text-xs text-ink/50 italic col-span-2 py-4">No active workflow execution to display.</p>}
          </div>

          {pending && (
            <p className="mt-4 rounded-xl border border-cream bg-cream/50 p-3 text-xs leading-relaxed text-ink/80">
              💡 <strong>At-Least-Once Recovery:</strong> If local execution was interrupted, clicking &quot;Recover Execution&quot; will rebuild the queue state from SQLite events and resume pending tasks.
            </p>
          )}
        </div>

        <aside className="rounded-2xl border border-line bg-canvas p-4">
          <div className="flex items-center justify-between border-b border-line pb-3">
            <div>
              <p className="text-[10px] font-extrabold tracking-wider text-ink/50 uppercase">Append-Only Log</p>
              <h3 className="mt-0.5 text-sm font-extrabold">Event Trace ({events.length})</h3>
            </div>
          </div>

          {events.length ? (
            <ol className="mt-3 space-y-2 max-h-96 overflow-y-auto pr-1">
              {events.slice(-8).map((event, index) => (
                <li key={`${event.event_id || event.event_type}-${index}`} className="rounded-xl border border-line bg-white px-3 py-2 text-xs shadow-2xs">
                  <div className="flex items-center justify-between gap-2">
                    <span className="font-extrabold capitalize text-ink/80">{event.event_type.replaceAll("_", " ")}</span>
                    <span className="rounded bg-canvas px-1.5 py-0.5 text-[10px] text-ink/50">{event.task_id ? "task" : "workflow"}</span>
                  </div>
                  {event.attempt && <p className="mt-1 text-[11px] text-ink/60">Attempt {event.attempt}</p>}
                </li>
              ))}
            </ol>
          ) : (
            <p className="mt-3 rounded-xl border border-dashed border-line bg-white p-4 text-xs leading-relaxed text-ink/50">
              Lifecycle events will stream here automatically upon submission.
            </p>
          )}
        </aside>
      </div>

      {/* 🚀 WORKFLOW DELIVERABLES & RESULTS INSPECTOR VIEW */}
      {completedTasks.length > 0 && (
        <div className="border-t border-line bg-canvas/40 p-5 md:p-7">
          <div className="mb-6 flex flex-col justify-between gap-3 sm:flex-row sm:items-center">
            <div>
              <p className="text-xs font-black tracking-widest text-mint-strong uppercase">Final Deliverables & Phase Output Results</p>
              <h3 className="mt-0.5 text-xl font-black text-ink">Generated Model Results ({completedTasks.length})</h3>
            </div>
            <button
              onClick={() => {
                const fullText = completedTasks
                  .map((t, idx) => {
                    const label = taskLabels[t.task_id]?.title || `Phase ${idx + 1}`;
                    return `=== ${label} (${taskLabels[t.task_id]?.type || "Task"}) ===\n${t.output || t.error || ""}`;
                  })
                  .join("\n\n");
                copyToClipboard(fullText, "all");
              }}
              className="rounded-xl bg-ink px-4 py-2 text-xs font-extrabold text-white transition hover:bg-ink/80 shadow-xs"
            >
              {copiedId === "all" ? "✓ All Copied!" : "📋 Copy All Workflow Deliverables"}
            </button>
          </div>

          <div className="space-y-5">
            {completedTasks.map((task, index) => {
              const draft = taskLabels[task.task_id];
              const isCode = draft?.type === "code_generation" || task.output?.includes("def ") || task.output?.includes("import ");
              return (
                <article key={task.task_id} className="rounded-2xl border border-line bg-white p-5 shadow-sm">
                  <div className="flex flex-wrap items-center justify-between gap-3 border-b border-line pb-3">
                    <div className="flex items-center gap-3">
                      <span className="grid size-7 place-items-center rounded-lg bg-ink text-xs font-black text-white">
                        {index + 1}
                      </span>
                      <div>
                        <h4 className="text-sm font-extrabold text-ink">{draft?.title || `Phase ${index + 1}`}</h4>
                        <p className="text-xs text-ink/60">
                          Type: <span className="font-bold uppercase tracking-wider text-ink/80">{draft?.type || "Task"}</span> · Quality:{" "}
                          <span className="font-semibold">{draft?.quality || "standard"}</span>
                        </p>
                      </div>
                    </div>

                    <div className="flex items-center gap-2">
                      <span className="rounded-full bg-emerald-100 px-3 py-1 text-xs font-extrabold text-emerald-900 border border-emerald-300">
                        Completed
                      </span>
                      {task.output && (
                        <button
                          onClick={() => copyToClipboard(task.output, task.task_id)}
                          className="rounded-lg border border-line bg-canvas px-3 py-1 text-xs font-bold text-ink/80 transition hover:bg-line"
                        >
                          {copiedId === task.task_id ? "✓ Copied!" : "Copy Result"}
                        </button>
                      )}
                    </div>
                  </div>

                  {draft?.prompt && (
                    <div className="mt-3 rounded-xl bg-canvas/70 p-3 text-xs border border-line/60">
                      <span className="font-extrabold text-ink/50 uppercase tracking-wider block mb-1 text-[10px]">Prompt Instruction</span>
                      <p className="text-ink/80 leading-relaxed italic">{draft.prompt}</p>
                    </div>
                  )}

                  <div className="mt-4">
                    <span className="font-extrabold text-ink/50 uppercase tracking-wider block mb-1.5 text-[10px]">Generated Output Deliverable</span>
                    {task.output ? (
                      isCode ? (
                        <pre className="w-full text-left font-mono text-xs leading-relaxed overflow-x-auto whitespace-pre p-4.5 rounded-xl bg-[#111216] text-mint border border-white/10 shadow-inner block my-2">
                          <code>{task.output}</code>
                        </pre>
                      ) : (
                        <div className="w-full text-left font-sans text-sm leading-relaxed text-ink/90 whitespace-pre-line p-4 rounded-xl border border-line bg-canvas/50 my-2">
                          {task.output}
                        </div>
                      )
                    ) : (
                      <p className="text-xs text-red-800 bg-red-50 p-3 rounded-xl font-semibold">{task.error || "No response generated."}</p>
                    )}
                  </div>
                </article>
              );
            })}
          </div>
        </div>
      )}
    </section>
  );
}

export default App;
