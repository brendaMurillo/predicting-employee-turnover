# Predicting Employee Turnover

An end-to-end data analysis project exploring the factors that drive employee churn using a dataset of 14,999 HR records.

## Overview

This project investigates why employees leave a company and identifies high-risk employees still on the workforce. The analysis covers data cleaning, exploratory data analysis, statistical summaries, SQL querying, and visual reporting.

**Key finding:** The overall turnover rate is **23.81%**, with low-salary employees leaving at nearly 30% — more than 4x the rate of high-salary employees.

## Motivation

Employee turnover is one of the most costly and disruptive challenges organizations face. When a skilled employee leaves, the company absorbs the cost of recruiting, onboarding, and training a replacement — estimates commonly place this cost between 50% and 200% of the departing employee's annual salary. Beyond the financial impact, high turnover lowers team morale, disrupts institutional knowledge, and reduces overall productivity.

Despite these consequences, many organizations respond to turnover reactively — only investigating after employees have already resigned. This project takes a **proactive approach**: using historical HR data to identify the conditions most strongly associated with employees leaving, so that at-risk individuals can be flagged and supported before they make the decision to go.

The dataset of 14,999 employees captures a range of workplace factors — satisfaction level, performance evaluation scores, workload (number of projects and monthly hours), tenure, salary tier, promotion history, and workplace accidents. By analyzing patterns across these variables, we aim to answer:

- What factors most strongly predict whether an employee will leave?
- Do overworked or underpaid employees leave at higher rates?
- Can we identify current employees who are at high risk of churning?
- What actionable changes could reduce turnover in the most vulnerable groups?

## Research Plan

The analysis follows a structured pipeline:

1. **Data Loading & Exploration** — Load the raw dataset, inspect variable types, record counts, and distributions to understand the data landscape.
2. **Data Cleaning** — Identify and handle missing values, detect outliers, and validate data types to ensure analytical integrity.
3. **Descriptive Statistics** — Compute mean, median, standard deviation, quartiles, and percentiles across all numeric features, segmented by turnover status.
4. **Database Design & SQL Querying** — Normalize the flat CSV into a relational SQLite schema (four tables) and run targeted queries to surface turnover rates by salary tier, satisfaction trends, and high-risk employee profiles.
5. **Visualization** — Generate charts to illustrate the relationships between key features (satisfaction, hours worked, tenure) and the likelihood of an employee leaving.
6. **Risk Profiling** — Identify employees currently still at the company who match the high-risk profile (low satisfaction + low salary + no promotion in 5 years) to support early intervention.

## Project Files

| File | Description |
|---|---|
| `DataAnalysisProject (1).ipynb` | Main Jupyter notebook — full analysis pipeline |
| `HR_Employee_Churn_Report.html` | Rendered HTML report with charts and findings |
| `HR_Employee_Churn_Poster.pdf` | Research poster summarizing the project |
| `Data Analysis Paper (1).pdf` | Written paper with methodology and conclusions |
| `hr_churn.db` | SQLite database of the HR dataset |
| `query_results.md` | SQL query outputs — turnover rates, risk profiles |
| `database_schema_workflow.md` | Database schema and workflow documentation |

## Key Findings

- **Turnover rate by salary:** Low (29.7%) · Medium (20.4%) · High (6.6%)
- **Satisfaction level:** Employees who left averaged 0.44 vs. 0.67 for those who stayed
- **Overwork signal:** Employees who left worked ~8 more hours/month on average
- **615 high-risk employees** remain at the company (low satisfaction, low salary, no promotion)

## Tools & Technologies

- Python (pandas, matplotlib)
- SQLite
- Jupyter Notebook
- Claude Code (AI-assisted workflow)

## Author

Brenda Murillo — California State University, Bakersfield
