# Folder Structure

[[README|Knowledge Base Home]] > Folder Structure

This document records the audited folder structure and responsibilities.

## Root

```text
.
├── .gitignore
├── AtherOS_Project_Master_Document.txt
├── JOURNEY.md
├── README.md
├── backend/
├── docs/
└── frontend/
```

## Root Files

- `README.md`: project introduction, current Phase 0 focus, and top-level structure.
- `JOURNEY.md`: human learning log and checkpoint notes.
- `AtherOS_Project_Master_Document.txt`: product vision, architectural principles, staged roadmap, and explanatory messaging.
- `.gitignore`: excludes Python caches, virtual environments, local databases, env files, frontend build artifacts, and editor files.

## Backend

```text
backend/
├── README.md
├── pyproject.toml
├── samples/
├── src/
│   ├── ather_os/
│   │   ├── __init__.py
│   │   ├── api/
│   │   ├── cache/
│   │   ├── checkpoint/
│   │   ├── config/
│   │   ├── dag/
│   │   │   ├── __init__.py
│   │   │   └── models.py
│   │   ├── providers/
│   │   ├── queue/
│   │   ├── state/
│   │   └── worker/
│   └── ather_os_backend.egg-info/
└── tests/
```

`backend/pyproject.toml` defines a Python 3.11+ package named `ather-os-backend` using setuptools package discovery from `src`.

`backend/src/ather_os/dag/models.py` is the implemented domain model file. See [[05_Components|Components]] and [[06_State_Management|State Management]] for relationships.

`backend/src/ather_os_backend.egg-info/` appears to be generated package metadata from an editable install and is ignored by `.gitignore`.

`backend/.venv/` and `backend/.pytest_cache/` exist locally but are ignored by `.gitignore`; they are not project source.

`backend/samples/.gitkeep` preserves an otherwise empty samples directory. There are no sample DAG JSON files yet.

`backend/tests/__init__.py` exists, but there are no test modules.

## Frontend

```text
frontend/
└── README.md
```

The [[Frontend]] is a placeholder. There is no `package.json`, framework configuration, component tree, routing setup, build pipeline, or UI source code.

## Docs

The `docs/` folder is this Obsidian knowledge base. It is the single source of truth for future AI-assisted development and should be updated whenever implementation changes.

## Relationship Map

- [[Backend]] owns [[DAG Models]] today.
- [[Frontend]] depends on future [[04_APIs|APIs]], but no dependency exists in code yet.
- [[04_APIs|APIs]] will depend on [[DAG Models]] when implemented.
- [[State Store]], [[Queue Broker]], [[Response Cache]], [[Provider Router]], [[Checkpoint Engine]], and [[Worker]] are named backend package boundaries with no implementation.

## Related

- [[00_Project_Overview|Project Overview]]
- [[01_Architecture|Architecture]]
- [[10_Current_Status|Current Status]]
