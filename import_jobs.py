import pandas as pd
import mysql.connector
from getpass import getpass

# Load CSV
df = pd.read_csv("data/jobs.csv")

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
INSERT INTO jobs (
    Job_ID,
    Company_ID,
    Job_Role,
    Required_Skills,
    Minimum_CGPA,
    Experience,
    Salary
)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

print(df.columns.tolist())
print(df.head())

for row in df.itertuples(index=False, name=None):
    cursor.execute(sql, row)

conn.commit()

print("Jobs imported successfully!")
print("Total jobs imported:", len(df))

cursor.close()
conn.close()