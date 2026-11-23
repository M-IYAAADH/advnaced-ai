# Malé flood AI: model-comparison task checklists (supporting experiment)

Created: 2026-11-23. Revised 2026-11-23 to fix conflicts with the project docs.
Study area: Malé island proper.
Destination in the repo: `docs/model_comparison_tasks.md`. This is not a root `todo.md`.

**Status of this study.** This is a supporting daily experiment. It asks how well weather ranks days with an accepted rain-flood report. It does not answer the project question, which is which roads flood. The lecturer confirmed it is not required. It must not displace the literature review (MF-70) or the road work.

**Where status lives.** Only in `sprint.md`. This file holds the checklists and completion criteria. No task here is claimed, implemented, reviewed or completed by this document.

## Claim a task

1. Read `docs/model_comparison_plan.md`, `agent.md` §8 and `CLAUDE.md` §7.
2. `git pull`. In the task's `sprint.md` row, set Owner to your member ID (`M1`, `M2` or `M3`) and Status to `In progress`. Commit and push (`MC-M04: In progress`).
3. Use one owner per task. A person may own several tasks. Coordinate changes to shared files with the MC-F03 owner.
4. Work only in your task's files. Keep a short handover: changes, commands, results, open dependencies.
5. Set Status to `Review` when the deliverables are ready. A different member reviews and sets `Done`. Record the review evidence in your handover.

Board statuses: `To do`, `In progress`, `Review`, `Done`. A Blocked task stays `In progress`, with the blocker written in its handover.

You may prepare a method task (factory and notes) now. Official scored runs need MC-F01 to MC-F03 in `Done` and the go/no-go record approved.

## Proposed sprint rows

Owners are proposals based on the team focus in `sprint.md`; anyone may claim instead. All rows: Status `To do`, Conditional `Yes`.

| ID | Sprint | Owner | Points | Task | Depends on | Issues |
| --- | --- | --- | --- | --- | --- | --- |
| MC-F01 | S5 | M2 | 3 | Freeze v003 daily label snapshot and ERA5 feature table | None | G4, G5, G6 |
| MC-F02 | S5 | M1 | 3 | Freeze features, timing, splits, metrics and go/no-go record | MC-F01 | G3, G5 |
| MC-F03 | S5 | M2 | 5 | Shared model interface and evaluation harness | MC-F01, MC-F02 | None |
| MC-M01 | S5 | M1 | 1 | Constant-score baseline | MC-F03 | None |
| MC-M02 | S5 | M1 | 1 | Rainfall-threshold baseline | MC-F03 | None |
| MC-M03 | S6 | M1 | 2 | Logistic Regression | MC-F03 | None |
| MC-M04 | S6 | M1 | 2 | Random Forest | MC-F03 | None |
| MC-M05 | S6 | M2 | 2 | Gradient Boosted Trees | MC-F03 | None |
| MC-M06 | S6 | M2 | 2 | RBF Support Vector Machine | MC-F03 | None |
| MC-C01 | S6 | M1 | 2 | Compare validation results and freeze selection | MC-M01, MC-M02, MC-M03, MC-M04, MC-M05, MC-M06 | G3 |
| MC-C02 | S6 | M2 | 2 | Evaluate frozen candidates on the final held-out period | MC-C01 | None |
| MC-C03 | S7 | M3 | 3 | Dashboard, figures and write-up of the comparison | MC-C01, MC-C02 | G1, G5 |

Acceptance text for each row is the "Done when" line of its section below.

## Shared comparison rules

- Labels come from `03_reviewed/events/flood_events.csv` v003 in the data root. A label of 0 means no accepted report; it does not mean a dry day.
- Overnight windows, uncertain dates, and coastal or mixed events are masked from the primary rain target. Windows are never expanded into daily positives.
- The earlier results in `derived/extended_analysis/` used v001 labels (11 retained events). Treat them as superseded legacy outputs, and keep them intact.
- Within each experiment, use the same data version, labels, eligible dates, features and folds. A baseline may use a subset of the features.
- Keep `retrospective_daily` and `next_day_hindcast` results separate. ERA5 latency is unknown, so both are retrospective. The hindcast is not a demonstrated forecast.
- The initial features are ERA5 rainfall only. Station rainfall and sea level are separate later feature sets (see the plan for the GSOD and sea-level clock caveats).
- Fit imputation, scaling and any feature selection inside each training fold. Do no resampling before splitting.
- Tune only within chronological development folds. Keep each proposed validation block (`validation_blocks_proposed_v002.csv`) inside one fold. Document any uncertain grouping.
- Use the frozen imbalance policy. Do not apply both class weights and equivalent sample weights.
- At most 12 predeclared configurations per classifier per experiment; smaller is better with this few positives. Use the shared seed policy.
- Select alert thresholds on validation data using the common rule. Report the realised held-out flagged fraction.
- Average precision uses continuous scores. SVM margins are fine.
- Report metrics per fold, with positive counts. Do not pool raw scores across folds without a documented reason.
- Model owners use development data only. MC-C02 owns the single final-test run.
- Preserve raw data and earlier outputs. Do not change another member's files or claim without asking.
- Never fill a leaderboard with expected, invented or training-only numbers.
- Keep the Council workbook out of shared bundles until permission is confirmed.

## File ownership and interface (repo conventions)

| Area | Owner | Path |
|---|---|---|
| Label snapshot and feature table | MC-F01 | `04_model_ready/` in the data root (versioned files) |
| Feature catalogue | MC-F01, MC-F02 | `04_model_ready/features/feature_catalog.csv` (data root) |
| Protocol and fold definitions | MC-F02 | `docs/model_comparison_plan.md`; `04_model_ready/splits/splits.csv` (data root) |
| Shared runner and scoring | MC-F03 | `scripts/model_comparison.py`, reusing `scripts/extended_daily_analysis.py` |
| Model code and bounded config | MC-Mxx | `scripts/models/<model_id>.py` (a `CONFIG` dict plus `build_estimator`) |
| Model notes | MC-Mxx | `docs/models/<model_id>.md` |
| Model checks | MC-Mxx | `tests/test_<model_id>.py` (stdlib `unittest`) |
| Run outputs | Shared schema | `05_outputs/runs/<experiment_id>/<model_id>/<run_id>/` (data root) |

The data root is passed as `--data-root` or `MALE_FLOOD_DATA_ROOT`. Never hard-code it.

Factory: `build_estimator(config, random_state)` returns an unfitted estimator or pipeline compatible with the shared runner. Preprocessing a method needs belongs in its pipeline or in the agreed common layer, not both.

Score direction: larger values mean stronger evidence for the positive catalogue class. The evaluator adapts `predict_proba` or `decision_function`.

## MC-F01: shared modelling snapshot

- [ ] Read `CHATGPT_DATA_UPDATE.md`, `TIME_ALIGNMENT_REPORT.md`, `SOURCE_VERIFICATION_REPORT.md` and `review_counts_v003.csv`.
- [ ] Recount events, asserted days, overnight windows and uncertain windows from v003. Do not copy the counts in this file.
- [ ] Build the primary daily target and its masks: windows, uncertain dates, coastal and mixed events.
- [ ] Flag property-level-only and single-source events for the sensitivity analysis.
- [ ] Keep label 0 as "no accepted report" in every column name and note.
- [ ] Build the ERA5 daily feature table on the established UTC+5 clock, and profile missingness.
- [ ] Record data versions, checksums, exclusions and the reproduction command.
- [ ] Hand off for review.

Done when the snapshot is reproducible and a reviewer can trace every label and feature to its source row.

## MC-F02: experiment and comparison protocol

- [ ] List the features with meaning, units, window and lag. Fill `feature_catalog.csv`.
- [ ] Define `retrospective_daily` and `next_day_hindcast`: issue time and target interval.
- [ ] Document time alignment, interval endpoints, lags and latency assumptions (ERA5 latency unknown).
- [ ] Freeze eligible dates and chronological folds, keeping validation blocks whole. Fill `splits.csv`.
- [ ] Count positives and blocks per fold and in the final test. If the final test has fewer than about 3 blocks, record it and choose the fallback.
- [ ] Define the average-precision aggregation and the secondary metrics.
- [ ] Define the common alert-budget rule, for example 5% of validation days.
- [ ] Define the imbalance handling, search budget and seeds.
- [ ] Define what happens when a fold has no positives, or when its training data has one class.
- [ ] Write the go/no-go record (per-fold counts, whether methods can be separated) and get group approval.

Done when every model owner can use one versioned specification and the group has approved the go/no-go.

## MC-F03: shared evaluation implementation

- [ ] Freeze the factory and the prediction and metric schemas.
- [ ] Extend or import from `scripts/extended_daily_analysis.py`: one loader, fold iterator, tuning and scoring procedure.
- [ ] Fit transformations on training data only.
- [ ] Support both probability scores and decision margins.
- [ ] Validate unique prediction keys, date and fold joins, and common evaluation rows.
- [ ] Check label leakage, feature lags, block boundaries and missingness.
- [ ] Add a check that changing held-out data cannot change the fitted training preprocessing.
- [ ] Pin any new dependency in `requirements.txt`.
- [ ] Run a small development smoke run and document how model owners run it.

Prediction columns: `experiment_id`, `dataset_version`, `feature_set_id`, `split_version`, `model_id`, `run_id`, `fold_id`, `target_date`, `event_ids`, `y_catalogue`, `score`, `predicted_label`, `evaluation_role`.

Metric fields: evaluated days, positive days, reported-event count, average precision, reported-event recall, flagged days and fraction, catalogue precision and F1, runtime, score method, threshold and threshold-selection rule.

Done when a model owner can plug in an unfitted estimator without redefining labels, splits or metrics.

## Common checklist for each method owner

Apply this within your own MC-Mxx task only.

- [ ] Claim the task in `sprint.md` and confirm the protocol version.
- [ ] Write concise method notes: rationale, limitations, references.
- [ ] Implement the factory and the training-only preprocessing it needs.
- [ ] Declare a bounded grid in `CONFIG`, within the common budget.
- [ ] Follow the common imbalance and seed policy.
- [ ] Add fit/score, missingness and reproducibility checks as applicable.
- [ ] Run the shared validation evaluator once MC-F01 to MC-F03 are `Done` and the go/no-go is approved.
- [ ] Save settings, fold predictions, metrics, runtime and reproduction commands.
- [ ] Summarise strengths and failures. Do not read feature importance as causation.
- [ ] Hand off for review. Leave the final test to MC-C02.

Done means the module, config, notes, checks and reproducible validation outputs are reviewed and meet the shared contract. Code alone is not completion.

## MC-M01: constant-score baseline

Model ID: `constant`. Suggested estimator: `DummyClassifier(strategy="prior")`. An earlier version exists in `scripts/extended_daily_analysis.py`; port it.

- [ ] Estimate the catalogue-positive fraction from the training fold only.
- [ ] Give every evaluated day that score.
- [ ] Document tie handling for the threshold and alert-budget metrics.
- [ ] Complete the common checklist.

Purpose: performance when weather adds no ranking information.

## MC-M02: rainfall-threshold baseline

Model ID: `rainfall_threshold`. An earlier training-F1 version exists in `scripts/extended_daily_analysis.py`; port it to the common alert-budget rule.

- [ ] Choose the rainfall feature from the frozen experiment definition.
- [ ] Use continuous rainfall as the ranking score.
- [ ] Select the binary alert threshold under the shared validation-only rule.
- [ ] Use preceding weather for the hindcast and the declared same-day feature for the retrospective experiment.
- [ ] Check monotonic score ordering and rainfall missingness.
- [ ] Complete the common checklist.

Purpose: does a simple rainfall rule already explain the catalogue pattern?

## MC-M03: regularised Logistic Regression

Model ID: `logistic_regression`. Suggested estimator: `LogisticRegression` with L2. An earlier version exists in `scripts/extended_daily_analysis.py`; port it.

- [ ] Include training-fitted imputation and scaling as agreed.
- [ ] Use a small C range, for example 0.1, 1, 10.
- [ ] Check convergence and the agreed class-weight policy.
- [ ] Save coefficients with feature names and preprocessing context.
- [ ] Complete the common checklist.

Purpose: interpretable regularised classifier.

## MC-M04: Random Forest

Model ID: `random_forest`. Suggested estimator: `RandomForestClassifier`.

- [ ] Bound depth and leaf size, for example max_depth 2–4 and min_samples_leaf 5–20.
- [ ] Keep the grid small, at most 6 configurations recommended.
- [ ] Fix the tree count and seed at first.
- [ ] Document the imbalance policy and what score values mean.
- [ ] Report feature importance cautiously; the inputs are correlated.
- [ ] Complete the common checklist.

Purpose: nonlinear averaging tree ensemble.

## MC-M05: Gradient Boosted Trees

Model ID: `gradient_boosting`. Suggested estimator: scikit-learn `GradientBoostingClassifier`.

- [ ] Use shallow trees (depth 1–2) and a small learning-rate and estimator-count grid.
- [ ] Apply the agreed training-only sample weights if class balancing is selected.
- [ ] Keep tuning and early-stopping decisions inside chronological development data.
- [ ] Document how sequential boosting differs from the forest.
- [ ] Complete the common checklist.

Purpose: boosting against averaging. XGBoost is not part of this study.

## MC-M06: RBF Support Vector Machine

Model ID: `svm_rbf`. Suggested estimator: `SVC(kernel="rbf", probability=False)`.

- [ ] Include training-fitted imputation and scaling as agreed.
- [ ] Use small C and gamma ranges within the budget.
- [ ] Apply the agreed class weighting.
- [ ] Use `decision_function` as the continuous score.
- [ ] Leave probability calibration out of the initial comparison.
- [ ] Complete the common checklist.

Purpose: nonlinear kernel comparator, distinct from the tree models.

## MC-C01: compare validation and freeze selection

- [ ] Verify that all six methods used the same protocol versions and evaluation dates.
- [ ] Produce a separate validation leaderboard for each experiment.
- [ ] Show per-fold results and counts alongside the aggregates.
- [ ] Compare each classifier against both baselines.
- [ ] Apply the predeclared selection rule. If the differences sit within the fold-to-fold spread, record "no method distinguishable".
- [ ] Freeze each candidate's settings and record the validation-based preference, if any.
- [ ] Record the remaining uncertainty and the planned final-test run.

Done when the selection is recorded before any final-test result is seen.

## MC-C02: final held-out evaluation

- [ ] Confirm MC-C01's frozen settings and selection record.
- [ ] Fit the frozen procedures on their permitted development data.
- [ ] Run the final evaluation once for all frozen candidates. If MC-F02 chose the no-final-test fallback, record that instead.
- [ ] Keep retrospective inputs and issue-time-available inputs distinct.
- [ ] Report results without retuning or reselecting.
- [ ] Preserve predictions, fitted artifacts, configuration and environment details.

Done when the comparison table and the final results are reproducible.

## MC-C03: dashboard and write-up

- [ ] Add comparison tables and plots with labelled validation and final-test results. Extend `scripts/build_dashboard.py`; do not start a new dashboard.
- [ ] Show accepted reported events alongside rainfall and model scores.
- [ ] Keep retrospective and next-day results visibly separate.
- [ ] State the label definition: "no accepted report", not dry.
- [ ] Write `reports/model_comparison.md` and export figures for the review (MF-70, MF-71).
- [ ] Say clearly that this is supporting work and does not answer the road question.
- [ ] Document what worked, what failed, time and feature sensitivity, and the limitations.
- [ ] Keep the Council workbook out of the shareable bundle while its sharing status is unresolved.

Done when the team can reproduce and explain the results without this chat.

## Reusable member prompt

Replace the member ID and task ID before giving this to your coding assistant:

> Read CLAUDE.md, agent.md, sprint.md, docs/model_comparison_plan.md and docs/model_comparison_tasks.md. If sprint.md shows task MC-M04 as `To do`, claim it: git pull, set Owner to M1 and Status to `In progress`, commit and push. Then implement only that task using the shared interface (scripts/models/, scripts/model_comparison.py). Do not change other members' files. Prepare the model module with a bounded CONFIG, method notes and unittest checks. Run official validation only after MC-F01 to MC-F03 are Done and the go/no-go is approved. Leave the final test to MC-C02. Then set the row to `Review`, and report changed paths, exact commands, actual results and open dependencies. If the task is already claimed, report that and leave the claim alone.

## Handover record template

- Task ID:
- Owner (member ID):
- Reviewer (member ID):
- Protocol, data and split versions:
- Branch or local changes:
- Files changed:
- Reproduction command:
- Validation results and evaluated event counts:
- Known issues and dependencies:
- Review evidence:
- Status in sprint.md:
