import pandas as pd
import mysql.connector
from getpass import getpass

# Load CSV
df = pd.read_csv("data/student_skills.csv")

# MySQL password
password = getpass("Enter your MySQL password: ")

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="placement_user",
    password=password,
    database="PlacementPulse"
)

cursor = conn.cursor()

sql = """
INSERT INTO student_skills (
    Student_ID,
    Skill_ID,
    Skill_Level
)
SELECT %s, Skill_ID, %s
FROM skills
WHERE Skill_Name = %s
"""

for row in df.itertuples(index=False, name=None):
    student_id = row[0]
    skill_name = row[1]
    skill_level = row[2]

    cursor.execute(
        sql,
        (student_id, skill_level, skill_name)
    )

conn.commit()

print("Student skills imported successfully!")
print("Total records imported:", len(df))

cursor.close()
conn.close()