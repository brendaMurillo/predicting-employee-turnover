# /report — Generate the HTML analysis report and research poster

Using the data in `hr_churn.db` and the findings in `query_results.md`, regenerate the full HTML report and research poster.

## Steps

1. Read query results from `hr_churn.db` (run the key queries fresh).
2. Generate 4 matplotlib charts and save as `chart1.png` through `chart4.png`:
   - chart1: Average satisfaction level — stayed vs. left (bar chart)
   - chart2: Turnover rate by salary category (bar chart)
   - chart3: Feature correlations with turnover (horizontal bar chart)
   - chart4: Overall turnover distribution (pie chart)
3. Embed all charts as base64 into the HTML files (no external dependencies).
4. Write `HR_Employee_Churn_Report.html` — full academic paper with:
   - Abstract, Introduction, Dataset Description, Methods, Results, Conclusion, References
5. Write `HR_Employee_Churn_Poster.html` — 3-column research poster at 48×36 inch proportions with:
   - CSUB logo from `image.png`
   - DOE Title III disclaimer in the footer
   - Key stats, charts, findings, conclusion, references

## Expected output

- `chart1.png` through `chart4.png`
- `HR_Employee_Churn_Report.html`
- `HR_Employee_Churn_Poster.html`
