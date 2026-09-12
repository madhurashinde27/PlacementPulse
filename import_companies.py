import pandas as pd
import mysql.connector
from getpass import getpass

# Load CSV
df = pd.read_csv("data/companies.csv")

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
INSERT INTO companies (
    Company_ID,
    Company_Name,
    Industry,
    Location,
    Company_Size
)
VALUES (%s, %s, %s, %s, %s)
"""

print(df.columns.tolist())
print(df.head())
for row in df.itertuples(index=False, name=None):
    cursor.execute(sql, row)

conn.commit()

print("Companies imported successfully!")
print("Total companies imported:", len(df))

cursor.close()
conn.close()