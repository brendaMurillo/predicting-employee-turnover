# /validate — Validate the full pipeline output

Check that every stage of the pipeline ran correctly and all expected files exist with correct content.

## Checks to perform

### 1. File existence
Confirm all these files exist in the project root:
- [ ] `hr_employee_churn_data.csv`
- [ ] `hr_churn.db`
- [ ] `query_results.md`
- [ ] `HR_Employee_Churn_Report.html`
- [ ] `HR_Employee_Churn_Poster.html`
- [ ] `chart1.png` through `chart4.png`
- [ ] `database_schema_workflow.md`

### 2. CSV validation
- Row count = 14,999
- Column count = 10
- Zero missing values in all columns

### 3. Database validation
- All 4 tables exist: `salary_levels`, `employees`, `performance_records`, `employment_events`
- `salary_levels` has exactly 3 rows
- `employees`, `performance_records`, `employment_events` each have exactly 14,999 rows
- Foreign key integrity: no orphaned rows in any joined table
- Run: `SELECT COUNT(*) FROM employees e LEFT JOIN salary_levels sl ON sl.salary_id = e.salary_id WHERE sl.salary_id IS NULL` → must return 0

### 4. Query results validation
- `query_results.md` exists and contains results for all 6 queries
- Overall turnover rate ≈ 23.81%
- Low salary turnover rate ≈ 29.7%
- Avg satisfaction for leavers ≈ 0.440

### 5. Report validation
- `HR_Employee_Churn_Report.html` file size > 200 KB (confirms charts are embedded)
- `HR_Employee_Churn_Poster.html` file size > 80 KB

## Output

Print a checklist: PASS or FAIL for each check.
Print a final line: "Pipeline VALID ✓" or "Pipeline has issues — see above".
