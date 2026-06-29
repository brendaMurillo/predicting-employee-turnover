# Predicting Employee Turnover

An end-to-end data analysis project exploring the factors that drive employee churn using a dataset of 14,999 HR records.

## Overview

This project investigates why employees leave a company and identifies high-risk employees still on the workforce. The analysis covers data cleaning, exploratory data analysis, statistical summaries, SQL querying, and visual reporting.

**Key finding:** The overall turnover rate is **23.81%**, with low-salary employees leaving at nearly 30% — more than 4x the rate of high-salary employees.

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
