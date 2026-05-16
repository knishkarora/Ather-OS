# Ather OS

Ather OS is a resilient, cost-aware autonomous AI execution engine.

The project will be built slowly and deliberately as a learning project. Phase 0
focuses on the local backend foundation: validating a task DAG, executing it
through a mock provider, storing append-only events, and recovering from crashes.

## Project Structure

- `backend/` - the execution engine, API, worker, state store, and recovery logic
- `frontend/` - the future user interface for submitting workflows and viewing progress
- `JOURNEY.md` - checkpoint notes about what was built, why it was built, and what was learned

## Current Build Focus

We are starting with Phase 0. The goal is to build a local backend engine before
adding real LLM providers, remote workers, or a full dashboard.
