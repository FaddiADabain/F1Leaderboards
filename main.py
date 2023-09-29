import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
database_password = os.getenv("DATABASE_PASSWORD")

db = mysql.connector.connect(
    user='user',
    password=database_password,
    host='10.129.238.132',
    database='formulaproject'
    )

data = db.cursor()

# Add data to database
# data.execute("INSERT INTO driverpoints (name, number, points, season) VALUES (%s, %s, %s, %s)",
#              ("Nico Hulkenberg", 27, 0, 2022))
# db.commit()

# Change data from database
# data.execute("UPDATE drivers SET season = 2023 WHERE number > 0")
# db.commit()

data.execute("SELECT * FROM drivers WHERE number = 3 ORDER BY name DESC")

# Fetches specific values from previous statement ALSO pops the first array
i = data.fetchone()[0]

print(i)

for x in data:
    print(x)
