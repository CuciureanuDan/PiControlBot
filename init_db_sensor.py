import sqlite3

# connect to db
conn = sqlite3.connect('sensor_data.db')
cursor = conn.cursor()

# create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS sensor_data(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
   temperature REAL,
   humidity REAL
)
''')

conn.commit()
conn.close()

