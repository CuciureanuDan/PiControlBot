import sqlite3
import logging

# Configure logging
logger = logging.getLogger(__name__)

class DataBaseHandler:

    """
    A class to handle interactions with an SQLite database for storing and retrieving sensor data.

    Attributes:
      connection: The connection object to the SQLite database.
      cursor: The cursor object for executing SQL commands.
    """
    def __init__(self, db_name):
        """
        Initializes the daatabase connection and cursor.
      
        Args:
            db_name (str): The name of the SQLite database file.
        """

        self.connection = sqlite3.connect(db_name)
        #self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
    
    def insert_sensor_data(self, data) -> None:
        """
        Insert sensor data (temperature and humidity) into the database.

        Args:
            data (dict): A dictionary containing sensor readings with keys:
                - 'temperature' (float)
                - 'humidity' (float)
        """
        try:
           query = "INSERT INTO sensor_data (temperature, humidity) VALUES (?, ?)"
           self.cursor.execute(query, (data['temperature'], data['humidity']))
           self.connection.commit()
        except sqlite3.Error as e:
           logging.error(f"Database error: {e}")
    
    def get_hours_data(self, hours) -> list:
        """
        Retrieves sensor data from the last {hours}.
        
        Args:
          hours (int): The number of hours to retrieve data for.
    
        Returns:
          list of tuples, where each tuple represent a row from table: 
            (ID, Timestamp, Temperature, Humidity)
        """
        
        query = f"SELECT * FROM sensor_data WHERE timestamp >= datetime('now', '-{hours} hours')" 
        self.cursor.execute(query)
        last_hours_data = self.cursor.fetchall()
        #print(type(last_hours_data))
        #print(last_hours_data)
        return last_hours_data

    def close(self):
        self.connection.close()


if __name__ == "__main__":
    db_handler = DataBaseHandler("sensor_data.db") 
    hours_to_retrieve = 2  # Example: Get data from the last 2 hours
    data = db_handler.get_hours_data(hours_to_retrieve)
    db_handler.close()
    print(data)
