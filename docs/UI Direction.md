# UI Direction

[[README|Knowledge Base Home]] > [[08_UI_System|UI System]] > UI Direction

This is Ather OS's visual north star for the frontend. It captures inspiration,
not a final screen specification. The user will supply the actual UI design
before implementation begins.

## Reference Images

These user-provided references are retained locally for future frontend slices:

![[ui-assets/inspiration/01-learning-dashboard.png]]

![[ui-assets/inspiration/02-workspace-dashboard.png]]

![[ui-assets/inspiration/03-task-summary-card.png]]

![[ui-assets/inspiration/04-task-detail-card.png]]

They are visual references only. Do not copy their names, text, avatars,
calendar behavior, or learning/productivity features into Ather OS.

## The Intended Feel

Ather OS should feel like a friendly, tactile developer workspace for observing
AI workflows: calm enough to scan, expressive enough to make execution state
obvious, and structured enough for serious debugging.

The strongest shared characteristics to carry forward are:

- An intentional app frame: a dark or near-black navigation shell surrounding
  a light workspace, rather than a flat generic dashboard.
- A warm off-white main canvas with generous rounded corners and controlled
  depth through soft shadows or subtle borders.
- Compact, information-rich task cards with a clear title, status, progress,
  and an obvious next action.
- Soft pastel accent colors used as semantic state signals, balanced by black,
  white, and muted gray neutrals.
- Large, readable headings and compact supporting text; visual hierarchy must
  make workflow state legible before a user reads every detail.
- Dependency lines, progress bars, pills, and small icon controls that make an
  execution system feel alive without making it visually noisy.

## Ather-Specific Translation

The reference products manage courses, calendars, and teams. Ather OS manages
workflow DAGs and task execution. Keep the visual grammar, but map it only to
real Ather concepts:

| Reference pattern | Ather OS use |
| --- | --- |
| Central board of cards | Workflow graph or execution board |
| Connected cards | Task dependencies |
| Completion bar / count | Completed tasks out of total tasks |
| Colored cards | Queued, running, completed, failed, retrying, or timed-out task state |
| Right-side activity column | Workflow summary, event trace, or task inspector |
| Compact task card | Task ID/name, prompt summary, attempt, status, and output/error preview |
| Overflow control | Task details, inspect events, or recovery action |

The UI must never imply features the backend does not provide. In particular,
do not add teams, people, calendars, meetings, notifications, billing, or
provider choices to the initial frontend.

## State Color Principle

Use color to reinforce state, never as the only state indicator. Every task
state needs a text label and an icon or shape cue as well.

- Queued: quiet neutral or cool tint.
- Running: energetic but controlled accent.
- Completed: mint/green success tint.
- Retryable failure or timeout: warm amber/orange warning tint.
- Terminal failure: coral/red error tint.

The exact palette, typeface, spacing scale, icon set, and responsive rules are
design decisions to be provided with the final UI design.

## Implementation Guardrails

- Do not begin frontend implementation from these references alone.
- Preserve this visual direction across the workflow list, workflow builder,
  execution board, task inspector, and event trace.
- Prefer native CSS and existing browser features; do not introduce a UI
  component library unless the chosen final design truly needs one.
- Build the frontend in stages once the design is available, starting with the
  application shell and one workflow view rather than every screen at once.

## Related

- [[08_UI_System|UI System]]
- [[04_APIs|APIs]]
- [[05_Components|Components]]
- [[Frontend]]
