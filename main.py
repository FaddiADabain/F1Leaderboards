import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
database_password = os.getenv("DATABASE_PASSWORD")
host_ip = os.getenv("HOST")
user_id = os.getenv("USER")

db = mysql.connector.connect(
    user=user_id,
    password=database_password,
    host=host_ip,
    database='formulaproject'
    )

data = db.cursor()

# Add data to database
# data.execute("INSERT INTO driverpoints (name, number, points, season) VALUES (%s, %s, %s, %s)",
#              ("Nico Hulkenberg", 27, 0, 2022))
# db.commit()
#
# Change data from database
# data.execute("UPDATE drivers SET season = 2023 WHERE number > 0")
# db.commit()

data.execute("SELECT name FROM drivers WHERE number = 16")
name = data.fetchone()[0]
print(name)

data.reset()

data.execute("SELECT * FROM tire_strategy")

# Fetches specific values from previous statement ALSO pops the first array
# name = data.fetchone()[0]
# print(name)

for x in data:
    print(x)

data.close()
db.close()