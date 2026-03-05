# Queries Reference Guide
**Project:** Heart Disease Data Analysis & Visualization using Tableau  
**Database:** PostgreSQL | **Table:** `heart_disease`  
**SQL File:** `sql/analysis_queries.sql`

---

## Column Reference (Post-Cleaning)

| Column | Type | Values |
|---|---|---|
| `heartdisease` | TEXT | `'Yes'` / `'No'` |
| `bmi` | FLOAT | IQR-clipped: `12.48 – 45.46` |
| `smoking` | INTEGER | `1` = Yes, `0` = No |
| `alcoholdrinking` | INTEGER | `1` = Yes, `0` = No |
| `stroke` | INTEGER | `1` = Yes, `0` = No |
| `physicalhealth` | INTEGER | Days of poor health (0–30) |
| `mentalhealth` | INTEGER | Days of poor mental health (0–30) |
| `diffwalking` | INTEGER | `1` = Yes, `0` = No |
| `sex` | INTEGER | `1` = Male, `0` = Female |
| `agecategory` | TEXT | `'18-24'` … `'80 or older'` (13 groups) |
| `race` | TEXT | White, Black, Asian, Hispanic, Other, American Indian/Alaskan Native |
| `diabetic` | TEXT | `'Yes'` / `'No'` (simplified from 4 values) |
| `physicalactivity` | INTEGER | `1` = Active, `0` = Inactive |
| `genhealth` | TEXT | Excellent, Very good, Good, Fair, Poor |
| `sleeptime` | INTEGER | Hours per night |
| `asthma` | INTEGER | `1` = Yes, `0` = No |
| `kidneydisease` | INTEGER | `1` = Yes, `0` = No |
| `skincancer` | INTEGER | `1` = Yes, `0` = No |

---

## Q0 — Table Overview & Basic Stats

**Purpose:** Validate successful data load and get a high-level snapshot of the dataset before any analysis.

**Queries included:**
- `COUNT(*)` — confirms total rows (expected: 4,494 after deduplication)
- Full summary — aggregates across all key columns: total HD cases, stroke, diabetic, smokers, alcohol, avg BMI, avg physical/mental health days, avg sleep
- HD distribution — shows Yes/No split with percentage, useful for understanding class imbalance
- `LIMIT 10` preview — quick sanity check on column values after cleaning

**Notes:** Run these first after `load_data.py` completes to verify data integrity before connecting Tableau.

---

## Q1 — Gender vs Heart Disease

**Tableau Chart:** Stacked Vertical Bar Chart  
**Shelf config:** Columns → `Sex` | Rows → `COUNT(HeartDisease)` | Color → `HeartDisease` | Stack Marks → ON

**Purpose:** Understand how heart disease prevalence differs between males and females. Supports Dr. Sharma's analysis of demographic risk groups.

**Queries included:**
- Core Tableau query — groups by decoded gender label + heartdisease, returns count for stacked bar
- Percentage breakdown — uses `PARTITION BY sex` window function to compute heart disease rate within each gender independently

**Key note:** `sex` is stored as integer (`1`/`0`). The `CASE WHEN sex = 1 THEN 'Male' ELSE 'Female'` decode is applied in SQL so Tableau receives human-readable labels directly.

---

## Q2 — Age vs Heart Disease

**Tableau Chart:** Grouped Stacked Bar Chart (Age Category + Sex)  
**Shelf config:** Columns → `Age Category`, `Sex` | Rows → `COUNT(HeartDisease)` | Color → `HeartDisease` | Stack Marks → ON

**Purpose:** Identify which age groups carry the highest heart disease burden, further segmented by gender. Key for Dr. Sharma's targeted awareness campaigns and Ramesh's policy planning by demographic.

**Queries included:**
- Core Tableau query — three-way group by (agecategory, gender, heartdisease) produces the multi-bar layout per age group
- Age summary — heart disease count and rate per age group only (no gender split), useful for a simpler trend line view

**Key note:** `agecategory` contains string ranges (`'18-24'`, `'80 or older'`). Tableau will sort these alphabetically by default — apply a custom sort in Tableau using the reference order: 18-24, 25-29, 30-34 … 80 or older.

---

## Q3 — Diabetic vs Stroke

**Tableau Chart:** Bubble Chart (Circle Marks)  
**Shelf config:** Columns → `Diabetic` | Rows → `SUM(Stroke)` | Marks → Circle | Size → `SUM(Stroke)` | Color → `HeartDisease`

**Purpose:** Examine how diabetes status influences stroke occurrence, and whether heart disease compounds that risk. Relevant to Anita's personal risk profile.

**Queries included:**
- Core Tableau query — groups by diabetic + heartdisease, returns `SUM(stroke)` and total patients. Bubble size driven by stroke count, color by HD status
- Stroke rate summary — clean two-row result (Yes/No diabetic) with stroke rate percentage for quick comparison

**Key note:** `stroke` is an integer column (`1`/`0`) after cleaning, so `SUM(stroke)` directly gives the stroke count — no `CASE WHEN` needed. `diabetic` is `TEXT` (`'Yes'`/`'No'`) after simplification from 4 original values.

---

## Q4 — Impact of Smoking and Alcohol on Heart Disease

**Tableau Chart:** Horizontal Stacked Bar Chart  
**Shelf config:** Rows → `Smoking`, `Alcohol` | Columns → `COUNT(HeartDisease)` | Color → `HeartDisease` | Marks → Bar

**Purpose:** Quantify how lifestyle habits (smoking, alcohol) independently and jointly affect heart disease risk. Supports Ramesh's policy recommendations on tobacco regulation and substance awareness.

**Queries included:**
- Core Tableau query — four combinations (Smoker/Drinker, Smoker/Non-Drinker, etc.) with HD breakdown, drives the two-level grouped horizontal bars
- Smoking-only breakdown — isolates smoking effect on HD rate
- Alcohol-only breakdown — isolates alcohol effect on HD rate
- Combined effect — all four combinations ranked by HD rate descending, reveals which combo carries highest risk

**Key note:** Both `smoking` and `alcoholdrinking` are integers. Human-readable labels (`'Smoker'`, `'Drinker'`) are applied via `CASE WHEN` in SQL.

---

## Q5 — Stroke vs Other Diseases

**Tableau Chart:** Clustered Bar Chart  
**Shelf config:** Columns → `Condition` | Rows → `SUM(Stroke)` | Color → `Has Condition`

**Purpose:** Compare how comorbid conditions (asthma, kidney disease, skin cancer) relate to stroke occurrence. Helps identify compounding risk factors beyond cardiac indicators.

**Queries included:**
- Individual queries for Asthma, Kidney Disease, Skin Cancer — each returns stroke count, total, and stroke rate
- Unified UNION ALL pivot — combines all three conditions into a single result set with `condition` and `has_condition` columns, ideal for a single Tableau data source driving all three bars

**Key note:** All three disease columns are integers. The UNION ALL approach is recommended for Tableau as it avoids needing to create multiple data sources or calculated fields for the clustered layout.

---

## Q6 — Race Wise Heart Disease

**Tableau Chart:** Pie Chart  
**Shelf config:** Marks → Pie | Angle → `SUM(hd_count)` | Color → `Race` | Label → Percent of Total (Quick Table Calc)

**Purpose:** Visualize heart disease distribution across racial groups to surface disparities. Relevant to Ramesh's equity-focused policy analysis.

**Queries included:**
- Core Tableau query — returns race, total patients, HD count, and percentage of total HD cases using `SUM(...) OVER ()` window function

**Key note:** Percentage is pre-computed in SQL for reference, but Tableau's built-in "Percent of Total" quick table calculation can also be used directly on the pie angle shelf for interactive filtering.

---

## Q7 — General Health vs Heart Disease

**Tableau Chart:** Packed Bubble Chart  
**Shelf config:** Marks → Packed Bubbles | Size → `COUNT(HeartDisease)` | Color → `GenHealth` | Label → Count

**Purpose:** Show how self-reported general health correlates with heart disease. Patients rating their health as Poor/Fair are expected to show significantly higher HD rates — this visualization makes that pattern immediately visible.

**Queries included:**
- Core Tableau query — groups by genhealth + heartdisease with custom `CASE` sort order (Excellent → Poor) to ensure logical ordering in Tableau
- HD rate by health level — summarized rate table for reference and annotation

**Key note:** `genhealth` contains 5 ordered categories. The `ORDER BY CASE` in SQL sorts them logically — Tableau should respect this order if the field is set as a discrete dimension.

---

## Q8 — Physical Activity vs Heart Disease

**Tableau Chart:** Donut Chart  
**Shelf config:** Duplicate measure on Rows → Dual Axis → First: Pie (Angle = COUNT, Color = PhysicalActivity) | Second: white circle overlay → Synchronize Axis

**Purpose:** Compare heart disease prevalence between physically active and inactive patients. Supports Dr. Sharma's recommendation for exercise-based interventions and Anita's lifestyle monitoring.

**Queries included:**
- Core Tableau query — four combinations (Active/Inactive × Yes/No HD) with count and percentage of total, feeds pie angle and color
- HD rate by activity — clean two-row summary with rate percentage

**Key note:** `physicalactivity` is integer (`1`/`0`). Decoded to `'Active'`/`'Inactive'` in SQL. The donut requires a dual-axis setup in Tableau — the second axis uses a constant `MIN(1)` measure as a white circle to create the hollow center.

---

## Q9 — Age and BMI vs Diabetic

**Tableau Chart:** Treemap  
**Shelf config:** Marks → Treemap | Size → `COUNT(*)` | Color → `AVG(BMI)` | Label → `AgeCategory` + `Diabetic`

**Purpose:** Visualize how age and BMI jointly relate to diabetes status. Larger treemap tiles indicate more patients in that age+BMI+diabetic combination. Color intensity reflects average BMI level.

**Queries included:**
- Core Tableau query — groups by agecategory, BMI category (derived via CASE), and diabetic status with count and avg BMI
- BMI stats by age + diabetic — avg/min/max BMI per combination for reference

**BMI categories used:**

| Range | Label |
|---|---|
| < 18.5 | Underweight |
| 18.5 – 24.9 | Normal |
| 25.0 – 29.9 | Overweight |
| ≥ 30.0 | Obese |

**Key note:** BMI was IQR-clipped during cleaning (range: 12.48–45.46), so extreme outliers are already handled before reaching this query.

---

## Q10 — Stroke Among Heart Disease and Diabetic Patients

**Tableau Chart:** Multi-Level Clustered Bar Chart  
**Shelf config:** Columns → `HeartDisease`, `Diabetic`, `AgeCategory` | Rows → `SUM(Stroke)` | Color → `AgeCategory`

**Purpose:** Identify which combinations of heart disease, diabetes, and age group produce the highest stroke burden. This is the most complex visualization and directly supports all three personas — clinical (Dr. Sharma), policy (Ramesh), and personal risk (Anita).

**Queries included:**
- Core Tableau query — full three-way group (heartdisease × diabetic × agecategory) with stroke count and total patients, drives the multi-level bar layout
- Stroke rate summary — compact four-row result (Yes/Yes, Yes/No, No/Yes, No/No combinations) with stroke rate, useful for annotation

**Key note:** This chart requires all three grouping fields on the Columns shelf in Tableau. Use `AgeCategory` as color to distinguish age cohorts across the clustered bars. Sort `agecategory` manually in Tableau for correct chronological order.

---

## PERF — Performance & Verification

**Purpose:** Validate data load completeness, test query execution speed, and support the project's performance testing requirement.

**Queries included:**
- Full dataset audit — single-query summary of all key counts post-load, compare against expected values (4,494 rows)
- High-risk profile — patients with all three conditions (HeartDisease=Yes, Stroke=1, Diabetic=Yes) grouped by age, gender, and race — most critical patient segment
- Index reference — indexes on `heartdisease`, `agecategory`, `sex`, `race`, `diabetic`, `stroke` are created automatically by `load_data.py`; listed here for documentation
- `EXPLAIN ANALYZE` — uncomment to measure actual query execution time in pgcli or pgAdmin for performance testing documentation

**Expected post-load counts:**

| Metric | Expected |
|---|---|
| Total rows | 4,494 |
| Unique age groups | 13 |
| Unique races | 6 |
| HD = Yes | ~400–500 |
| Stroke = 1 | ~150–250 |
| Diabetic = Yes | ~900–1,100 |