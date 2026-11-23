# AGENTS.md

Instructions for coding agents (Codex and others) working in this repo. Claude Code reads `CLAUDE.md`; the rules are the same.

## Read before doing anything

1. `CLAUDE.md`: requirements, scope, data cautions, task-tracking rules (§7).
2. `agent.md`: working brief, processing conventions, data locations, sprint workflow (§8).
3. `sprint.md`: the only task board. `sprint_board.html` validates it.
4. `todo.md`: checklists for the supporting model-comparison study (status still lives in `sprint.md`).
5. `data_issues.md` and `reports/combined_folder_review.md`: known data problems and the current evidence by ward.

Where this file and those disagree, those files win. The student's latest explicit instruction wins over all of them.

## Rules you must not break

- **Question:** which areas of Malé island proper flood after rain. Report by the 4 OSM wards; analyse on the 200 m grid (`derived/male_grid_200m.geojson`). This is susceptibility mapping, not forecasting.
- **Labels are positive-only.** No report means unknown, never dry. Do not create negative labels.
- **Rainfall:** keep units and accumulation periods; an unknown period stays `unknown`; never call an amount a threshold.
- **Data:** never edit raw files. Outputs go in `derived/`, built by scripts in `scripts/` with project-relative paths. Never invent counts, labels or results.
- **Privacy:** the Council workbook (`bobs flood.xlsx`) must never be committed or shared.
- **Tasks:** before starting, find or add the task's row in `sprint.md` (Owner `M1`/`M2`/`M3`, Status `To do`/`In progress`/`Review`/`Done`, no `|` inside cells). Set `Review` when its acceptance check is met; another member sets `Done`.
- **Git:** commit the work and its `sprint.md` change together (`MF-xx: Review`). Push only when the student has asked you to.

## Run

Python 3.12: `python -m pip install -r requirements.txt`, then the steps in `README.md`, from the project root.
