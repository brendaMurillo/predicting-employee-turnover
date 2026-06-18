# HR Employee Churn Analysis — AI Vibe Coding Pipeline

**Author:** Brenda Murillo  
**Course:** Data Analytics Final Project  
**Institution:** California State University, Bakersfield  

---

## Project Overview

This project analyzes the HR Employee Churn dataset (14,999 employee records) to identify
the primary drivers of voluntary employee turnover. The pipeline was built using **Claude Code**
with AI-driven `/workflow` commands.

**Key finding:** Employee satisfaction level is the strongest predictor of turnover (r = −0.388).
Low-salary employees leave at 4.5× the rate of high-salary employees (29.7% vs. 6.6%).

---

## Pipeline

```
/crawl  →  hr_employee_churn_data.csv
/build  →  hr_churn.db  (normalized SQLite, 3NF)
/query  →  query_results.md
/report →  HR_Employee_Churn_Report.html + HR_Employee_Churn_Poster.html
/validate → pipeline check
```

---

## Workflow Commands

All commands live in `.claude/commands/` and run inside Claude Code with `/command-name`.

| Command | What it does |
|---|---|
| `/crawl` | Extracts CSV from zip, cleans missing values, saves `hr_employee_churn_data.csv` |
| `/build` | Creates normalized SQLite database `hr_churn.db` with 4 tables (3NF) |
| `/query` | Runs 6 analytical queries, saves results to `query_results.md` |
| `/report` | Generates charts + HTML report + HTML research poster |
| `/validate` | Checks all pipeline outputs for correctness |

---

## Database Schema (3NF)

```
salary_levels       employees              performance_records    employment_events
─────────────       ─────────────────      ───────────────────    ─────────────────
salary_id (PK)  ◄── salary_id (FK)         emp_id (PK/FK)         emp_id (PK/FK)
salary_label        emp_id (PK)            satisfaction_level      work_accident
                    time_spend_company     last_evaluation         promotion_last_5years
                                           number_project          left_company
                                           average_monthly_hours
```

---

## Key Results

| Metric | Value |
|---|---|
| Total employees | 14,999 |
| Overall turnover rate | 23.81% |
| Avg satisfaction — stayed | 0.667 |
| Avg satisfaction — left | 0.440 |
| Turnover rate — low salary | 29.7% |
| Turnover rate — high salary | 6.6% |
| Strongest predictor | satisfaction_level (r = −0.388) |

---

## Tools

- **Python** — pandas, matplotlib, sqlite3
- **Claude Code** — AI-driven workflow commands
- **SQLite** — normalized relational database
- **MCP servers** — fetch, fs, git, GitHub

---

## How to Run

```bash
# In Claude Code terminal
/crawl      # extract and clean the data
/build      # build the database
/query      # run analysis queries
/report     # generate HTML report and poster
/validate   # confirm everything is correct
```

---

*This research program is funded by the U.S. Department of Education, Title III Part F,
HSI-STEM program under award number P031C210093.*
