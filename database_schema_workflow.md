# Database Schema Workflow — HR Employee Churn

## Overview

This workflow defines the relational database schema for the HR Employee Churn dataset
(`hr_employee_churn_data.csv`, 14,999 records). The raw flat CSV is normalized into four
tables to eliminate redundancy and support efficient querying.

---

## Step 1 — Identify Entities and Normalize

The flat CSV has 10 columns. Normalization splits it into:

| Table | Purpose |
|---|---|
| `salary_levels` | Lookup table for salary categories |
| `employees` | Core employee identity and employment info |
| `performance_records` | Satisfaction, evaluation, projects, hours |
| `employment_events` | Accidents, promotions, and turnover outcome |

---

## Step 2 — Entity Relationship Diagram (ERD)

```
salary_levels          employees
─────────────          ─────────────────────────────
salary_id (PK)  ◄───── salary_id (FK)
salary_label           emp_id (PK)
                       time_spend_company

                           │1
                           │
               ┌───────────┴────────────┐
               │                        │
   performance_records        employment_events
   ────────────────────        ─────────────────────
   record_id (PK)              event_id (PK)
   emp_id (FK)                 emp_id (FK)
   satisfaction_level          work_accident
   last_evaluation             promotion_last_5years
   number_project              left
   average_monthly_hours
```

---

## Step 3 — DDL: Create Tables

```sql
-- ── 1. Lookup: salary levels ──────────────────────────────────────────
CREATE TABLE salary_levels (
    salary_id     SERIAL        PRIMARY KEY,
    salary_label  VARCHAR(10)   NOT NULL UNIQUE  -- 'low', 'medium', 'high'
);

-- ── 2. Core employee table ────────────────────────────────────────────
CREATE TABLE employees (
    emp_id              INT           PRIMARY KEY,
    salary_id           INT           NOT NULL,
    time_spend_company  INT           NOT NULL CHECK (time_spend_company >= 0),
    FOREIGN KEY (salary_id) REFERENCES salary_levels(salary_id)
);

-- ── 3. Performance records ────────────────────────────────────────────
CREATE TABLE performance_records (
    record_id              SERIAL        PRIMARY KEY,
    emp_id                 INT           NOT NULL UNIQUE,
    satisfaction_level     DECIMAL(4,3)  CHECK (satisfaction_level BETWEEN 0 AND 1),
    last_evaluation        DECIMAL(4,3)  NOT NULL CHECK (last_evaluation BETWEEN 0 AND 1),
    number_project         INT           NOT NULL CHECK (number_project >= 0),
    average_monthly_hours  INT           NOT NULL CHECK (average_monthly_hours >= 0),
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
);

-- ── 4. Employment events (accidents, promotions, turnover) ────────────
CREATE TABLE employment_events (
    event_id               SERIAL   PRIMARY KEY,
    emp_id                 INT      NOT NULL UNIQUE,
    work_accident          BOOLEAN  NOT NULL DEFAULT FALSE,
    promotion_last_5years  BOOLEAN  NOT NULL DEFAULT FALSE,
    left_company           BOOLEAN  NOT NULL DEFAULT FALSE,
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
);
```

---

## Step 4 — Seed Lookup Data

```sql
INSERT INTO salary_levels (salary_label) VALUES
    ('low'),
    ('medium'),
    ('high');
```

---

## Step 5 — Load CSV Data

### Option A — Python (Pandas + psycopg2)

```python
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# Connection
engine = create_engine("postgresql://user:password@localhost:5432/hr_churn")

# Load CSV
df = pd.read_csv("hr_employee_churn_data.csv")
df["satisfaction_level"] = df["satisfaction_level"].fillna(df["satisfaction_level"].mean())

# Map salary labels to IDs
salary_map = {"low": 1, "medium": 2, "high": 3}
df["salary_id"] = df["salary"].map(salary_map)

# Insert employees
employees_df = df[["empid", "salary_id", "time_spend_company"]].rename(columns={"empid": "emp_id"})
employees_df.to_sql("employees", engine, if_exists="append", index=False)

# Insert performance_records
perf_df = df[["empid", "satisfaction_level", "last_evaluation",
              "number_project", "average_montly_hours"]].rename(columns={
    "empid": "emp_id",
    "average_montly_hours": "average_monthly_hours"
})
perf_df.to_sql("performance_records", engine, if_exists="append", index=False)

# Insert employment_events
events_df = df[["empid", "Work_accident", "promotion_last_5years", "left"]].rename(columns={
    "empid": "emp_id",
    "Work_accident": "work_accident",
    "left": "left_company"
})
events_df["work_accident"] = events_df["work_accident"].astype(bool)
events_df["promotion_last_5years"] = events_df["promotion_last_5years"].astype(bool)
events_df["left_company"] = events_df["left_company"].astype(bool)
events_df.to_sql("employment_events", engine, if_exists="append", index=False)

print("Load complete.")
```

### Option B — PostgreSQL `COPY` (direct from CSV)

```sql
-- Requires a staging table first, then transform into normalized tables
CREATE TEMP TABLE staging (
    empid                 INT,
    satisfaction_level    FLOAT,
    last_evaluation       FLOAT,
    number_project        INT,
    average_montly_hours  INT,
    time_spend_company    INT,
    work_accident         INT,
    promotion_last_5years INT,
    salary                VARCHAR(10),
    left                  INT
);

COPY staging FROM '/path/to/hr_employee_churn_data.csv'
    WITH (FORMAT csv, HEADER true);

-- Populate employees
INSERT INTO employees (emp_id, salary_id, time_spend_company)
SELECT s.empid,
       sl.salary_id,
       s.time_spend_company
FROM staging s
JOIN salary_levels sl ON sl.salary_label = s.salary;

-- Populate performance_records
INSERT INTO performance_records
    (emp_id, satisfaction_level, last_evaluation, number_project, average_monthly_hours)
SELECT empid,
       COALESCE(satisfaction_level, 0.613),  -- impute missing with mean
       last_evaluation,
       number_project,
       average_montly_hours
FROM staging;

-- Populate employment_events
INSERT INTO employment_events
    (emp_id, work_accident, promotion_last_5years, left_company)
SELECT empid,
       work_accident::BOOLEAN,
       promotion_last_5years::BOOLEAN,
       left::BOOLEAN
FROM staging;

DROP TABLE staging;
```

---

## Step 6 — Verify the Load

```sql
-- Row counts should all be 14,999
SELECT 'employees'         AS tbl, COUNT(*) FROM employees
UNION ALL
SELECT 'performance_records',      COUNT(*) FROM performance_records
UNION ALL
SELECT 'employment_events',        COUNT(*) FROM employment_events;

-- Check for orphaned foreign keys
SELECT COUNT(*) AS orphaned_perf
FROM performance_records p
LEFT JOIN employees e ON e.emp_id = p.emp_id
WHERE e.emp_id IS NULL;

-- Spot-check first 5 rows joined
SELECT e.emp_id, sl.salary_label, e.time_spend_company,
       p.satisfaction_level, p.last_evaluation, p.number_project,
       ev.work_accident, ev.left_company
FROM employees e
JOIN salary_levels     sl ON sl.salary_id   = e.salary_id
JOIN performance_records p  ON p.emp_id      = e.emp_id
JOIN employment_events  ev ON ev.emp_id      = e.emp_id
LIMIT 5;
```

---

## Step 7 — Useful Analytical Queries

```sql
-- Turnover rate overall
SELECT
    ROUND(100.0 * SUM(left_company::INT) / COUNT(*), 2) AS turnover_pct
FROM employment_events;

-- Turnover rate by salary category
SELECT
    sl.salary_label,
    COUNT(*)                                                   AS total,
    SUM(ev.left_company::INT)                                  AS left_count,
    ROUND(100.0 * SUM(ev.left_company::INT) / COUNT(*), 2)    AS turnover_pct
FROM employment_events ev
JOIN employees      e  ON e.emp_id    = ev.emp_id
JOIN salary_levels  sl ON sl.salary_id = e.salary_id
GROUP BY sl.salary_label
ORDER BY turnover_pct DESC;

-- Average satisfaction by turnover status
SELECT
    ev.left_company,
    ROUND(AVG(p.satisfaction_level)::NUMERIC, 3) AS avg_satisfaction
FROM performance_records p
JOIN employment_events ev ON ev.emp_id = p.emp_id
GROUP BY ev.left_company;

-- Employees with high risk profile (low satisfaction + no promotion + low salary)
SELECT e.emp_id, sl.salary_label, p.satisfaction_level
FROM employees e
JOIN salary_levels      sl ON sl.salary_id   = e.salary_id
JOIN performance_records p  ON p.emp_id       = e.emp_id
JOIN employment_events  ev ON ev.emp_id       = e.emp_id
WHERE p.satisfaction_level < 0.4
  AND ev.promotion_last_5years = FALSE
  AND sl.salary_label = 'low'
  AND ev.left_company = FALSE   -- still at company (at-risk)
ORDER BY p.satisfaction_level ASC;
```

---

## Schema Summary

| Table | Rows | Primary Key | Foreign Keys |
|---|---|---|---|
| `salary_levels` | 3 | `salary_id` | — |
| `employees` | 14,999 | `emp_id` | `salary_id` |
| `performance_records` | 14,999 | `record_id` | `emp_id` |
| `employment_events` | 14,999 | `event_id` | `emp_id` |
