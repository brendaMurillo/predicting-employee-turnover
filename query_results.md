# Query Results — HR Employee Churn Analysis

## 1. Overall Turnover Rate

| Metric | Value |
|---|---|
| Total employees | 14,999 |
| Employees who left | 3,571 |
| Turnover rate | 23.81% |

## 2. Turnover Rate by Salary Category

| Salary | Total | Left | Turnover Rate |
|---|---|---|---|
| low | 7,316 | 2,172 | 29.69% |
| medium | 6,446 | 1,317 | 20.43% |
| high | 1,237 | 82 | 6.63% |

## 3. Average Satisfaction by Turnover Status

| Status | Avg Satisfaction Level |
|---|---|
| Stayed | 0.667 |
| Left | 0.44 |

## 4. Average Monthly Hours by Turnover Status

| Status | Avg Monthly Hours |
|---|---|
| Stayed | 199.1 |
| Left | 207.4 |

## 5. Average Feature Values by Turnover Status

| Feature | Stayed (left=0) | Left (left=1) |
|---|---|---|
| satisfaction_level | 0.667 | 0.44 |
| last_evaluation | 0.715 | 0.718 |
| number_project | 3.79 | 3.86 |
| avg_monthly_hours | 199.1 | 207.4 |
| time_spend_company | 3.38 | 3.88 |

## 6. High-Risk Employees (Still Employed)

Criteria: satisfaction < 0.4, salary = low, no promotion, still at company

| emp_id | Satisfaction | Monthly Hours | Tenure (yrs) |
|---|---|---|---|
| 2087 | 0.12 | 244 | 5 |
| 3129 | 0.12 | 257 | 6 |
| 4026 | 0.12 | 241 | 2 |
| 4684 | 0.12 | 276 | 4 |
| 5336 | 0.12 | 166 | 3 |
| 7772 | 0.12 | 161 | 4 |
| 8745 | 0.12 | 287 | 4 |
| 9283 | 0.12 | 200 | 3 |
| 11069 | 0.12 | 191 | 5 |
| 13280 | 0.12 | 191 | 5 |

*Showing top 10 of 615 high-risk employees still at the company.*
