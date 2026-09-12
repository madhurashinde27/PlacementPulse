import pandas as pd
import mysql.connector
from getpass import getpass

# Load students CSV
df = pd.read_csv("data/students.csv")

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

# Insert data
sql = """
INSERT INTO students (
    Student_ID,
    Name,
    Branch,
    CGPA,
    Backlogs,
    Internship,
    Projects,
    Certifications,
    Communication_Score,
    Technical_Score,
    Placement_Status,
    Salary
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for row in df.itertuples(index=False, name=None):
    cursor.execute(sql, row)

conn.commit()

print("Students imported successfully!")
print("Total students imported:", len(df))

cursor.close()
conn.close()