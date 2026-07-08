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
- [[07_Authentication|Authentication]]
- [[08_UI_System|UI System]]

## Project Memory

- [[12_Bugs|Bugs]]
- [[13_Decisions|Decisions]]
- [[14_Changelog|Changelog]]

## Current Knowledge Graph

[[00_Project_Overview|Project Overview]] connects to [[01_Architecture|Architecture]], which currently centers on [[DAG Models]] in `backend/src/ather_os/dag/models.py`. [[DAG Models]] are the only implemented domain logic. They define [[Workflow Model]], [[Task Model]], [[TaskType]], and [[QualityTier]], which will later be consumed by [[04_APIs|APIs]], [[06_State_Management|State Management]], [[03_Database|Database]], [[Checkpoint Engine]], [[Provider Router]], and [[Worker]].

The [[Frontend]] is currently a placeholder. The [[Backend]] contains package boundaries for the planned engine, but most modules contain only package docstrings. This means many documents explain why a topic is not yet applicable while still linking to the planned responsibility that appears in the repository structure.
