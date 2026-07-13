# Ather OS Knowledge Base

This `/docs` folder is the Obsidian knowledge base for [[00_Project_Overview|Ather OS]]. It records what the repository currently contains, how the pieces relate, and where the implementation differs from the larger product vision described in [[09_Roadmap|Roadmap]].

## Start Here

- [[00_Project_Overview|Project Overview]] explains the current project purpose and implementation boundary.
- [[01_Architecture|Architecture]] maps the intended system against the code that exists today.
- [[02_Folder_Structure|Folder Structure]] documents every project folder and its responsibility.
- [[10_Current_Status|Current Status]] is the most direct snapshot of implemented, partial, missing, and risky areas.
- [[11_Tasks|Tasks]] is the living task list for future development.

## Core Areas

- [[03_Database|Database]]
- [[04_APIs|APIs]]
- [[05_Components|Components]]
- [[06_State_Management|State Management]]
- [[State Store]]
- [[07_Authentication|Authentication]]
- [[08_UI_System|UI System]]

## Project Memory

- [[12_Bugs|Bugs]]
- [[13_Decisions|Decisions]]
- [[14_Changelog|Changelog]]

## Current Knowledge Graph

[[00_Project_Overview|Project Overview]] connects to [[01_Architecture|Architecture]], which currently centers on [[DAG Models]] in `backend/src/ather_os/dag/models.py`, [[DAG Validator]] in `backend/src/ather_os/dag/validators.py`, and [[State Store]] in `backend/src/ather_os/state/`. [[DAG Models]] define [[Workflow Model]], [[Task Model]], [[TaskType]], and [[QualityTier]]. [[DAG Validator]] verifies workflow dependency structure before future [[04_APIs|APIs]], [[06_State_Management|State Management]], [[03_Database|Database]], [[Checkpoint Engine]], [[Provider Router]], and [[Worker]] code rely on it.

The [[Frontend]] is currently a placeholder. The [[Backend]] contains package boundaries for the planned engine; [[State Store]] now has real code, while several other modules still contain only package docstrings. This means many documents explain why a topic is not yet applicable while still linking to the planned responsibility that appears in the repository structure.
