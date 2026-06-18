# /crawl — Extract and prepare the HR Employee Churn dataset

Extract the raw HR Employee Churn data from `archive (4).zip` and save it as a clean, standalone CSV file called `hr_employee_churn_data.csv` in the project root.

## Steps

1. Unzip `archive (4).zip` and read `hr_employee_churn_data.csv` using pandas.
2. Impute the 2 missing values in `satisfaction_level` with the column mean.
3. Rename `average_montly_hours` → `average_monthly_hours` (fix the typo).
4. Save the cleaned dataframe to `hr_employee_churn_data.csv` in the project root.
5. Print a summary: number of rows, columns, missing values remaining, and first 5 rows.

## Expected output

- File: `hr_employee_churn_data.csv` (14,999 rows × 10 columns)
- Console: row count, column names, zero missing values confirmed
