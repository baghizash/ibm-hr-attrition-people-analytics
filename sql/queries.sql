-- ============================================================
-- ANALISIS HR EMPLOYEE ATTRITION  (People Analytics)
-- Tabel: employees  |  Kolom target: Attrition ('Yes' = resign)
-- Rate attrition = SUM(Attrition='Yes') / COUNT(*)
-- ============================================================

-- a. ATTRITION RATE KESELURUHAN
-- Berapa banyak karyawan yang resign dan berapa persen dari total.
SELECT
    COUNT(*)                       AS total_karyawan,
    SUM(Attrition = 'Yes')         AS resign,
    ROUND(100.0 * SUM(Attrition = 'Yes') / COUNT(*), 1) AS rate_persen
FROM employees;

-- b1. ATTRITION PER DEPARTMENT
-- Departemen mana yang tingkat resignnya paling tinggi.
SELECT
    Department,
    COUNT(*)                       AS karyawan,
    SUM(Attrition = 'Yes')         AS resign,
    ROUND(100.0 * SUM(Attrition = 'Yes') / COUNT(*), 1) AS rate_persen
FROM employees
GROUP BY Department
ORDER BY rate_persen DESC;

-- b2. ATTRITION PER JOB ROLE
-- Role mana yang paling tinggi resignnya (urut dari tertinggi).
SELECT
    JobRole,
    COUNT(*)                       AS karyawan,
    SUM(Attrition = 'Yes')         AS resign,
    ROUND(100.0 * SUM(Attrition = 'Yes') / COUNT(*), 1) AS rate_persen
FROM employees
GROUP BY JobRole
ORDER BY rate_persen DESC;

-- c. OVERTIME (LEMBUR) VS ATTRITION
-- Apakah karyawan yang lembur lebih sering resign dibanding yang tidak lembur.
SELECT
    OverTime,
    COUNT(*)                       AS karyawan,
    SUM(Attrition = 'Yes')         AS resign,
    ROUND(100.0 * SUM(Attrition = 'Yes') / COUNT(*), 1) AS rate_persen
FROM employees
GROUP BY OverTime;

-- d. MONTHLY INCOME PER BAND
-- Kelompok gaji bulanan (USD): <3000, 3000-6000, 6000-10000, >10000.
SELECT
    CASE
        WHEN MonthlyIncome < 3000                 THEN '< 3.000'
        WHEN MonthlyIncome < 6000                 THEN '3.000-6.000'
        WHEN MonthlyIncome < 10000                THEN '6.000-10.000'
        ELSE '> 10.000'
    END AS band_gaji,
    COUNT(*)                       AS karyawan,
    SUM(Attrition = 'Yes')         AS resign,
    ROUND(100.0 * SUM(Attrition = 'Yes') / COUNT(*), 1) AS rate_persen
FROM employees
GROUP BY band_gaji
ORDER BY MIN(MonthlyIncome);

-- e. AGE PER KELOMPOK UMUR
-- Kelompok umur: <30, 30-39, 40-49, 50+ tahun.
SELECT
    CASE
        WHEN Age < 30  THEN '< 30'
        WHEN Age < 40  THEN '30-39'
        WHEN Age < 50  THEN '40-49'
        ELSE '50+'
    END AS kelompok_umur,
    COUNT(*)                       AS karyawan,
    SUM(Attrition = 'Yes')         AS resign,
    ROUND(100.0 * SUM(Attrition = 'Yes') / COUNT(*), 1) AS rate_persen
FROM employees
GROUP BY kelompok_umur
ORDER BY MIN(Age);

-- f. DISTANCE FROM HOME (KM) PER KELOMPOK JARAK
-- Kelompok jarak rumah-kantor: 1-4, 5-9, 10-14, 15+ km.
SELECT
    CASE
        WHEN DistanceFromHome < 5   THEN '1-4'
        WHEN DistanceFromHome < 10  THEN '5-9'
        WHEN DistanceFromHome < 15  THEN '10-14'
        ELSE '15+'
    END AS kelompok_jarak,
    COUNT(*)                       AS karyawan,
    SUM(Attrition = 'Yes')         AS resign,
    ROUND(100.0 * SUM(Attrition = 'Yes') / COUNT(*), 1) AS rate_persen
FROM employees
GROUP BY kelompok_jarak
ORDER BY MIN(DistanceFromHome);

-- g1. JOB SATISFACTION VS ATTRITION
-- Kepuasan kerja (Low < Medium < High < Very High) vs tingkat resign.
SELECT
    JobSatisfaction,
    COUNT(*)                       AS karyawan,
    SUM(Attrition = 'Yes')         AS resign,
    ROUND(100.0 * SUM(Attrition = 'Yes') / COUNT(*), 1) AS rate_persen
FROM employees
GROUP BY JobSatisfaction;

-- g2. ENVIRONMENT SATISFACTION VS ATTRITION
-- Kepuasan terhadap lingkungan kerja vs tingkat resign.
SELECT
    EnvironmentSatisfaction,
    COUNT(*)                       AS karyawan,
    SUM(Attrition = 'Yes')         AS resign,
    ROUND(100.0 * SUM(Attrition = 'Yes') / COUNT(*), 1) AS rate_persen
FROM employees
GROUP BY EnvironmentSatisfaction;

-- g3. WORK-LIFE BALANCE VS ATTRITION
-- Keseimbangan kerja-hidup (Bad < Good < Better < Best) vs tingkat resign.
SELECT
    WorkLifeBalance,
    COUNT(*)                       AS karyawan,
    SUM(Attrition = 'Yes')         AS resign,
    ROUND(100.0 * SUM(Attrition = 'Yes') / COUNT(*), 1) AS rate_persen
FROM employees
GROUP BY WorkLifeBalance;

-- h1. YEARS AT COMPANY (MASA KERJA) VS ATTRITION
-- Kelompok masa kerja di perusahaan: 0-2, 3-5, 6-10, 11+ tahun.
SELECT
    CASE
        WHEN YearsAtCompany < 3   THEN '0-2'
        WHEN YearsAtCompany < 6   THEN '3-5'
        WHEN YearsAtCompany < 11  THEN '6-10'
        ELSE '11+'
    END AS masa_kerja,
    COUNT(*)                       AS karyawan,
    SUM(Attrition = 'Yes')         AS resign,
    ROUND(100.0 * SUM(Attrition = 'Yes') / COUNT(*), 1) AS rate_persen
FROM employees
GROUP BY masa_kerja
ORDER BY MIN(YearsAtCompany);

-- h2. YEARS IN CURRENT ROLE (LAMA DI POSISI SEKARANG) VS ATTRITION
-- Kelompok: 0-2, 3-5, 6+ tahun.
SELECT
    CASE
        WHEN YearsInCurrentRole < 3  THEN '0-2'
        WHEN YearsInCurrentRole < 6  THEN '3-5'
        ELSE '6+'
    END AS lama_di_posisi,
    COUNT(*)                       AS karyawan,
    SUM(Attrition = 'Yes')         AS resign,
    ROUND(100.0 * SUM(Attrition = 'Yes') / COUNT(*), 1) AS rate_persen
FROM employees
GROUP BY lama_di_posisi
ORDER BY MIN(YearsInCurrentRole);

-- h3. YEARS SINCE LAST PROMOTION (SEJAK PROMOSI TERAKHIR) VS ATTRITION
-- Kelompok: 0-2, 3-5, 6+ tahun.
SELECT
    CASE
        WHEN YearsSinceLastPromotion < 3  THEN '0-2'
        WHEN YearsSinceLastPromotion < 6  THEN '3-5'
        ELSE '6+'
    END AS sejak_promosi,
    COUNT(*)                       AS karyawan,
    SUM(Attrition = 'Yes')         AS resign,
    ROUND(100.0 * SUM(Attrition = 'Yes') / COUNT(*), 1) AS rate_persen
FROM employees
GROUP BY sejak_promosi
ORDER BY MIN(YearsSinceLastPromotion);

-- i1. GENDER VS ATTRITION
SELECT
    Gender,
    COUNT(*)                       AS karyawan,
    SUM(Attrition = 'Yes')         AS resign,
    ROUND(100.0 * SUM(Attrition = 'Yes') / COUNT(*), 1) AS rate_persen
FROM employees
GROUP BY Gender;

-- i2. MARITAL STATUS VS ATTRITION
SELECT
    MaritalStatus,
    COUNT(*)                       AS karyawan,
    SUM(Attrition = 'Yes')         AS resign,
    ROUND(100.0 * SUM(Attrition = 'Yes') / COUNT(*), 1) AS rate_persen
FROM employees
GROUP BY MaritalStatus
ORDER BY rate_persen DESC;

-- j. BUSINESS TRAVEL VS ATTRITION (BONUS)
-- Non-Travel < Travel_Rarely < Travel_Frequently.
SELECT
    BusinessTravel,
    COUNT(*)                       AS karyawan,
    SUM(Attrition = 'Yes')         AS resign,
    ROUND(100.0 * SUM(Attrition = 'Yes') / COUNT(*), 1) AS rate_persen
FROM employees
GROUP BY BusinessTravel
ORDER BY rate_persen DESC;
