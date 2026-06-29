# Research Plan — Employee Retention Analytics
**Understanding Workforce Attrition Through Statistical Analysis**

Reconstructed from the repo's paper, database schema workflow (`database_schema_workflow.md`),
query results (`query_results.md`), and the four charts (`chart1`–`chart4.png`).

## 1. Problem Definition
- **Research goal:** Identify and quantify the factors that most strongly drive employee
  turnover, so HR can move from assumption-based to data-driven retention strategies.
- **New paradigm for data analysis:** Treat a flat HR CSV as a **normalized relational database
  + reproducible SQL pipeline** (crawl → build → query → report) rather than a one-off
  spreadsheet — making the analysis queryable, auditable, and repeatable.
- **Investigating the current dataset:** HR Employee Retention Dataset (Kaggle), ~14,999
  simulated employee records, 10 columns spanning satisfaction, evaluation, workload (projects,
  monthly hours), tenure, work accidents, promotions, salary band, and the `left` outcome.
- **New techniques to acquire results:** Normalize into 4 tables (`salary_levels`, `employees`,
  `performance_records`, `employment_events`) in SQLite; derive metrics via SQL aggregation and
  correlation, then visualize. A reusable AI/`/workflow` command pipeline automates each step.
- **New criteria to define the dataset:** Enforce data quality with schema constraints —
  PK/FK integrity, `CHECK` ranges (satisfaction & evaluation ∈ [0,1], non-negative hours/tenure),
  boolean typing for events, and mean-imputation of missing satisfaction.

## 2. State of the Art / Current Issues
- **Current issues in the field:** Organizations design retention strategies on intuition;
  HR signals are collected but rarely analyzed jointly; descriptive dashboards stop short of
  identifying *which* factors actually move turnover or *who* is at risk.
- **Known issues:** Most public analyses are **cross-sectional** and **correlational**
  (no causality); class imbalance (only ~24% leavers); reliance on **simulated** data limits
  external validity; single-table CSV workflows are hard to reproduce or audit.

## 3. Existing Research
- **Similar research:** People-analytics / HR-attrition studies on this same Kaggle-style dataset
  commonly report low satisfaction, low pay, heavy workload, long tenure-without-promotion, and
  lack of advancement as leading attrition drivers, often via logistic regression or tree models.
- **Issues carried from existing research + solutions:** prior work tends to (a) skip data
  engineering — *solution:* a normalized, constraint-checked schema; (b) report black-box model
  accuracy without interpretable factor ranking — *solution:* transparent correlation + group
  turnover rates; (c) stop at description — *solution:* an actionable high-risk query.

## 4. Proposed Approach (analysis + improved analytics presentation)
- **Method:** Normalize → load into `hr_churn.db` → SQL queries for turnover rates and
  satisfaction comparisons → correlation of each feature vs. `left` → high-risk profiling →
  chart-based reporting.
- **Validation of methods:**
  - **Load verification:** row counts reconcile to 14,999 across all tables; orphaned-FK check
    returns 0; 5-row joined spot-check (built into the schema workflow).
  - **Consistency:** SQL-derived turnover (23.81%) matches the chart figures (3,571 / 14,999).
- **Correctness of results:** Findings are internally consistent and directionally sensible —
  - Overall turnover **23.81%** (3,571 left, 11,428 stayed).
  - By salary: low **29.7%** > medium **20.4%** > high **6.6%**.
  - Satisfaction: stayed **0.667** vs. left **0.440**.
  - Feature correlation with turnover: satisfaction **−0.388** (strongest), work_accident −0.155,
    promotion −0.062, evaluation +0.007, projects +0.024, avg_hours +0.071, tenure **+0.145**.
- **Biggest contribution:** A **reproducible, constraint-validated SQL pipeline** that converts a
  raw HR CSV into ranked, interpretable turnover drivers **and an operational at-risk employee list**
  (615 still-employed high-risk workers) HR can act on immediately — not just a model score.

## 5. Results & Lessons Learned
- Low **satisfaction** and low **salary** are the dominant attrition drivers; evaluation score and
  project count are near-zero predictors.
- Data engineering (normalization + constraints) caught quality issues early and made every result
  reproducible.
- Key limitation/lesson: results are **associations on simulated data** — not causal proof; class
  imbalance must be considered before any predictive modeling.

## 6. Further Research
- Add **predictive modeling** (logistic regression, decision tree, random forest) with proper
  handling of class imbalance, to score individual risk rather than describe group rates.
- Identify **thresholds** (satisfaction or monthly-hours cutoffs where turnover spikes) and
  **interaction effects** (salary × satisfaction × workload).
- Validate on **real, longitudinal** organizational data.
- Productionize the high-risk query into an **early-warning HR dashboard**.
