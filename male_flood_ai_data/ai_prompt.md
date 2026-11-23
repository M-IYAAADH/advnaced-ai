# Codex prompt: set up the Malé model-comparison study (supporting experiment)

Paste the following into Codex at the project repository root (`advance ai/`, the clone of `M-IYAAADH/advnaced-ai`).

Revised 2026-11-23 to fix conflicts with the project docs. Original kept outside the project folder.

---

Set up a **supporting** daily model-comparison study for our Malé-island flood AI project. Create the planning documents and add claimable tasks to the existing sprint board so each team member can pick a method and build their part.

This run is planning and team setup only. Do not train the candidate models, choose a winner, fabricate results or push.

## Read first (there is no AGENTS.md in this repo)

Read these before writing anything. Where they conflict with this prompt, they win:
1. `CLAUDE.md`: scope, data cautions, task-tracking rules (§7).
2. `agent.md`: research question, processing conventions, sprint workflow (§8).
3. `sprint.md`: the **only** task board. `sprint_board.html` validates it.
4. `data_issues.md`, especially G1–G6.
5. `reports/extended_analysis.md`, `reports/daily_exploration.md`, `reports/data_inventory_and_progress_report.md` §6.
6. The code behind those reports: `scripts/explore_daily_flood.py`, `scripts/extended_daily_analysis.py`, `scripts/build_dashboard.py`. These may still be uncommitted; do not discard or move them.
7. In the data root: `README.md`, `FOLDER_MAP.md`, `06_research/reports/CHATGPT_DATA_UPDATE.md`, `06_research/reports/TIME_ALIGNMENT_REPORT.md`, `06_research/reports/SOURCE_VERIFICATION_REPORT.md`, `03_reviewed/events/review_counts_v003.csv`.

**Data root:** the organised data folder `male_flood_ai_data/`, currently at `~/Downloads/male_flood_ai_data/`. Code takes it as a `--data-root` argument (or the `MALE_FLOOD_DATA_ROOT` environment variable). Never hard-code the absolute path.

## Scope: what this study is, and is not

- The project's research question is **which roads or road sections on Malé island proper are prone to rain flooding** (`agent.md` §1–2). This study does not answer it.
- This study is a supporting experiment. It asks how well daily weather ranks days with an accepted rain-flood report. Every document must say so, in those words or close to them.
- The lecturer confirmed that a model comparison is **not required** (`agent.md` §3; PB-04 was removed from `sprint.md`). This is optional group work. It must not displace the literature review (MF-70) or the road work (MF-20 to MF-33).
- Every new sprint row is `Conditional = Yes`. MC-F02 includes a go/no-go record that the group must approve before any scored run (see below).
- Do not change the existing MF-50 decision. MF-50 concerns road ranking; this study does not create flooded/dry road labels.

## Task IDs and the board

- Use the prefix **MC-** for every new task, so model IDs cannot be confused with team members `M1`/`M2`/`M3`:
  - MC-F01, MC-F02, MC-F03: shared setup.
  - MC-M01 to MC-M06: methods.
  - MC-C01, MC-C02, MC-C03: comparison, final test, write-up.
- Add one row per task to the `sprint.md` Tasks table. Follow its rules exactly:
  - headers unchanged;
  - no `|` inside cells;
  - Sprint is an existing Sprint ID;
  - Owner is `M1`, `M2` or `M3`;
  - Status is `To do`;
  - Points are whole numbers;
  - Depends on lists only existing task IDs, or `None`;
  - `Conditional = Yes`.
- Owners are **proposals** taken from the team focus in `sprint.md` (M1 modelling and evaluation, M2 data and pipelines, M3 writing). Anyone claims a task by changing its Owner cell and setting `In progress`. Use the proposed owner, sprint and points in `docs/model_comparison_tasks.md`.
- Do **not** create a root `todo.md` or any second status board. Checklists and completion criteria go in `docs/model_comparison_tasks.md`. Status lives only in `sprint.md`.
- Commit the docs and the sprint rows together in one local commit, `MC-setup: To do`. Do not push. A human pushes after review, following `CLAUDE.md` §7.

## Candidate methods (fixed initial list)

- MC-M01: constant-score baseline using training-set report prevalence.
- MC-M02: rainfall-threshold baseline with a continuous rainfall ranking score.
- MC-M03: regularised Logistic Regression.
- MC-M04: Random Forest with constrained tree complexity.
- MC-M05: Gradient Boosted Trees (scikit-learn `GradientBoostingClassifier`).
- MC-M06: Support Vector Machine with an RBF kernel.

MC-M01 to MC-M03 already have earlier versions in `scripts/extended_daily_analysis.py`: a prevalence baseline, a training-F1 rainfall threshold and logistic regression. Port them to the shared interface rather than rewrite them. Record that the earlier results used the v001 label set (11 retained events) and are superseded.

## Create the shared protocol before implementation

Write:
1. `docs/model_comparison_plan.md`: the protocol.
2. `docs/model_comparison_tasks.md`: per-task checklists, adapted from the supplied starter `todo (1).md`.

Do not write a separate team-workflow document. `agent.md` §8 is the workflow; the tasks file adds only the claim and handover rules.

The protocol must fix the following.

**Labels (from v003, recounted by MC-F01, not copied from this prompt)**
- Source: `03_reviewed/events/flood_events.csv` v003 in the data root.
- Target: calendar days asserted as accepted rain-report days on Malé island proper. `review_counts_v003.csv` currently gives 29 such days from 30 accepted rain events.
- A label of 0 means "no accepted report in this catalogue". It is unlabelled, not dry. Keep this wording in every output.
- The 2 overnight-window events are masked from the primary daily target and never expanded into daily positives. Give them a separate sensitivity policy.
- Uncertain-date windows and single uncertain dates are masked from the primary target.
- Coastal events and mixed-cause events are masked from the rain target. They are not label 0.
- Declare the primary rule for the 3 property-level-only events and the 13 single-source events. Run a sensitivity analysis with and without them.

**Features (small and rainfall-first)**
- Primary source: ERA5 via Open-Meteo on its established UTC+5 clock. Its release latency and original request remain unknown, so every result is retrospective.
- Hulhulé station rainfall is a separate, later feature set.
  - It ends on 2025-08-24.
  - GSOD for local day L is stored on date L+1.
  - The SYNOP 24-hour group has a one-tenth defect on 178 days, so use the 6- and 12-hour blocks for magnitude.
  - The station is on Hulhulé, not Malé.
- Sea level is a separate later experiment on common coverage. The marine model's clock (UTC+4 or UTC+5) is unresolved.
- Fill `04_model_ready/features/feature_catalog.csv`, which so far has only its header. Record units, window, lag and availability at issue time for each feature.

**Experiments**
- Two separate experiment IDs:
  - `retrospective_daily`: same-day weather against same-day reports.
  - `next_day_hindcast`: weather up to the issue time against the next day.
- Define the issue time, horizon and accumulation windows for each.
- A reanalysis hindcast does not establish live forecast availability; say so.

**Splits**
- Chronological development folds plus one final held-out period.
- Use `03_reviewed/storm_groups/validation_blocks_proposed_v002.csv` (28 rain blocks) to keep related events in one fold. Mark it provisional.
- Fill `04_model_ready/splits/splits.csv`, which so far has only its header.
- Before freezing, count the positives and blocks in every fold and in the final test. The earlier yearly folds had only 2–4 reported days each, and no separate final test was possible.
- If the final test would hold fewer than about 3 blocks, record that and choose a fallback, for example nested folds only with no separate final test. Do not split anyway.
- Define what happens when a fold has no positives, or when its training data has only one class.

**Fitting and tuning**
- Fit model-specific preprocessing only within training folds.
- Use one shared class-imbalance policy. Do not apply both class weights and equivalent sample weights.
- At most 12 predeclared configurations per classifier per experiment, with a fixed seed policy. With so few positives, prefer the smaller grids given below.
- Select parameters and alert thresholds on validation data only.

**Metrics**
- Primary: per-fold average precision against catalogue labels, with positive counts and variability. Do not pool raw scores across folds without a documented reason.
- Secondary: reported-event recall, catalogue precision and F1, flagged days and fraction, and runtime.
- Alert rule: a common validation alert budget, for example 5% of validation days. Report the realised held-out flagged fraction.
- Make no claims about verified physical false alarms or calibrated flood probabilities.

**Go/no-go (part of MC-F02)**
- Before any scored run, write a short decision record in the plan. It states:
  - the per-fold positive counts;
  - whether the six-method comparison can separate methods at all;
  - the group's approval.
- C01 may legitimately conclude that "no method is distinguishable from the baselines".

Recommend bounded initial parameter ranges for each classifier. Keep candidate settings separate from any decision about a winner.

## Implementation contract (repo conventions: `scripts/` and `derived/`)

The repo has no `src/`, `configs/` or `tests/` folder, and `pyyaml` is not a dependency. Use:
- `scripts/models/<model_id>.py`. Each module defines:
  - `CONFIG`, a plain dict holding fixed settings and the bounded search grid;
  - `build_estimator(config, random_state)`, which returns an unfitted scikit-learn estimator or pipeline.
- `docs/models/<model_id>.md`: method notes.
- `tests/test_<model_id>.py`: stdlib `unittest`, run with `python -m unittest`. No new test dependency.
- Shared evaluator (MC-F03): `scripts/model_comparison.py`, extending or importing from `scripts/extended_daily_analysis.py`. Do not fork the label or fold logic.
- Run outputs in the data root: `05_outputs/runs/<experiment_id>/<model_id>/<run_id>/`. Follow `05_outputs/runs/README.md`.
- Keep `derived/daily_exploration/` and `derived/extended_analysis/` intact as legacy outputs.
- Model IDs: `constant`, `rainfall_threshold`, `logistic_regression`, `random_forest`, `gradient_boosting`, `svm_rbf`.

The score must be continuous, with larger values meaning stronger evidence for the positive catalogue class. The evaluator accepts `predict_proba` or `decision_function`. The SVM uses `decision_function` without calibration.

One evaluation owner (MC-F03, and later MC-C02) implements loading, folds, tuning, threshold selection, metrics and output validation. Model owners reuse it and do not write their own evaluation rules.

Freeze the prediction and metric schemas in the plan.
- Prediction columns: `experiment_id`, `dataset_version`, `feature_set_id`, `split_version`, `model_id`, `run_id`, `fold_id`, `target_date`, `event_ids`, `y_catalogue`, `score`, `predicted_label`, `evaluation_role`.
- Metric fields: as in the tasks file.

If you add a dependency, pin it in `requirements.txt`.

## Board content

Rows MC-F01 to MC-F03, MC-M01 to MC-M06 and MC-C01 to MC-C03, with the proposed sprint, owner, points and dependencies from `docs/model_comparison_tasks.md`.
- Members may write their estimator factory and method notes now.
- Official scored runs depend on MC-F01 to MC-F03 and the go/no-go record.
- Model owners deliver code, a bounded config, checks, a reproduction command, validation outputs and a handover. A different member reviews before `Done`.
- MC-C02 runs the final test once, after MC-C01 has frozen every candidate's settings. No retuning or reselection from final-test results.

## Data and sharing rules

- Never edit raw files.
- Keep the Council workbook (`bobs flood.xlsx`) out of any shared bundle until permission is confirmed.
- Do not invent data counts, completion statuses or results. Where the repo evidence is not enough, write "unknown".

End with: the files created or updated, the new sprint rows, the first shared tasks to claim (MC-F01, MC-F02), and any conflict you could not resolve.
