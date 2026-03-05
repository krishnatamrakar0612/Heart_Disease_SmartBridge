-- Heart Disease Analysis Queries
-- Table: heart_disease | DB: PostgreSQL
-- See: queries_reference.md for full descriptions


-- [Q0] TABLE OVERVIEW
SELECT COUNT(*) AS total_records FROM heart_disease;

SELECT
    COUNT(*)                                                              AS total_rows,
    COUNT(DISTINCT agecategory)                                           AS unique_age_groups,
    COUNT(DISTINCT race)                                                  AS unique_races,
    SUM(CASE WHEN heartdisease = 'Yes' THEN 1 ELSE 0 END)                AS total_heart_disease,
    SUM(stroke)                                                           AS total_stroke,
    SUM(CASE WHEN diabetic = 'Yes' THEN 1 ELSE 0 END)                    AS total_diabetic,
    SUM(smoking)                                                          AS total_smokers,
    SUM(alcoholdrinking)                                                  AS total_alcohol,
    ROUND(AVG(bmi)::NUMERIC, 2)                                           AS avg_bmi,
    ROUND(AVG(physicalhealth)::NUMERIC, 2)                                AS avg_physical_health_days,
    ROUND(AVG(mentalhealth)::NUMERIC, 2)                                  AS avg_mental_health_days,
    ROUND(AVG(sleeptime)::NUMERIC, 2)                                     AS avg_sleep_hours
FROM heart_disease;

SELECT
    heartdisease,
    COUNT(*)                                                              AS count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()::NUMERIC, 2)          AS percentage
FROM heart_disease
GROUP BY heartdisease
ORDER BY heartdisease;

SELECT * FROM heart_disease LIMIT 10;


-- [Q1] GENDER VS HEART DISEASE | Chart: Stacked Vertical Bar
SELECT
    CASE WHEN sex = 1 THEN 'Male' ELSE 'Female' END                      AS gender,
    heartdisease,
    COUNT(*)                                                              AS count
FROM heart_disease
GROUP BY sex, heartdisease
ORDER BY sex DESC, heartdisease;

SELECT
    CASE WHEN sex = 1 THEN 'Male' ELSE 'Female' END                      AS gender,
    heartdisease,
    COUNT(*)                                                              AS count,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY sex)::NUMERIC, 2
    )                                                                     AS pct_within_gender
FROM heart_disease
GROUP BY sex, heartdisease
ORDER BY sex DESC, heartdisease;


-- [Q2] AGE VS HEART DISEASE | Chart: Grouped Stacked Bar
SELECT
    agecategory,
    CASE WHEN sex = 1 THEN 'Male' ELSE 'Female' END                      AS gender,
    heartdisease,
    COUNT(*)                                                              AS count
FROM heart_disease
GROUP BY agecategory, sex, heartdisease
ORDER BY agecategory, sex DESC, heartdisease;

SELECT
    agecategory,
    COUNT(*)                                                              AS total,
    SUM(CASE WHEN heartdisease = 'Yes' THEN 1 ELSE 0 END)                AS hd_count,
    ROUND(
        SUM(CASE WHEN heartdisease = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*)::NUMERIC, 2
    )                                                                     AS hd_rate_pct
FROM heart_disease
GROUP BY agecategory
ORDER BY agecategory;


-- [Q3] DIABETIC VS STROKE | Chart: Bubble Chart
SELECT
    diabetic,
    heartdisease,
    SUM(stroke)                                                           AS stroke_count,
    COUNT(*)                                                              AS total_patients
FROM heart_disease
GROUP BY diabetic, heartdisease
ORDER BY diabetic, heartdisease;

SELECT
    diabetic,
    COUNT(*)                                                              AS total,
    SUM(stroke)                                                           AS stroke_count,
    ROUND(SUM(stroke) * 100.0 / COUNT(*)::NUMERIC, 2)                    AS stroke_rate_pct
FROM heart_disease
GROUP BY diabetic
ORDER BY stroke_rate_pct DESC;


-- [Q4] SMOKING & ALCOHOL VS HEART DISEASE | Chart: Horizontal Stacked Bar
SELECT
    CASE WHEN smoking = 1 THEN 'Smoker' ELSE 'Non-Smoker' END            AS smoking_status,
    CASE WHEN alcoholdrinking = 1 THEN 'Drinker' ELSE 'Non-Drinker' END  AS alcohol_status,
    heartdisease,
    COUNT(*)                                                              AS count
FROM heart_disease
GROUP BY smoking, alcoholdrinking, heartdisease
ORDER BY smoking DESC, alcoholdrinking DESC, heartdisease;

SELECT
    CASE WHEN smoking = 1 THEN 'Smoker' ELSE 'Non-Smoker' END            AS smoking_status,
    COUNT(*)                                                              AS total,
    SUM(CASE WHEN heartdisease = 'Yes' THEN 1 ELSE 0 END)                AS hd_count,
    ROUND(
        SUM(CASE WHEN heartdisease = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*)::NUMERIC, 2
    )                                                                     AS hd_rate_pct
FROM heart_disease
GROUP BY smoking ORDER BY smoking DESC;

SELECT
    CASE WHEN alcoholdrinking = 1 THEN 'Drinker' ELSE 'Non-Drinker' END  AS alcohol_status,
    COUNT(*)                                                              AS total,
    SUM(CASE WHEN heartdisease = 'Yes' THEN 1 ELSE 0 END)                AS hd_count,
    ROUND(
        SUM(CASE WHEN heartdisease = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*)::NUMERIC, 2
    )                                                                     AS hd_rate_pct
FROM heart_disease
GROUP BY alcoholdrinking ORDER BY alcoholdrinking DESC;

SELECT
    CASE WHEN smoking = 1 THEN 'Smoker' ELSE 'Non-Smoker' END            AS smoking_status,
    CASE WHEN alcoholdrinking = 1 THEN 'Drinker' ELSE 'Non-Drinker' END  AS alcohol_status,
    COUNT(*)                                                              AS total,
    SUM(CASE WHEN heartdisease = 'Yes' THEN 1 ELSE 0 END)                AS hd_count,
    ROUND(
        SUM(CASE WHEN heartdisease = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*)::NUMERIC, 2
    )                                                                     AS hd_rate_pct
FROM heart_disease
GROUP BY smoking, alcoholdrinking
ORDER BY hd_rate_pct DESC;


-- [Q5] STROKE VS OTHER DISEASES | Chart: Clustered Bar
SELECT 'Asthma'         AS condition,
       CASE WHEN asthma = 1 THEN 'Yes' ELSE 'No' END                     AS has_condition,
       SUM(stroke)                                                        AS stroke_count,
       COUNT(*)                                                           AS total
FROM heart_disease GROUP BY asthma

UNION ALL

SELECT 'Kidney Disease',
       CASE WHEN kidneydisease = 1 THEN 'Yes' ELSE 'No' END,
       SUM(stroke), COUNT(*)
FROM heart_disease GROUP BY kidneydisease

UNION ALL

SELECT 'Skin Cancer',
       CASE WHEN skincancer = 1 THEN 'Yes' ELSE 'No' END,
       SUM(stroke), COUNT(*)
FROM heart_disease GROUP BY skincancer

ORDER BY condition, has_condition;


-- [Q6] RACE VS HEART DISEASE | Chart: Pie Chart
SELECT
    race,
    COUNT(*)                                                              AS total_patients,
    SUM(CASE WHEN heartdisease = 'Yes' THEN 1 ELSE 0 END)                AS hd_count,
    ROUND(
        SUM(CASE WHEN heartdisease = 'Yes' THEN 1 ELSE 0 END) * 100.0
        / SUM(SUM(CASE WHEN heartdisease = 'Yes' THEN 1 ELSE 0 END))
          OVER ()::NUMERIC, 2
    )                                                                     AS pct_of_total_hd
FROM heart_disease
GROUP BY race
ORDER BY hd_count DESC;


-- [Q7] GENERAL HEALTH VS HEART DISEASE | Chart: Packed Bubble
SELECT
    genhealth,
    heartdisease,
    COUNT(*)                                                              AS count
FROM heart_disease
GROUP BY genhealth, heartdisease
ORDER BY
    CASE genhealth
        WHEN 'Excellent' THEN 1 WHEN 'Very good' THEN 2
        WHEN 'Good'      THEN 3 WHEN 'Fair'      THEN 4
        WHEN 'Poor'      THEN 5
    END, heartdisease;

SELECT
    genhealth,
    COUNT(*)                                                              AS total,
    SUM(CASE WHEN heartdisease = 'Yes' THEN 1 ELSE 0 END)                AS hd_count,
    ROUND(
        SUM(CASE WHEN heartdisease = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*)::NUMERIC, 2
    )                                                                     AS hd_rate_pct
FROM heart_disease
GROUP BY genhealth
ORDER BY hd_rate_pct DESC;


-- [Q8] PHYSICAL ACTIVITY VS HEART DISEASE | Chart: Donut Chart
SELECT
    CASE WHEN physicalactivity = 1 THEN 'Active' ELSE 'Inactive' END     AS activity_status,
    heartdisease,
    COUNT(*)                                                              AS count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()::NUMERIC, 2)          AS pct_of_total
FROM heart_disease
GROUP BY physicalactivity, heartdisease
ORDER BY physicalactivity DESC, heartdisease;

SELECT
    CASE WHEN physicalactivity = 1 THEN 'Active' ELSE 'Inactive' END     AS activity_status,
    COUNT(*)                                                              AS total,
    SUM(CASE WHEN heartdisease = 'Yes' THEN 1 ELSE 0 END)                AS hd_count,
    ROUND(
        SUM(CASE WHEN heartdisease = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*)::NUMERIC, 2
    )                                                                     AS hd_rate_pct
FROM heart_disease
GROUP BY physicalactivity
ORDER BY physicalactivity DESC;


-- [Q9] AGE & BMI VS DIABETIC | Chart: Treemap
SELECT
    agecategory,
    CASE
        WHEN bmi < 18.5                THEN 'Underweight'
        WHEN bmi BETWEEN 18.5 AND 24.9 THEN 'Normal'
        WHEN bmi BETWEEN 25.0 AND 29.9 THEN 'Overweight'
        ELSE                                'Obese'
    END                                                                   AS bmi_category,
    diabetic,
    COUNT(*)                                                              AS count,
    ROUND(AVG(bmi)::NUMERIC, 2)                                           AS avg_bmi
FROM heart_disease
GROUP BY agecategory, bmi_category, diabetic
ORDER BY agecategory, bmi_category, diabetic;

SELECT
    agecategory,
    diabetic,
    COUNT(*)                                                              AS total,
    ROUND(AVG(bmi)::NUMERIC, 2)                                           AS avg_bmi,
    ROUND(MIN(bmi)::NUMERIC, 2)                                           AS min_bmi,
    ROUND(MAX(bmi)::NUMERIC, 2)                                           AS max_bmi
FROM heart_disease
GROUP BY agecategory, diabetic
ORDER BY agecategory, diabetic;


-- [Q10] STROKE | HEART DISEASE & DIABETIC | Chart: Multi-Level Clustered Bar
SELECT
    heartdisease,
    diabetic,
    agecategory,
    SUM(stroke)                                                           AS stroke_count,
    COUNT(*)                                                              AS total_patients
FROM heart_disease
GROUP BY heartdisease, diabetic, agecategory
ORDER BY heartdisease, diabetic, agecategory;

SELECT
    heartdisease,
    diabetic,
    COUNT(*)                                                              AS total_patients,
    SUM(stroke)                                                           AS stroke_count,
    ROUND(SUM(stroke) * 100.0 / COUNT(*)::NUMERIC, 2)                    AS stroke_rate_pct
FROM heart_disease
GROUP BY heartdisease, diabetic
ORDER BY stroke_rate_pct DESC;


-- [PERF] PERFORMANCE & VERIFICATION
SELECT
    COUNT(*)                                                              AS total_rows,
    COUNT(DISTINCT agecategory)                                           AS unique_age_groups,
    COUNT(DISTINCT race)                                                  AS unique_races,
    SUM(CASE WHEN heartdisease = 'Yes' THEN 1 ELSE 0 END)                AS total_hd,
    SUM(stroke)                                                           AS total_stroke,
    SUM(CASE WHEN diabetic = 'Yes' THEN 1 ELSE 0 END)                    AS total_diabetic
FROM heart_disease;

-- High-risk profile: HeartDisease + Stroke + Diabetic
SELECT
    agecategory,
    CASE WHEN sex = 1 THEN 'Male' ELSE 'Female' END                      AS gender,
    race,
    COUNT(*)                                                              AS high_risk_count
FROM heart_disease
WHERE heartdisease = 'Yes'
  AND stroke       = 1
  AND diabetic     = 'Yes'
GROUP BY agecategory, sex, race
ORDER BY high_risk_count DESC;

-- Indexes (handled by load_data.py — listed for reference)
-- CREATE INDEX IF NOT EXISTS idx_heartdisease ON heart_disease(heartdisease);
-- CREATE INDEX IF NOT EXISTS idx_agecategory  ON heart_disease(agecategory);
-- CREATE INDEX IF NOT EXISTS idx_sex          ON heart_disease(sex);
-- CREATE INDEX IF NOT EXISTS idx_race         ON heart_disease(race);
-- CREATE INDEX IF NOT EXISTS idx_diabetic     ON heart_disease(diabetic);
-- CREATE INDEX IF NOT EXISTS idx_stroke       ON heart_disease(stroke);

-- EXPLAIN ANALYZE SELECT heartdisease, COUNT(*) FROM heart_disease GROUP BY heartdisease;