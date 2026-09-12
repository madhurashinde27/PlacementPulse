CREATE DATABASE IF NOT EXISTS PlacementPulse;
USE PlacementPulse;

CREATE TABLE students (
    Student_ID VARCHAR(10) PRIMARY KEY,
    Name VARCHAR(100),
    Branch VARCHAR(20),
    CGPA DECIMAL(3,2),
    Backlogs INT,
    Internship VARCHAR(10),
    Projects INT,
    Certifications INT,
    Communication_Score INT,
    Technical_Score INT,
    Placement_Status VARCHAR(20),
    Salary INT
);

CREATE TABLE companies (
    Company_ID VARCHAR(10) PRIMARY KEY,
    Company_Name VARCHAR(100),
    Industry VARCHAR(100),
    Location VARCHAR(100),
    Company_Size VARCHAR(20)
);

CREATE TABLE skills (
    Skill_ID VARCHAR(10) PRIMARY KEY,
    Skill_Name VARCHAR(100),
    Category VARCHAR(50)
);

CREATE TABLE jobs (
    Job_ID VARCHAR(10) PRIMARY KEY,
    Company_ID VARCHAR(10),
    Job_Role VARCHAR(100),
    Required_Skills TEXT,
    Minimum_CGPA DECIMAL(3,2),
    Experience INT,
    Salary INT,
    FOREIGN KEY (Company_ID) REFERENCES companies(Company_ID)
);

CREATE TABLE student_skills (
    Student_ID VARCHAR(10),
    Skill_ID VARCHAR(10),
    Skill_Level VARCHAR(20),
    PRIMARY KEY (Student_ID, Skill_ID),
    FOREIGN KEY (Student_ID) REFERENCES students(Student_ID),
    FOREIGN KEY (Skill_ID) REFERENCES skills(Skill_ID)
);