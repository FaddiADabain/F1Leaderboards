
import mysql.connector

db = mysql.connector.connect(
    user='root',
    password='',
    host='127.0.0.1',
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

data.execute("SELECT * FROM drivers ORDER BY name DESC")

for x in data:
    print(x)
