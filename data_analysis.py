import pandas as pd

# Load datasets
students = pd.read_csv("data/students.csv")
companies = pd.read_csv("data/companies.csv")
skills = pd.read_csv("data/skills.csv")
jobs = pd.read_csv("data/jobs.csv")
student_skills = pd.read_csv("data/student_skills.csv")

# Display basic information
print("Students Dataset:")
print(students.head())

print("\nCompanies Dataset:")
print(companies.head())

print("\nSkills Dataset:")
print(skills.head())

print("\nJobs Dataset:")
print(jobs.head())


# -----------------------------
# BASIC PLACEMENT ANALYSIS
# -----------------------------

total_students = len(students)

placed_students = len(
    students[students["Placement_Status"] == "Placed"]
)

not_placed_students = len(
    students[students["Placement_Status"] == "Not Placed"]
)

placement_rate = (placed_students / total_students) * 100

placed_data = students[students["Placement_Status"] == "Placed"]

average_salary = placed_data["Salary"].mean()
highest_salary = placed_data["Salary"].max()
lowest_salary = placed_data["Salary"].min()

print("\n===== PLACEMENT ANALYSIS =====")

print("Total Students:", total_students)
print("Placed Students:", placed_students)
print("Not Placed Students:", not_placed_students)

print("Placement Rate:", round(placement_rate, 2), "%")

print("Average Salary:", round(average_salary, 2))
print("Highest Salary:", highest_salary)
print("Lowest Salary:", lowest_salary)


# -----------------------------
# BRANCH-WISE PLACEMENT ANALYSIS
# -----------------------------

branch_analysis = students.groupby("Branch").agg(
    Total_Students=("Student_ID", "count"),
    Placed_Students=("Placement_Status", lambda x: (x == "Placed").sum()),
    Average_CGPA=("CGPA", "mean"),
    Average_Salary=("Salary", "mean")
).reset_index()

branch_analysis["Placement_Rate"] = (
    branch_analysis["Placed_Students"]
    / branch_analysis["Total_Students"]
    * 100
)

print("\n===== BRANCH-WISE PLACEMENT ANALYSIS =====")
print(branch_analysis.round(2))


# -----------------------------
# CGPA VS PLACEMENT ANALYSIS
# -----------------------------

students["Placement_Numeric"] = students["Placement_Status"].map({
    "Placed": 1,
    "Not Placed": 0
})

cgpa_analysis = students.groupby(
    pd.cut(
        students["CGPA"],
        bins=[0, 7, 8, 9, 10],
        labels=["Below 7", "7 - 8", "8 - 9", "9 - 10"]
    )
).agg(
    Total_Students=("Student_ID", "count"),
    Placed_Students=("Placement_Numeric", "sum")
).reset_index()

cgpa_analysis["Placement_Rate"] = (
    cgpa_analysis["Placed_Students"]
    / cgpa_analysis["Total_Students"]
    * 100
)

print("\n===== CGPA VS PLACEMENT ANALYSIS =====")
print(cgpa_analysis.round(2))


# -----------------------------
# INTERNSHIP VS PLACEMENT ANALYSIS
# -----------------------------

internship_analysis = students.groupby("Internship").agg(
    Total_Students=("Student_ID", "count"),
    Placed_Students=("Placement_Numeric", "sum"),
    Average_CGPA=("CGPA", "mean"),
    Average_Salary=("Salary", "mean")
).reset_index()

internship_analysis["Placement_Rate"] = (
    internship_analysis["Placed_Students"]
    / internship_analysis["Total_Students"]
    * 100
)

print("\n===== INTERNSHIP VS PLACEMENT ANALYSIS =====")
print(internship_analysis.round(2))


# -----------------------------
# PROJECTS & CERTIFICATIONS ANALYSIS
# -----------------------------

projects_analysis = students.groupby("Projects").agg(
    Total_Students=("Student_ID", "count"),
    Placed_Students=("Placement_Numeric", "sum"),
    Average_CGPA=("CGPA", "mean")
).reset_index()

projects_analysis["Placement_Rate"] = (
    projects_analysis["Placed_Students"]
    / projects_analysis["Total_Students"]
    * 100
)

certification_analysis = students.groupby("Certifications").agg(
    Total_Students=("Student_ID", "count"),
    Placed_Students=("Placement_Numeric", "sum"),
    Average_CGPA=("CGPA", "mean")
).reset_index()

certification_analysis["Placement_Rate"] = (
    certification_analysis["Placed_Students"]
    / certification_analysis["Total_Students"]
    * 100
)

print("\n===== PROJECTS VS PLACEMENT =====")
print(projects_analysis.round(2))

print("\n===== CERTIFICATIONS VS PLACEMENT =====")
print(certification_analysis.round(2))


# -----------------------------
# LOAD STUDENT SKILLS
# -----------------------------

print("\n===== STUDENT SKILLS =====")
print(student_skills.head(10))

print("\nTotal Skill Records:", len(student_skills))
print("Unique Students:", student_skills["Student_ID"].nunique())
print("Unique Skills:", student_skills["Skill_Name"].nunique())


# -----------------------------
# SKILL DEMAND ANALYSIS
# -----------------------------

# Split required skills and create individual skill records
job_skills = jobs.assign(
    Skill_Name=jobs["Required_Skills"].str.split("|")
).explode("Skill_Name")

# Remove extra spaces
job_skills["Skill_Name"] = job_skills["Skill_Name"].str.strip()

# Count how many job postings require each skill
skill_demand = (
    job_skills.groupby("Skill_Name")
    .size()
    .reset_index(name="Job_Demand")
    .sort_values("Job_Demand", ascending=False)
)

print("\n===== TOP DEMANDED SKILLS =====")
print(skill_demand.to_string(index=False))


# -----------------------------
# SKILL GAP ANALYSIS
# -----------------------------

# Count how many students have each skill
student_skill_count = (
    student_skills.groupby("Skill_Name")
    .size()
    .reset_index(name="Student_Count")
)

# Merge job demand with student skill availability
skill_gap = pd.merge(
    skill_demand,
    student_skill_count,
    on="Skill_Name",
    how="outer"
).fillna(0)

# Calculate percentages
skill_gap["Job_Demand_Percent"] = (
    skill_gap["Job_Demand"] / len(jobs) * 100
)

skill_gap["Student_Skill_Percent"] = (
    skill_gap["Student_Count"] / len(students) * 100
)

# Calculate skill gap
skill_gap["Skill_Gap"] = (
    skill_gap["Job_Demand_Percent"]
    - skill_gap["Student_Skill_Percent"]
)

# Sort by highest skill gap
skill_gap = skill_gap.sort_values(
    "Skill_Gap",
    ascending=False
)

print("\n===== SKILL GAP ANALYSIS =====")
print(skill_gap.round(2).to_string(index=False))


# -----------------------------
# SKILL PRIORITY CLASSIFICATION
# -----------------------------

def classify_priority(gap):
    if gap >= 20:
        return "High"
    elif gap >= 10:
        return "Medium"
    else:
        return "Low"


skill_gap["Priority"] = skill_gap["Skill_Gap"].apply(
    classify_priority
)

print("\n===== SKILL PRIORITY =====")

print(
    skill_gap[
        [
            "Skill_Name",
            "Job_Demand",
            "Student_Count",
            "Skill_Gap",
            "Priority"
        ]
    ].round(2).to_string(index=False)
)


# -----------------------------
# STUDENT-WISE SKILL RECOMMENDATION
# -----------------------------

def recommend_skills(student_id):
    
    # Get student's current skills
    current_skills = set(
        student_skills[
            student_skills["Student_ID"] == student_id
        ]["Skill_Name"]
    )

    # Get high and medium priority skills
    priority_skills = skill_gap[
        skill_gap["Priority"].isin(["High", "Medium"])
    ]["Skill_Name"]

    # Find missing skills
    recommended = [
        skill for skill in priority_skills
        if skill not in current_skills
    ]

    return recommended


# Example student
student_id = "ST005"

recommendations = recommend_skills(student_id)

print("\n===== STUDENT SKILL RECOMMENDATION =====")
print("Student ID:", student_id)
print("Current Skills:")

current = student_skills[
    student_skills["Student_ID"] == student_id
]["Skill_Name"].tolist()

print(current)

print("\nRecommended Skills:")
print(recommendations)


# -----------------------------
# PLACEMENT STATUS CHART
# -----------------------------

import matplotlib.pyplot as plt

placement_counts = students["Placement_Status"].value_counts()

plt.figure(figsize=(7, 5))
placement_counts.plot(kind="bar")

plt.title("Placement Status")
plt.xlabel("Placement Status")
plt.ylabel("Number of Students")
plt.xticks(rotation=0)

plt.tight_layout()
plt.show()


# -----------------------------
# BRANCH-WISE PLACEMENT CHART
# -----------------------------

plt.figure(figsize=(8, 5))

plt.bar(
    branch_analysis["Branch"],
    branch_analysis["Placement_Rate"]
)

plt.title("Branch-wise Placement Rate")
plt.xlabel("Branch")
plt.ylabel("Placement Rate (%)")

plt.ylim(0, 100)

plt.tight_layout()
plt.show()


# -----------------------------
# TOP DEMANDED SKILLS CHART
# -----------------------------

top_skills = skill_demand.head(10).sort_values(
    "Job_Demand",
    ascending=True
)

plt.figure(figsize=(9, 6))

plt.barh(
    top_skills["Skill_Name"],
    top_skills["Job_Demand"]
)

plt.title("Top 10 Most Demanded Skills")
plt.xlabel("Number of Job Postings")
plt.ylabel("Skill")

plt.tight_layout()
plt.show()


# -----------------------------
# SKILL GAP CHART
# -----------------------------

top_gap = skill_gap.head(10).sort_values(
    "Skill_Gap",
    ascending=True
)

plt.figure(figsize=(9, 6))

plt.barh(
    top_gap["Skill_Name"],
    top_gap["Skill_Gap"]
)

plt.title("Top Skill Gaps")
plt.xlabel("Skill Gap (%)")
plt.ylabel("Skill")

plt.tight_layout()
plt.show()


# -----------------------------
# SAVE ANALYSIS RESULTS
# -----------------------------

branch_analysis.to_csv(
    "data/branch_analysis.csv",
    index=False
)

skill_demand.to_csv(
    "data/skill_demand.csv",
    index=False
)

skill_gap.to_csv(
    "data/skill_gap_analysis.csv",
    index=False
)

internship_analysis.to_csv(
    "data/internship_analysis.csv",
    index=False
)

projects_analysis.to_csv(
    "data/projects_analysis.csv",
    index=False
)

certification_analysis.to_csv(
    "data/certification_analysis.csv",
    index=False
)

print("\n===== ANALYSIS FILES SAVED SUCCESSFULLY =====")