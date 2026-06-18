# /query — Run analytical queries and save results

Open `hr_churn.db` and run the key analytical queries from the Day-3 analysis. Save all results to `query_results.md`.

## Queries to run

1. **Overall turnover rate** — percentage of employees who left
2. **Turnover by salary category** — count, left count, and rate for low / medium / high
3. **Average satisfaction by turnover status** — stayed vs. left
4. **Average monthly hours by turnover status** — stayed vs. left
5. **Correlation proxy** — avg values of each numeric feature grouped by left_company (0 vs 1)
6. **High-risk employees** — still employed (left_company=0), satisfaction < 0.4, salary = low, no promotion

## Steps

1. Connect to `hr_churn.db` with `.headers on` and `.mode column`.
2. Run each query above and capture the output.
3. Write all results into `query_results.md` with a heading and table for each query.
4. Print a summary of how many rows each query returned.

## Expected output

- File: `query_results.md` with 6 labelled query result tables
- Console: query names and row counts
