# AGENT.md

Behavioral guidelines for working on this project.

The objective is to make development predictable, maintainable, and AI-friendly while keeping the `/docs` directory as the project's primary knowledge base.

This is a learning project. Working code that I understand is better than perfect code that I don't.

---

# 1. Think Before Coding

**Don't assume. Don't hide uncertainty. Surface tradeoffs.**

Before implementing:

* State your assumptions explicitly.
* If multiple interpretations exist, present them instead of choosing silently.
* If a simpler solution exists, recommend it.
* If requirements are unclear, stop and ask instead of guessing.
* Explain significant tradeoffs before implementing.
* If a feature seems like it will take more than ~30 minutes of agent time to implement, pause and ask me if I want to proceed or simplify.

---

# 2. Simplicity First

**Implement the simplest solution that completely satisfies the request.**

* Do not build features that were not requested.
* Avoid premature abstraction.
* Avoid unnecessary configurability.
* Avoid speculative code.
* Do not over-engineer.

Ask yourself:

> Would a senior engineer consider this unnecessarily complicated?

If the answer is yes, simplify it.

---

# 3. Surgical Changes

**Modify only what is necessary.**

When editing existing code:

* Touch only files related to the requested task.
* Do not refactor unrelated code.
* Do not change formatting outside the affected area.
* Match the existing coding style, architecture, naming conventions, folder organization, and design patterns.
* If unrelated issues are discovered, mention them instead of fixing them unless explicitly requested.

If your changes create unused imports, variables, functions, or files, remove only those introduced by your own work.

Every modified line should directly support the requested task.

---

# 4. Goal-Driven Execution

Before making changes, define a short implementation plan.

Example:

1. Analyze existing implementation
2. Implement requested changes
3. Verify functionality
4. Update documentation

Whenever possible, verify changes through existing tests or by validating the affected functionality.

A task is only complete after both the implementation and documentation have been updated.

---

# 5. Documentation & Knowledge Base

The `/docs` directory is the project's **single source of truth** for understanding the architecture.

Treat the documentation as part of the application—not as optional notes.

Whenever code changes, determine whether the documentation is affected.

If it is, update the relevant documentation as part of the same task.

Documentation must always reflect the current implementation.

Never leave the documentation behind the codebase.

Maintain Obsidian-compatible wiki links (`[[Page Name]]`) between related documents.

Whenever new concepts are introduced:

* Update existing documentation.
* Create new documentation when necessary.
* Link the new concept into the existing knowledge graph.
* Update every affected document.

Keep these documents synchronized whenever applicable:

* Project Overview
* Architecture
* Folder Structure
* Components
* APIs
* Database
* Authentication
* State Management
* UI System
* Current Status
* Roadmap
* Tasks
* Bugs
* Decisions
* Changelog

Update the changelog whenever significant development work is completed.

Update the current status whenever features are started, completed, removed, or substantially modified.

Update docs when you learn something new about the architecture. Don't let docs fall more than 2-3 tasks behind code. For small bug fixes, a one-line note is enough.

---

# 6. Documentation-First Workflow

Before reading or modifying source code, use the documentation as your primary entry point.

When a task is assigned:

1. Read the relevant documentation inside `/docs`.
2. Follow the Obsidian wiki links (`[[Page]]`) to discover related components.
3. Build an understanding of the affected architecture through the documentation graph.
4. Only then inspect the relevant source files to verify implementation details.
5. Avoid scanning unrelated parts of the codebase unless the documentation indicates they are connected.

The documentation should guide your understanding.

The code should verify your understanding.

Do not begin implementation until both agree.

---

# 7. Follow the Knowledge Graph

Use the Obsidian knowledge graph to determine the scope of your work.

When modifying any feature:

* Identify the documentation page describing that feature.
* Follow all directly connected wiki links.
* Read only the documentation relevant to the requested change.
* Inspect only the source files represented by those connected documents unless additional dependencies are discovered.

Avoid reading the entire project when the documentation graph already defines the relevant context.

Whenever a new dependency or relationship is discovered, update the documentation so future work benefits from that knowledge.

The objective is for future AI agents to understand the project by navigating the documentation graph rather than repeatedly rediscovering the architecture from source code.

---

# 8. Preserve Project Consistency

Before introducing new code:

* Look for an existing implementation that solves a similar problem.
* Reuse existing utilities, services, components, hooks, helpers, and design patterns whenever appropriate.
* Avoid duplicate implementations.
* Extend the existing architecture instead of creating parallel solutions.

Maintain consistency in:

* Folder structure
* Naming conventions
* Component organization
* API design
* Database design
* Coding style
* Documentation structure

Consistency is preferred over personal preference.

---

# 9. Long-Term Project Memory

Treat the `/docs` directory as the long-term memory of the project.

The documentation should allow a new AI agent—or a new developer—to understand the project without reading the entire codebase.

Whenever architectural decisions are made, record them.

Whenever assumptions change, update them.

Whenever features evolve, document the evolution.

Whenever relationships between modules change, update the Obsidian links.

The knowledge graph should become increasingly accurate over time.

Every completed task should leave the project easier to understand than before.

---

## 10. Project Journey

`JOURNEY.md` is the project's development diary.

Its purpose is to document the story behind the project—not to act as a changelog or technical documentation.

The goal is to capture meaningful progress, important decisions, lessons learned, and the evolution of the project over time.

For student projects, also document: "What I learned from this" and "What I'd do differently next time." This turns JOURNEY.md into interview prep material.

### Update `JOURNEY.md` only when a meaningful milestone is reached, such as:

- A complete module is finished.
- A feature works end-to-end for the first time.
- A major architectural or design decision is made.
- A significant technical challenge is solved.
- A new technology, framework, or subsystem is successfully integrated.
- A project phase is completed.
- A milestone worth demonstrating in an interview or portfolio is achieved.

### Do **not** update `JOURNEY.md` for:

- Small bug fixes.
- Typo corrections.
- Formatting changes.
- Variable or function renames.
- Minor refactoring.
- Dependency version updates.
- Small UI adjustments.
- Routine documentation updates.
- Minor code cleanups.
- Routine maintenance tasks.
- Small configuration changes.
- Any change that does not represent meaningful project progress.

### Each new journey entry should include:

- What was accomplished.
- Why this milestone mattered.
- The biggest challenge encountered.
- The reasoning behind important decisions.
- The primary lesson learned.
- Any future improvements or ideas worth revisiting.

### Supporting Evidence

When a milestone is reached, recommend saving supporting evidence whenever appropriate, such as:

- Terminal output
- Screenshots
- UI captures
- API responses
- Architecture diagrams
- Test results
- Performance benchmarks

Store these assets inside:

`docs/journey-assets/`

Reference them from the corresponding journey entry whenever useful.

Treat `JOURNEY.md` as the human story behind the project. Every entry should be something worth reading months later, helping future developers—or future versions of yourself—understand not only what changed, but why it mattered.