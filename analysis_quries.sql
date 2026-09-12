USE PlacementPulse;

-- 1. Total Students
SELECT COUNT(*) AS Total_Students
FROM students;

-- 2. Placed Students
SELECT COUNT(*) AS Placed_Students
FROM students
WHERE Placement_Status = 'Placed';

-- 3. Overall Placement Rate
SELECT 
    ROUND(
        100.0 * SUM(Placement_Status = 'Placed') / COUNT(*),
        2
    ) AS Placement_Rate
FROM students;

-- 4. Branch-wise Placement
SELECT
    Branch,
    COUNT(*) AS Total_Students,
    SUM(Placement_Status = 'Placed') AS Placed_Students,
    ROUND(
        100.0 * SUM(Placement_Status = 'Placed') / COUNT(*),
        2
    ) AS Placement_Rate
FROM students
GROUP BY Branch
ORDER BY Placement_Rate DESC;

-- 5. Internship vs Placement
SELECT
    Internship,
    COUNT(*) AS Total_Students,
    SUM(Placement_Status = 'Placed') AS Placed_Students,
    ROUND(
        100.0 * SUM(Placement_Status = 'Placed') / COUNT(*),
        2
    ) AS Placement_Rate
FROM students
GROUP BY Internship;

-- 6. Average Salary
SELECT
    ROUND(AVG(Salary), 2) AS Average_Salary
FROM students
WHERE Placement_Status = 'Placed';

-- 7. Average CGPA: Placed vs Not Placed
SELECT
    Placement_Status,
    ROUND(AVG(CGPA), 2) AS Average_CGPA,
    ROUND(AVG(Technical_Score), 2) AS Average_Technical_Score,
    ROUND(AVG(Communication_Score), 2) AS Average_Communication_Score
FROM students
GROUP BY Placement_Status;

-- 8. Skill Demand
SELECT
    s.Skill_Name,
    COUNT(ss.Student_ID) AS Students_With_Skill
FROM skills s
LEFT JOIN student_skills ss
    ON s.Skill_ID = ss.Skill_ID
GROUP BY s.Skill_ID, s.Skill_Name
ORDER BY Students_With_Skill DESC;

-- 9. Company-wise Job Openings
SELECT
    c.Company_Name,
    COUNT(j.Job_ID) AS Job_Openings
FROM companies c
LEFT JOIN jobs j
    ON c.Company_ID = j.Company_ID
GROUP BY c.Company_ID, c.Company_Name
ORDER BY Job_Openings DESC;

-- 10. Job Role Analysis
SELECT
    Job_Role,
    COUNT(*) AS Number_of_Jobs,
    ROUND(AVG(Salary), 2) AS Average_Salary,
    MIN(Minimum_CGPA) AS Minimum_CGPA
FROM jobs
GROUP BY Job_Role
ORDER BY Number_of_Jobs DESC;