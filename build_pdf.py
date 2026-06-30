"""
Generates final_paper.pdf in IEEE two-column conference format.
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer,
    Table, TableStyle, KeepTogether
)
from reportlab.lib import colors
from reportlab.lib.colors import black

# ── Page geometry ─────────────────────────────────────────────────────────────
PW, PH      = letter                  # 612 x 792 pts
LMARGIN     = 0.75 * inch
RMARGIN     = 0.75 * inch
TMARGIN     = 1.00 * inch
BMARGIN     = 1.00 * inch
GUTTER      = 0.25 * inch
USABLE_W    = PW - LMARGIN - RMARGIN
COL_W       = (USABLE_W - GUTTER) / 2
COL_H       = PH - TMARGIN - BMARGIN

# ── Styles ────────────────────────────────────────────────────────────────────
SERIF = "Times-Roman"
SERIF_B = "Times-Bold"
SERIF_BI = "Times-BoldItalic"
SERIF_I = "Times-Italic"

def sty(name, **kw):
    defaults = dict(fontName=SERIF, fontSize=10, leading=12,
                    spaceAfter=4, textColor=black)
    defaults.update(kw)
    return ParagraphStyle(name, **defaults)

S = {
    "title":   sty("title",  fontName=SERIF_B, fontSize=16, leading=20,
                   alignment=TA_CENTER, spaceAfter=8),
    "author":  sty("author", fontSize=11, alignment=TA_CENTER,
                   fontName=SERIF_B, spaceAfter=2),
    "affil":   sty("affil",  fontSize=10, alignment=TA_CENTER,
                   fontName=SERIF_I, spaceAfter=2),
    "email":   sty("email",  fontSize=10, alignment=TA_CENTER, spaceAfter=10),
    "abstract":sty("abstract", fontSize=9, leading=11,
                   alignment=TA_JUSTIFY, spaceAfter=4),
    "sec":     sty("sec",    fontName=SERIF_B, fontSize=10, leading=12,
                   alignment=TA_CENTER, spaceBefore=8, spaceAfter=4),
    "subsec":  sty("subsec", fontName=SERIF_I, fontSize=10, leading=12,
                   alignment=TA_LEFT, spaceBefore=4, spaceAfter=2),
    "body":    sty("body",   fontSize=10, leading=12,
                   alignment=TA_JUSTIFY, firstLineIndent=0.15*inch,
                   spaceAfter=4),
    "body_ni": sty("body_ni", fontSize=10, leading=12,
                   alignment=TA_JUSTIFY, spaceAfter=4),
    "ref":     sty("ref",    fontSize=9, leading=11,
                   alignment=TA_JUSTIFY, leftIndent=0.18*inch,
                   firstLineIndent=-0.18*inch, spaceAfter=2),
    "tcap":    sty("tcap",   fontName=SERIF_B, fontSize=9, leading=11,
                   alignment=TA_CENTER, spaceAfter=2, spaceBefore=6),
    "enum":    sty("enum",   fontSize=10, leading=12,
                   alignment=TA_JUSTIFY, leftIndent=0.2*inch,
                   spaceAfter=2),
}

# ── Cell paragraph style (for wrapping inside table cells) ───────────────────
CS  = ParagraphStyle("cell",  fontName=SERIF,   fontSize=9, leading=11)
CSB = ParagraphStyle("cellb", fontName=SERIF_B, fontSize=9, leading=11)

def cell(text, bold=False):
    return Paragraph(text, CSB if bold else CS)

def trow(vals, bold=False):
    return [cell(v, bold) for v in vals]

# ── Table style ───────────────────────────────────────────────────────────────
def tstyle(header_rows=1):
    cmds = [
        ('VALIGN',    (0,0), (-1,-1), 'TOP'),
        ('GRID',      (0,0), (-1,-1), 0.5, colors.black),
        ('LINEBELOW', (0,0), (-1, header_rows-1), 1.0, colors.black),
        ('TOPPADDING',(0,0), (-1,-1), 3),
        ('BOTTOMPADDING',(0,0),(-1,-1), 3),
        ('LEFTPADDING', (0,0),(-1,-1), 4),
        ('RIGHTPADDING',(0,0),(-1,-1), 4),
    ]
    return TableStyle(cmds)

# ── Page template: one wide frame for title block, then two columns ────────────
def make_doc(filename):
    doc = BaseDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=LMARGIN, rightMargin=RMARGIN,
        topMargin=TMARGIN,  bottomMargin=BMARGIN,
    )

    # Frame 1: full-width title block (top ~2.5 inches)
    title_frame = Frame(
        LMARGIN, PH - TMARGIN - 2.5*inch,
        USABLE_W, 2.5*inch,
        leftPadding=0, rightPadding=0,
        topPadding=0,  bottomPadding=0,
        id='title'
    )
    # Frame 2: left column
    left_frame = Frame(
        LMARGIN, BMARGIN,
        COL_W, PH - TMARGIN - BMARGIN - 2.5*inch,
        leftPadding=0, rightPadding=4,
        topPadding=0,  bottomPadding=0,
        id='left'
    )
    # Frame 3: right column
    right_frame = Frame(
        LMARGIN + COL_W + GUTTER, BMARGIN,
        COL_W, PH - TMARGIN - BMARGIN - 2.5*inch,
        leftPadding=4, rightPadding=0,
        topPadding=0,  bottomPadding=0,
        id='right'
    )

    # Subsequent pages: full two-column (no title block)
    left2 = Frame(
        LMARGIN, BMARGIN,
        COL_W, COL_H,
        leftPadding=0, rightPadding=4,
        topPadding=0,  bottomPadding=0,
        id='left2'
    )
    right2 = Frame(
        LMARGIN + COL_W + GUTTER, BMARGIN,
        COL_W, COL_H,
        leftPadding=4, rightPadding=0,
        topPadding=0,  bottomPadding=0,
        id='right2'
    )

    doc.addPageTemplates([
        PageTemplate(id='First', frames=[title_frame, left_frame, right_frame]),
        PageTemplate(id='Later', frames=[left2, right2]),
    ])
    return doc

# ── Content helpers ───────────────────────────────────────────────────────────
def sec(num, title):
    return Paragraph(f"{num}.&nbsp;&nbsp;{title.upper()}", S["sec"])

def subsec(letter, title):
    return Paragraph(f"<i>{letter}.&nbsp;&nbsp;{title}</i>", S["subsec"])

def body(text):
    return Paragraph(text, S["body"])

def body_ni(text):
    return Paragraph(text, S["body_ni"])

def sp(h=4):
    return Spacer(1, h)

TCAP_KWN = ParagraphStyle(
    "tcap_kwn", parent=S["tcap"], keepWithNext=True
)

def make_table(caption, data, col_widths, header_rows=1):
    t = Table(data, colWidths=col_widths, repeatRows=header_rows)
    t.setStyle(tstyle(header_rows))
    cap = Paragraph(caption, TCAP_KWN)
    return [cap, t, Spacer(1, 6)]

# ── Build story ───────────────────────────────────────────────────────────────
def build():
    story = []

    # ── Title block ──────────────────────────────────────────────────────────
    story.append(Paragraph(
        "Predicting Employee Turnover: A Statistical Analysis<br/>"
        "of Workforce Attrition Factors",
        S["title"]
    ))
    story.append(Paragraph(
        "Brenda Murillo &nbsp;&nbsp;&nbsp;&nbsp; Lucinda Pina",
        S["author"]
    ))
    story.append(Paragraph(
        "Dept. of Computer and Electrical Engineering and Computer Science",
        S["affil"]
    ))
    story.append(Paragraph(
        "California State University, Bakersfield — Bakersfield, CA, USA",
        S["affil"]
    ))
    story.append(Paragraph("bmurillo3@csub.edu", S["email"]))

    # ── Abstract & Index Terms (full-width, before columns) ──────────────────
    story.append(Paragraph(
        "<b><i>Abstract</i>—</b>"
        "<b>Employee turnover represents one of the most persistent and costly "
        "challenges facing organizations today, yet most retention strategies rely "
        "on intuition rather than data. This paper presents a statistical analysis "
        "of workforce attrition using an HR dataset of 14,999 employee records drawn "
        "from Kaggle. We apply descriptive statistics, relational database querying "
        "(SQLite), correlation analysis, and visual analysis to identify the factors "
        "most strongly associated with employee departure. Our findings reveal an "
        "overall turnover rate of 23.81%, with low-salary employees leaving at nearly "
        "30%—more than four times the rate of high-salary employees. Job satisfaction "
        "emerges as the single strongest predictor (r = −0.388); employees who left "
        "averaged a satisfaction score of 0.44 compared to 0.67 for those who stayed. "
        "We further identify 615 current employees who match a high-risk churn profile. "
        "These findings provide HR departments with actionable, data-driven criteria "
        "for early intervention and targeted retention strategies.</b>",
        S["abstract"]
    ))
    story.append(Paragraph(
        "<b><i>Index Terms</i>—employee turnover, workforce attrition, HR analytics, "
        "churn prediction, descriptive statistics, SQLite, data analysis</b>",
        S["abstract"]
    ))
    story.append(sp(6))

    # ── I. INTRODUCTION ───────────────────────────────────────────────────────
    story.append(sec("I", "Introduction"))
    story.append(body(
        "The cost of replacing an employee is widely estimated at between 50% and "
        "200% of that employee's annual salary, accounting for recruiting, onboarding, "
        "lost productivity, and institutional knowledge transfer [2]. Yet despite this "
        "substantial burden, many organizations respond to turnover reactively—conducting "
        "exit interviews only after employees have already resigned, and implementing "
        "changes too late to retain the individuals who prompted them."
    ))
    story.append(body(
        "The central challenge is one of prediction: given observable workplace factors, "
        "can an organization identify which employees are most likely to leave before they "
        "submit their resignation? Modern HR systems routinely capture variables such as "
        "satisfaction surveys, performance evaluations, compensation tiers, workload "
        "metrics, and promotion histories—precisely the kinds of signals that may indicate "
        "attrition risk."
    ))
    story.append(body(
        "This paper addresses that challenge using a dataset of 14,999 employee records. "
        "We pursue four research questions: (1) How strongly does salary level predict "
        "turnover? (2) What is the relationship between satisfaction and departure? "
        "(3) Does workload influence turnover? (4) Can we identify high-risk employees "
        "using observable characteristics?"
    ))
    story.append(body(
        "Our approach is grounded in accessible statistical methods—descriptive "
        "statistics, group comparisons, correlation analysis, and SQL querying against "
        "a normalized relational database—rather than black-box machine learning models, "
        "making findings interpretable and actionable for HR practitioners."
    ))

    # ── II. RELATED WORK ──────────────────────────────────────────────────────
    story.append(sec("II", "Related Work"))
    story.append(body(
        "Early work by Mobley [1] established a foundational behavioral model of "
        "turnover, identifying job dissatisfaction as the primary precursor to "
        "resignation. Griffeth, Hom, and Gaertner [2] confirmed through meta-analysis "
        "that satisfaction, pay, and workload are the most reliable predictors of "
        "departure across industries and time periods."
    ))
    story.append(body(
        "More recent computational approaches have applied supervised machine learning "
        "to HR datasets. Punnoose and Ajit [5] applied random forests and logistic "
        "regression to the same Kaggle HR dataset, achieving accuracies above 97%. "
        "Alduayj and Rajpoot [7] compared decision trees, SVMs, and neural networks, "
        "finding tree-based models consistently outperformed others on HR tabular data. "
        "Zhao et al. [6] demonstrated ensemble methods improve performance but at "
        "significant cost to interpretability [8]."
    ))
    story.append(body(
        "Our work prioritizes interpretability over predictive accuracy: every finding "
        "can be expressed as a SQL query, a summary statistic, or a chart that any "
        "analyst can reproduce and explain to a non-technical stakeholder."
    ))

    # ── III. DATASET ──────────────────────────────────────────────────────────
    story.append(sec("III", "Dataset"))
    story.append(subsec("A", "Source and Scope"))
    story.append(body(
        "The dataset is the HR Employee Retention dataset from Kaggle [9], containing "
        "14,999 employee records. The outcome variable (<i>left</i>) indicates whether "
        "the employee departed (1) or remained (0)."
    ))

    story.append(subsec("B", "Variables"))
    story.append(body_ni("The dataset includes ten variables across four domains (Table I)."))
    story.append(sp(4))

    # TABLE I
    cw1 = [COL_W * f for f in [0.27, 0.38, 0.18, 0.17]]
    t1_data = [
        trow(["Domain", "Variable", "Type", "Descr."], bold=True),
        trow(["Satisfaction",  "satisfaction_level",    "Num [0,1]", "Job satisfaction"]),
        trow(["Performance",   "last_evaluation",        "Num [0,1]", "Perf. review"]),
        trow(["Workload",      "number_project",          "Integer",   "Projects"]),
        trow(["Workload",      "avg_monthly_hrs",         "Integer",   "Avg. hrs/mo"]),
        trow(["Tenure",        "time_spend_company",      "Integer",   "Yrs at company"]),
        trow(["Safety",        "work_accident",           "Boolean",   "Work accident"]),
        trow(["Career",        "promotion_last_5yrs",     "Boolean",   "Promoted 5 yrs"]),
        trow(["Compensation",  "salary",                  "Category",  "Lo/med/hi"]),
        trow(["Outcome",       "left",                    "Boolean",   "Left company"]),
    ]
    story.extend(make_table("TABLE I.&nbsp;&nbsp;&nbsp;DATASET VARIABLES", t1_data, cw1))

    story.append(subsec("C", "Data Quality"))
    story.append(body(
        "A missing value audit revealed no null entries. Outlier detection using the "
        "IQR method identified anomalous values in avg_monthly_hours (above 310/month), "
        "retained as plausible extreme-workload cases. Schema CHECK constraints validated "
        "satisfaction and evaluation scores within [0,1], non-negative hours and tenure, "
        "and foreign key consistency across all four tables."
    ))

    story.append(subsec("D", "Database Schema"))
    story.append(body(
        "The flat CSV was normalized into a four-table SQLite schema [10]: "
        "(1) <i>salary_levels</i>—lookup table; "
        "(2) <i>employees</i>—core identity table; "
        "(3) <i>performance_records</i>—satisfaction, evaluation, hours; "
        "(4) <i>employment_events</i>—accidents, promotions, turnover outcome. "
        "This eliminates redundancy, enforces referential integrity, and allows the "
        "turnover outcome to be joined against any attribute combination in a single query."
    ))

    # ── IV. METHODOLOGY ───────────────────────────────────────────────────────
    story.append(sec("IV", "Methodology"))
    story.append(subsec("A", "Descriptive Statistics"))
    story.append(body(
        "For all numeric variables we computed mean, median, standard deviation, "
        "variance, range, Q1, Q3, and IQR, calculated separately for employees "
        "who left and those who stayed."
    ))
    story.append(subsec("B", "Group Comparison"))
    story.append(body(
        "Turnover rates were computed for each level of categorical variables "
        "(salary tier, promotion status, work accident). Numeric variables were "
        "segmented into bins to identify non-linear patterns."
    ))
    story.append(subsec("C", "Correlation Analysis"))
    story.append(body(
        "Pearson correlation coefficients were computed between each numeric feature "
        "and the binary <i>left</i> outcome, producing a ranked list of predictors "
        "by association strength."
    ))
    story.append(subsec("D", "SQL-Based Analysis"))
    story.append(body(
        "All group-level queries were executed against the normalized SQLite database: "
        "overall turnover rate, turnover by salary tier (three-table join), average "
        "satisfaction and monthly hours by turnover status, and high-risk identification "
        "using compound WHERE filters."
    ))
    story.append(subsec("E", "Risk Profiling"))
    story.append(body(
        "A high-risk profile was defined using three simultaneous criteria: satisfaction "
        "below 0.4, salary tier 'low', and no promotion in the last five years, "
        "constrained to employees still at the company."
    ))

    # ── V. RESULTS ────────────────────────────────────────────────────────────
    story.append(sec("V", "Results"))
    story.append(subsec("A", "Overall Turnover Rate"))
    story.append(body(
        "Of 14,999 employees, 3,571 left, yielding an overall turnover rate of "
        "<b>23.81%</b>—substantially higher than the U.S. industry average of "
        "approximately 15% [4]."
    ))

    story.append(subsec("B", "Turnover by Salary Tier"))
    story.append(body_ni("Table II shows low-salary employees leave at over four times the rate of high-salary employees."))
    story.append(sp(4))
    cw2 = [COL_W * f for f in [0.26, 0.26, 0.22, 0.26]]
    t2_data = [
        trow(["Salary Tier", "Total", "Left", "Rate"], bold=True),
        trow(["Low",    "7,316", "2,172", "29.69%"]),
        trow(["Medium", "6,446", "1,317", "20.43%"]),
        trow(["High",   "1,237",    "82",  "6.63%"]),
    ]
    story.extend(make_table("TABLE II.&nbsp;&nbsp;&nbsp;TURNOVER RATE BY SALARY TIER", t2_data, cw2))

    story.append(subsec("C", "Job Satisfaction and Turnover"))
    story.append(body(
        "Job satisfaction shows the most pronounced difference between retained and "
        "departed employees (Table III) and produces the strongest Pearson correlation "
        "with turnover (r = −0.388). Satisfaction differs by 0.227 points—a 34% "
        "relative gap. By contrast, evaluation scores are nearly identical "
        "(0.715 vs. 0.718), confirming turnover is a satisfaction problem, "
        "not a performance problem."
    ))
    story.append(sp(4))
    cw3 = [COL_W * f for f in [0.48, 0.26, 0.26]]
    t3_data = [
        trow(["Feature", "Stayed", "Left"], bold=True),
        trow(["Satisfaction level",   "0.667", "0.440"]),
        trow(["Last evaluation",      "0.715", "0.718"]),
        trow(["Number of projects",   "3.79",  "3.86"]),
        trow(["Avg. monthly hours",   "199.1", "207.4"]),
        trow(["Years at company",     "3.38",  "3.88"]),
    ]
    story.extend(make_table("TABLE III.&nbsp;&nbsp;&nbsp;AVERAGE FEATURE VALUES BY TURNOVER STATUS", t3_data, cw3))

    story.append(subsec("D", "Feature Correlation Analysis"))
    story.append(body_ni("Table IV ranks each feature by its Pearson correlation with the <i>left</i> outcome."))
    story.append(sp(4))
    cw4 = [COL_W * 0.68, COL_W * 0.32]
    t4_data = [
        trow(["Feature", "Pearson r"], bold=True),
        trow(["satisfaction_level",     "−0.388"]),
        trow(["work_accident",          "−0.155"]),
        trow(["time_spend_company",     "+0.145"]),
        trow(["avg_monthly_hours",      "+0.071"]),
        trow(["promotion_last_5years",  "−0.062"]),
        trow(["number_project",         "+0.024"]),
        trow(["last_evaluation",        "+0.007"]),
    ]
    story.extend(make_table("TABLE IV.&nbsp;&nbsp;&nbsp;FEATURE CORRELATION WITH TURNOVER", t4_data, cw4))

    story.append(subsec("E", "Workload and Turnover"))
    story.append(body(
        "Employees who left worked an average of 207.4 hours/month compared to "
        "199.1 for those who stayed—8.3 extra hours, or roughly two additional "
        "workdays per month. The correlation of avg_monthly_hours with turnover "
        "(r = +0.071) suggests overwork is a contributing factor, acting as a "
        "compounding stressor alongside low satisfaction and low pay."
    ))

    story.append(subsec("F", "High-Risk Employee Profiling"))
    story.append(body_ni("Applying the compound risk profile identified <b>615 current employees</b> matching all three criteria (Table V)."))
    story.append(sp(4))
    cw5 = [COL_W * f for f in [0.24, 0.26, 0.24, 0.26]]
    t5_data = [
        trow(["Emp. ID", "Satisfaction", "Hrs/Mo", "Tenure"], bold=True),
        trow(["2087",  "0.12", "244", "5 yrs"]),
        trow(["3129",  "0.12", "257", "6 yrs"]),
        trow(["4026",  "0.12", "241", "2 yrs"]),
        trow(["4684",  "0.12", "276", "4 yrs"]),
        trow(["5336",  "0.12", "166", "3 yrs"]),
        trow(["7772",  "0.12", "161", "4 yrs"]),
        trow(["8745",  "0.12", "287", "4 yrs"]),
        trow(["9283",  "0.12", "200", "3 yrs"]),
        trow(["11069", "0.12", "191", "5 yrs"]),
        trow(["13280", "0.12", "191", "5 yrs"]),
    ]
    story.extend(make_table("TABLE V.&nbsp;&nbsp;&nbsp;SAMPLE HIGH-RISK EMPLOYEES (TOP 10)", t5_data, cw5))

    # ── VI. DISCUSSION ────────────────────────────────────────────────────────
    story.append(sec("VI", "Discussion"))
    story.append(subsec("A", "Compensation is the Dominant Structural Factor"))
    story.append(body(
        "The four-to-one ratio in turnover rates between low and high salary tiers "
        "is the single most actionable finding. Compensation structure creates a "
        "systemic attrition risk that cannot be resolved through engagement programs "
        "or managerial coaching alone. Organizations with large proportions of "
        "low-salary employees should treat compensation review as a primary retention "
        "strategy [2]."
    ))
    story.append(subsec("B", "Satisfaction Predicts Turnover Independently of Performance"))
    story.append(body(
        "The near-identical evaluation scores between leavers and stayers (0.718 vs. "
        "0.715), combined with the near-zero correlation of last_evaluation "
        "(r = +0.007), challenges the common assumption that turnover is driven by "
        "underperformers. This replicates Mobley's foundational finding [1]: retention "
        "efforts should be framed as a satisfaction and engagement problem, not a "
        "performance management problem."
    ))
    story.append(subsec("C", "Workload Acts as a Compounding Risk Factor"))
    story.append(body(
        "The highest-risk employees combine low satisfaction with above-average hours, "
        "suggesting overwork amplifies the effect of dissatisfaction rather than "
        "driving attrition independently. HR interventions should target the "
        "intersection of these factors [3]."
    ))
    story.append(subsec("D", "Early Intervention Opportunity"))
    story.append(body(
        "The identification of 615 high-risk current employees is the most practically "
        "valuable output of this analysis. HR departments can operationalize it as a "
        "recurring SQL query to generate a prioritized list for manager outreach, "
        "salary review, or promotion consideration before employees resign."
    ))
    story.append(subsec("E", "Limitations"))
    story.append(body(
        "This study has several limitations. First, the dataset is simulated [9] and "
        "limits generalizability of specific threshold values. Second, the analysis "
        "is descriptive, not causal. Third, the dataset lacks department or role "
        "information. Fourth, class imbalance (~24% leavers) must be addressed before "
        "extending this framework to predictive modeling."
    ))

    # ── VII. CONCLUSION ───────────────────────────────────────────────────────
    story.append(sec("VII", "Conclusion"))
    story.append(body(
        "This paper analyzed an HR dataset of 14,999 employees to identify factors "
        "most strongly associated with workforce attrition. Salary tier and job "
        "satisfaction are the two dominant predictors—satisfaction producing the "
        "strongest correlation (r = −0.388)—while performance evaluation is "
        "essentially uncorrelated with departure (r = +0.007). Critically, departed "
        "employees were equally well-evaluated as retained employees, confirming "
        "that turnover is a satisfaction problem, not a performance problem."
    ))
    story.append(body(
        "By normalizing a flat HR CSV into a constraint-validated SQLite schema and "
        "operationalizing findings as reusable SQL queries, we demonstrate that "
        "organizations can generate actionable, prioritized intervention lists from "
        "existing HR data without requiring machine learning infrastructure. The 615 "
        "high-risk employees identified here represent an immediately addressable "
        "retention opportunity."
    ))
    story.append(body(
        "Future work should apply this framework to real organizational data with "
        "department-level granularity, incorporate time-series analysis, and explore "
        "causal inference methods to move beyond association toward actionable "
        "causal claims about salary increases or promotion effects on retention."
    ))

    # ── ACKNOWLEDGMENT ────────────────────────────────────────────────────────
    story.append(Paragraph("ACKNOWLEDGMENT", S["sec"]))
    story.append(body_ni(
        "The author thanks the faculty of the Department of Computer and Electrical "
        "Engineering and Computer Science at California State University, Bakersfield "
        "for guidance on this project."
    ))

    # ── REFERENCES ────────────────────────────────────────────────────────────
    story.append(Paragraph("REFERENCES", S["sec"]))
    refs = [
        "[1] W. H. Mobley, \"Intermediate linkages in the relationship between job satisfaction and employee turnover,\" <i>J. Appl. Psychol.</i>, vol. 62, no. 2, pp. 237–240, 1977.",
        "[2] R. W. Griffeth, P. W. Hom, and S. Gaertner, \"A meta-analysis of antecedents and correlates of employee turnover,\" <i>J. Manag.</i>, vol. 26, no. 3, pp. 463–488, 2000.",
        "[3] P. W. Hom, T. W. Lee, J. D. Shaw, and J. P. Hausknecht, \"One hundred years of employee turnover theory and research,\" <i>J. Appl. Psychol.</i>, vol. 102, no. 3, pp. 530–545, 2017.",
        "[4] Bureau of Labor Statistics, \"Job Openings and Labor Turnover Summary,\" U.S. Dept. of Labor, 2023.",
        "[5] R. Punnoose and P. Ajit, \"Prediction of employee turnover in organizations using machine learning algorithms,\" <i>Int. J. Adv. Res. Artif. Intell.</i>, vol. 5, no. 9, pp. 22–26, 2016.",
        "[6] Y. Zhao et al., \"Employee turnover prediction with machine learning: A reliable approach,\" in <i>Proc. IntelliSys</i>, 2018, pp. 737–758.",
        "[7] S. S. Alduayj and K. Rajpoot, \"Predicting employee attrition using machine learning,\" in <i>Proc. IIT</i>, 2018, pp. 93–98.",
        "[8] F. Doshi-Velez and B. Kim, \"Towards a rigorous science of interpretable machine learning,\" <i>arXiv:1702.08608</i>, 2017.",
        "[9] HR Analytics / Employee Retention Dataset, Kaggle. [Online]. Available: https://www.kaggle.com/",
        "[10] E. F. Codd, \"A relational model of data for large shared data banks,\" <i>Commun. ACM</i>, vol. 13, no. 6, pp. 377–387, 1970.",
    ]
    for r in refs:
        story.append(Paragraph(r, S["ref"]))

    return story

# ── Render ────────────────────────────────────────────────────────────────────
OUT = "/Users/brendamurillo/Desktop/data analyst project/final_paper.pdf"
doc = make_doc(OUT)
doc.build(build())
print(f"Saved: {OUT}")
