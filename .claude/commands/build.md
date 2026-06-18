# /build — Build the normalized SQLite database

Read `hr_employee_churn_data.csv` and load it into a normalized SQLite database called `hr_churn.db` using the 3NF schema defined in `database_schema_workflow.md`.

## Steps

1. Delete `hr_churn.db` if it already exists (fresh build every time).
2. Create the database with 4 tables in this order:
   - `salary_levels` (lookup: low / medium / high)
   - `employees` (emp_id PK, salary_id FK, time_spend_company)
   - `performance_records` (emp_id PK/FK, satisfaction_level, last_evaluation, number_project, average_monthly_hours)
   - `employment_events` (emp_id PK/FK, work_accident, promotion_last_5years, left_company)
3. Enable foreign key enforcement (`PRAGMA foreign_keys = ON`).
4. Insert all 14,999 rows into each table.
5. Verify: print row counts for all 4 tables — each should show 14,999 (salary_levels shows 3).

## Expected output

- File: `hr_churn.db` (SQLite database, ~772 KB)
- Console: row counts confirming successful load
