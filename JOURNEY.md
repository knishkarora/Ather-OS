# Ather OS Journey

This file records the learning journey behind Ather OS.

It is not meant to track every tiny edit. Instead, it will be updated at useful
checkpoints: when a meaningful project structure, module, feature, or design
decision is completed.

## Why This File Exists

Ather OS is being built as a learning project, not as a rushed hackathon build.
That means the reasoning matters as much as the final code.

This journey file will help capture:

- what was built at each checkpoint
- why that step came next
- which design choices were made
- what challenges or confusions came up
- how each piece connects to the larger architecture

## Current Direction

The long-term vision is an autonomous AI execution engine that can break a goal
into tasks, execute those tasks reliably, recover from failure, control cost,
and provide a clear audit trail.

The first focus is Phase 0: a local backend engine with no real LLM calls and no
remote infrastructure. Phase 0 will prove the foundation first:

- a validated workflow DAG
- event-sourced task state
- checkpoint recovery
- response caching
- mock provider execution
- an in-process worker
- a small API for running and inspecting workflows

## Checkpoint 1: Project Structure Begins

We started by creating the first project folders:

- `backend/` for the execution engine
- `frontend/` for the future interface

We also added a root `README.md` so the project has a simple entry point, and
this `JOURNEY.md` file so the learning path can be documented as the project
grows.

This is intentionally small. Before writing engine code, the project needs a
clear shape so every future file has a natural place to live.

