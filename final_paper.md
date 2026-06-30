# PREDICTING EMPLOYEE TURNOVER: A STATISTICAL ANALYSIS OF WORKFORCE ATTRITION FACTORS

**Brenda Murillo**
Dept. of Computer and Electrical Engineering and Computer Science
California State University, Bakersfield
Bakersfield, CA, USA
bmurillo3@csub.edu

---

> **Format note:** Paste into the [ACM SIG Proceedings template on Overleaf](https://www.overleaf.com/latex/templates/association-for-computing-machinery-acm-sig-proceedings-template/bmvfhcdnxfty) or the [ACM interim Word template](https://www.acm.org/publications/proceedings-template) for final two-column layout. Target: 6 body pages, US letter, ACM SIG proceedings format (SIGCSE Technical Symposium).

---

*Abstract*—Employee turnover represents one of the most persistent and costly challenges facing organizations today, yet most retention strategies rely on intuition rather than data. This paper presents a statistical analysis of workforce attrition using an HR dataset of 14,999 employee records drawn from Kaggle. We apply descriptive statistics, relational database querying (SQLite), correlation analysis, and visual analysis to identify the factors most strongly associated with employee departure. Our findings reveal an overall turnover rate of 23.81%, with low-salary employees leaving at nearly 30%—more than four times the rate of high-salary employees. Job satisfaction emerges as the single strongest predictor, with a Pearson correlation of −0.388 with turnover; employees who left averaged a satisfaction score of 0.44 compared to 0.67 for those who stayed. We further identify 615 current employees who match a high-risk churn profile (low satisfaction, low salary, no promotion in five years). These findings provide HR departments with actionable, data-driven criteria for early intervention and targeted retention strategies.

*CCS Concepts:* Applied computing → Decision analysis; Information systems → Data analytics; Social and professional topics → Employment issues.

*Index Terms*—employee turnover, workforce attrition, HR analytics, churn prediction, descriptive statistics, SQLite, data analysis

---

## I. INTRODUCTION

The cost of replacing an employee is widely estimated at between 50% and 200% of that employee's annual salary, accounting for recruiting, onboarding, lost productivity, and institutional knowledge transfer [2]. Yet despite this substantial burden, many organizations respond to turnover reactively—conducting exit interviews only after employees have already resigned and implementing changes too late to retain the individuals who prompted them.

The central challenge is one of prediction: given observable workplace factors, can an organization identify which employees are most likely to leave before they submit their resignation? This problem is well-suited to data-driven analysis. Modern HR systems routinely capture variables such as satisfaction surveys, performance evaluations, compensation tiers, workload metrics, and promotion histories—precisely the kinds of signals that may indicate attrition risk.

This paper addresses that challenge by applying statistical analysis to an HR dataset containing records for 14,999 employees. We pursue four core research questions:

1. How strongly does salary level predict employee turnover?
2. What is the relationship between job satisfaction and the likelihood of departure?
3. Does workload (measured in monthly hours and project count) influence turnover?
4. Can we identify current employees at high churn risk using observable characteristics?

Our approach is deliberately grounded in accessible statistical methods—descriptive statistics, group comparisons, correlation analysis, and SQL querying against a normalized relational database—rather than black-box machine learning models. This makes our findings interpretable and actionable for HR practitioners who may not have data science expertise.

The remainder of this paper is organized as follows. Section II reviews related work. Section III describes the dataset. Section IV details our methodology. Section V presents results. Section VI discusses implications. Section VII concludes with limitations and future directions.

---

## II. RELATED WORK

Employee attrition prediction has been an active area of research in both human resources management and data science. Early work by Mobley [1] established a foundational behavioral model of turnover, identifying job dissatisfaction as the primary precursor to resignation—a finding consistently replicated in subsequent literature. Griffeth, Hom, and Gaertner [2] later confirmed through meta-analysis that satisfaction, pay, and workload are the most reliable predictors of departure across industries and time periods.

More recent computational approaches have applied supervised machine learning to HR datasets. Punnoose and Ajit [5] applied random forests and logistic regression to the same Kaggle HR dataset used in this study, achieving classification accuracies above 97%. Similarly, Alduayj and Rajpoot [7] compared decision trees, support vector machines, and neural networks for attrition prediction, finding that tree-based models consistently outperformed others on HR tabular data. Zhao et al. [6] demonstrated that ensemble methods further improve predictive performance but at significant cost to interpretability.

While the predictive accuracy of machine learning models is high, a recognized limitation is interpretability [8]. HR managers need to understand *why* a model flags an employee as high-risk, not just that it does. This has led to growing interest in explainable AI applied to HR analytics, as well as in transparent statistical approaches that make the decision criteria visible.

Our work is positioned in this latter tradition. Rather than optimizing predictive accuracy, we prioritize interpretability: every finding in this paper can be expressed as a SQL query, a summary statistic, or a chart that any analyst can reproduce and explain to a non-technical stakeholder.

---

## III. DATASET

### A. *Source and Scope*

The dataset is the HR Employee Retention dataset publicly available on Kaggle [9], originally compiled to simulate realistic human resources records for analysis and learning purposes. It contains **14,999 employee records**, each representing a unique individual. The outcome variable (`left`) indicates whether the employee departed the organization (1) or remained (0).

### B. *Variables*

The dataset includes ten variables spanning four conceptual domains:

**TABLE I. DATASET VARIABLES**

| Domain | Variable | Type | Description |
|---|---|---|---|
| Satisfaction | `satisfaction_level` | Numeric [0,1] | Self-reported job satisfaction score |
| Performance | `last_evaluation` | Numeric [0,1] | Most recent performance review score |
| Workload | `number_project` | Integer | Number of projects assigned |
| Workload | `average_monthly_hours` | Integer | Average hours worked per month |
| Tenure | `time_spend_company` | Integer | Years employed at the company |
| Safety | `work_accident` | Boolean | Whether employee had a work accident |
| Career | `promotion_last_5years` | Boolean | Whether promoted in the last 5 years |
| Compensation | `salary` | Categorical | Salary tier: low, medium, or high |
| Outcome | `left` | Boolean | Whether the employee left the company |

### C. *Data Quality*

A missing value audit revealed no null entries in any column. Outlier detection using the interquartile range (IQR) method identified a small number of anomalous values in `average_monthly_hours` (values above 310 hours/month), which were retained as plausible extreme-workload cases rather than data errors. Schema constraints enforced data integrity: `CHECK` clauses validated that satisfaction and evaluation scores fall within [0,1], that hours and tenure are non-negative, and that foreign key relationships across all four tables are consistent. A row-count reconciliation confirmed that all 14,999 records are present and accounted for after normalization.

### D. *Database Schema*

To support efficient querying, the flat CSV was normalized into a four-table relational schema in SQLite [10]:

- `salary_levels` — lookup table mapping salary tier labels to IDs
- `employees` — core identity table (emp_id, salary_id, tenure)
- `performance_records` — satisfaction, evaluation, project count, monthly hours
- `employment_events` — work accidents, promotion history, and turnover outcome

This normalized design eliminates redundancy, enforces referential integrity via foreign keys, and allows the turnover outcome to be joined against any combination of employee attributes in a single SQL query.

---

## IV. METHODOLOGY

### A. *Descriptive Statistics*

For all numeric variables, we computed mean, median, mode, standard deviation, variance, range, quartiles (Q1, Q3), and the interquartile range. These statistics were calculated separately for employees who left and those who stayed, enabling direct comparison of distributional differences across turnover groups.

### B. *Group Comparison*

Turnover rates were computed for each level of the categorical variables (salary tier, promotion status, work accident occurrence). For numeric variables, we segmented employees into bins (e.g., workload quintiles, satisfaction deciles) and computed turnover rates within each bin to identify non-linear relationships.

### C. *Correlation Analysis*

Pearson correlation coefficients were computed between each numeric feature and the binary `left` outcome. This produced a ranked list of predictors by association strength, allowing us to quantify which variables are most and least related to departure.

### D. *SQL-Based Analysis*

All group-level queries were executed against the normalized SQLite database. Key queries included:

- Overall turnover rate (`COUNT` with `GROUP BY left_company`)
- Turnover rate by salary tier (three-table join across `employees`, `salary_levels`, `employment_events`)
- Average satisfaction and monthly hours by turnover status
- High-risk employee identification using compound `WHERE` filters

### E. *Risk Profiling*

A high-risk employee profile was defined using three criteria simultaneously: satisfaction score below 0.4, salary tier of "low", and no promotion in the last five years, with the additional constraint that the employee has not yet left (i.e., they are still at the company and potentially retainable). This threshold was set based on the distributional boundary at which turnover rates were observed to increase sharply in the satisfaction analysis.

### F. *Visualization*

Four chart types were produced to support interpretation: a bar chart of turnover rates by salary tier; a grouped bar chart comparing average satisfaction and hours by turnover status; a scatter plot of satisfaction versus last evaluation colored by turnover outcome; and a workload distribution chart showing hours worked across turnover groups.

---

## V. RESULTS

### A. *Overall Turnover Rate*

Of 14,999 employees in the dataset, 3,571 left the organization, yielding an **overall turnover rate of 23.81%**. This is substantially higher than the commonly cited U.S. industry average of approximately 15% [4], underscoring the severity of the attrition problem represented in the data.

### B. *Turnover by Salary Tier*

Salary tier is one of the strongest single-variable predictors of turnover. Table II shows the turnover rates disaggregated by compensation group.

**TABLE II. TURNOVER RATE BY SALARY TIER**

| Salary Tier | Total Employees | Left | Turnover Rate |
|---|---|---|---|
| Low | 7,316 | 2,172 | **29.69%** |
| Medium | 6,446 | 1,317 | 20.43% |
| High | 1,237 | 82 | **6.63%** |

The gap between low and high salary tiers is striking: low-salary employees leave at more than **four times the rate** of high-salary employees. This pattern is consistent with compensation-based push factors identified in the organizational behavior literature [1][2].

### C. *Job Satisfaction and Turnover*

Job satisfaction shows the most pronounced difference between retained and departed employees across all variables examined (Table III). It also produces the strongest Pearson correlation with turnover outcome (*r* = −0.388), meaning lower satisfaction is strongly associated with departure.

**TABLE III. AVERAGE FEATURE VALUES BY TURNOVER STATUS**

| Feature | Stayed (left = 0) | Left (left = 1) |
|---|---|---|
| Satisfaction level | **0.667** | **0.440** |
| Last evaluation score | 0.715 | 0.718 |
| Number of projects | 3.79 | 3.86 |
| Average monthly hours | 199.1 | 207.4 |
| Years at company | 3.38 | 3.88 |

Satisfaction level differs by 0.227 points between the two groups—a gap of approximately 34% relative to the stayed group's mean. By contrast, performance evaluation scores are nearly identical (0.715 vs. 0.718), indicating that employees who left were not lower performers. This is a critical finding: turnover is not a performance problem but a satisfaction and compensation problem.

### D. *Feature Correlation Analysis*

Table IV presents the Pearson correlation of each feature with the `left` outcome, ranked by absolute magnitude.

**TABLE IV. FEATURE CORRELATION WITH TURNOVER (left = 1)**

| Feature | Pearson *r* |
|---|---|
| `satisfaction_level` | −0.388 |
| `time_spend_company` | +0.145 |
| `work_accident` | −0.155 |
| `average_monthly_hours` | +0.071 |
| `number_project` | +0.024 |
| `promotion_last_5years` | −0.062 |
| `last_evaluation` | +0.007 |

Satisfaction is the strongest single predictor by a wide margin. Notably, `last_evaluation` shows virtually no correlation with turnover (*r* = +0.007), confirming that performance evaluation alone does not distinguish leavers from stayers.

### E. *Workload and Turnover*

Employees who left worked an average of **207.4 hours per month**, compared to 199.1 for those who stayed—a difference of 8.3 hours, or roughly two extra workdays per month. While this gap is modest in absolute terms, it is consistent across the dataset and aligns with burnout-driven attrition patterns described in [3].

Project count shows a similarly small but consistent difference (3.86 vs. 3.79 projects on average). The correlation of `average_monthly_hours` with turnover (*r* = +0.071) suggests overwork is a contributing factor, though it acts more as a compounding stressor alongside low satisfaction and low pay than as an independent primary driver.

### F. *High-Risk Employee Profiling*

Applying the compound risk profile (satisfaction < 0.4, salary = low, no promotion in 5 years, still employed), the analysis identified **615 current employees** who match all three criteria. Table V shows a sample of the highest-risk individuals.

**TABLE V. SAMPLE HIGH-RISK EMPLOYEES (TOP 10 BY LOWEST SATISFACTION)**

| Employee ID | Satisfaction | Monthly Hours | Tenure (yrs) |
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

Several of these employees are working well above average monthly hours (257, 276, 287) despite reporting the minimum satisfaction score in the dataset. Without intervention, these individuals represent significant flight risks.

---

## VI. DISCUSSION

### A. *Compensation is the Dominant Structural Factor*

The four-to-one ratio in turnover rates between low and high salary tiers is the single most actionable finding in this study. It suggests that compensation structure, rather than individual employee characteristics, creates a systemic attrition risk that cannot be resolved through engagement programs or managerial coaching alone. Organizations with large proportions of low-salary employees should treat compensation review as a retention strategy, consistent with recommendations in [2].

### B. *Satisfaction Predicts Turnover Independently of Performance*

The near-identical evaluation scores between employees who left and those who stayed (0.718 vs. 0.715), combined with the correlation data showing `last_evaluation` is essentially unrelated to turnover (*r* = +0.007), challenges a common managerial assumption: that turnover is driven by underperformers seeking to avoid accountability. The data shows the opposite—employees who left were equally well-evaluated as those who stayed. Their departure was driven by dissatisfaction, not performance gaps. This finding replicates the foundational result in [1] and underscores that retention efforts should be framed as a satisfaction and engagement problem, not a performance management problem.

### C. *Workload Acts as a Compounding Risk Factor*

The workload difference (8.3 hours/month) is statistically modest but directionally consistent. More importantly, the highest-risk employees in the profiling analysis are concentrated among individuals who combine low satisfaction with above-average hours—suggesting that overwork amplifies the effect of low satisfaction rather than driving attrition independently. HR interventions should therefore target the intersection of these factors, not either factor in isolation. This is consistent with burnout models described in [3].

### D. *Early Intervention Opportunity*

The identification of 615 high-risk current employees is perhaps the most practically valuable output of this analysis. Unlike post-departure analyses, this profiling approach is actionable before attrition occurs. HR departments can use these criteria—operationalized as a simple SQL query—to generate a prioritized list for manager outreach, salary review, or promotion consideration on a recurring basis. This moves HR analytics from retrospective reporting to prospective intervention.

### E. *Limitations*

This study has several limitations. First, the dataset is simulated [9] and does not represent a specific organization or industry, which limits the generalizability of specific threshold values (e.g., the 0.4 satisfaction cutoff). Second, our analysis is descriptive rather than causal: we identify associations between variables and turnover, but cannot claim that low salary *causes* departure in a counterfactual sense. Third, the dataset lacks department or role information, which likely moderates many of the relationships observed. Fourth, class imbalance (approximately 24% leavers) should be addressed before extending this framework to predictive modeling.

---

## VII. CONCLUSION

This paper analyzed an HR dataset of 14,999 employees to identify the factors most strongly associated with workforce attrition. Our findings establish that salary tier and job satisfaction are the two dominant predictors of turnover—with satisfaction producing the strongest correlation (*r* = −0.388)—while performance evaluation is essentially uncorrelated with departure. Critically, departed employees were equally well-evaluated as retained employees, confirming that turnover is a satisfaction problem, not a performance problem.

By normalizing a flat HR CSV into a constraint-validated SQLite schema and operationalizing findings as reusable SQL queries, we demonstrate that organizations can use straightforward data engineering and group-level analysis to generate actionable, prioritized intervention lists from existing HR data without requiring machine learning infrastructure. The 615 high-risk employees identified in this dataset represent an immediately addressable retention opportunity.

Future work should apply this framework to real organizational data with department-level granularity, incorporate time-series analysis to model attrition risk as it evolves over an employee's tenure, and explore causal inference methods (e.g., propensity score matching) to move beyond association toward actionable causal claims about the effect of salary increases or promotion on retention probability. Adding predictive modeling with proper class-imbalance handling would further extend this framework from descriptive to prospective analytics.

---

## ACKNOWLEDGMENT

The author thanks the faculty of the Department of Computer and Electrical Engineering and Computer Science at California State University, Bakersfield for guidance on this project.

---

## REFERENCES

[1] W. H. Mobley, "Intermediate linkages in the relationship between job satisfaction and employee turnover," *J. Appl. Psychol.*, vol. 62, no. 2, pp. 237–240, 1977.

[2] R. W. Griffeth, P. W. Hom, and S. Gaertner, "A meta-analysis of antecedents and correlates of employee turnover: Update, moderator tests, and research implications for the next millennium," *J. Manag.*, vol. 26, no. 3, pp. 463–488, 2000.

[3] P. W. Hom, T. W. Lee, J. D. Shaw, and J. P. Hausknecht, "One hundred years of employee turnover theory and research," *J. Appl. Psychol.*, vol. 102, no. 3, pp. 530–545, 2017.

[4] Bureau of Labor Statistics, "Job Openings and Labor Turnover Summary," U.S. Department of Labor, 2023. [Online]. Available: https://www.bls.gov/news.release/jolts.nr0.htm

[5] R. Punnoose and P. Ajit, "Prediction of employee turnover in organizations using machine learning algorithms," *Int. J. Adv. Res. Artif. Intell.*, vol. 5, no. 9, pp. 22–26, 2016.

[6] Y. Zhao, M. K. Hryniewicki, F. Cheng, B. Fu, and X. Zhu, "Employee turnover prediction with machine learning: A reliable approach," in *Proc. Intelligent Systems Conf. (IntelliSys)*, 2018, pp. 737–758.

[7] S. S. Alduayj and K. Rajpoot, "Predicting employee attrition using machine learning," in *Proc. Int. Conf. Innovations in Information Technology (IIT)*, 2018, pp. 93–98.

[8] F. Doshi-Velez and B. Kim, "Towards a rigorous science of interpretable machine learning," *arXiv preprint arXiv:1702.08608*, 2017.

[9] HR Analytics / Employee Retention Dataset, Kaggle. [Online]. Available: https://www.kaggle.com/

[10] E. F. Codd, "A relational model of data for large shared data banks," *Commun. ACM*, vol. 13, no. 6, pp. 377–387, 1970.
