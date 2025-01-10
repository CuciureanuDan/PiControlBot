import sqlite3

class DataBaseHandler:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
    
    def insert_sensor_data(self, data):
        query = "INSERT INTO sensor_data (temperature, humidity) VALUES (?, ?)"
        self.cursor.execute(query, (data['temperature'], data['humidity']))
        self.connection.commit()

    def close(self):
        self.connection.close()
