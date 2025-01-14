import time
from db_handler import DataBaseHandler
import logging
import asyncio

# Configure logging
logger = logging.getLogger(__name__)


def fill_database(sensor_manager, db_name="sensor_data.db"):
    """
    Populates the database and alerts on temperature differents between reading too big or if humidity exceeds a certain threshold.

    :param sensor_manager: Object to fetch sensor data.
    :param send_alert: Callback function to send Telegram alerts. 
    :param db_name: Name of the database file.
    """
    logging.info("Database population has started.")
    db = DataBaseHandler(db_name) 
    try:
        while True:
            
            logging.info("One insertion.") # delete later
            # get sensor data
            # looks like if there is imperfect connection i get None in data
            data = None # added
            while data == None: # added
               data = sensor_manager.get_read_sensor() # added
            #data = sensor_manager.get_read_sensor() # original line
            logging.info(f"data: {data}") # delete later
            db.insert_sensor_data(data)
            # wait 10 minutes between readings
            time.sleep(600)
    except KeyboardInterrupt:
        logging.warning("Database got an KeyboardInterrupt")
    finally:
        db.close()
        logging.info("Database is closed.")
