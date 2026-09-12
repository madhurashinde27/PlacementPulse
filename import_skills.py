import pandas as pd
import mysql.connector
from getpass import getpass

# Load CSV
df = pd.read_csv("data/skills.csv")

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
INSERT INTO skills (
    Skill_ID,
    Skill_Name,
    Category
)
VALUES (%s, %s, %s)
"""

for row in df.itertuples(index=False, name=None):
    cursor.execute(sql, row)

conn.commit()

print("Skills imported successfully!")
print("Total skills imported:", len(df))

cursor.close()
conn.close()