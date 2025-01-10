import time
from db_handler import DataBaseHandler
import logging

# Configure logging
logger = logging.getLogger(__name__)


def fill_database(sensor_manager, db_name="sensor_data.db"):
    logging.info("Database population has started.")
    db = DataBaseHandler(db_name) 
    try:
        while True:
            
            logging.info("One insertion.")
            # get sensor data
            data = sensor_manager.get_read_sensor()
            db.insert_sensor_data(data)
            
            # wait 10 minutes between readings
            time.sleep(600)
    except KeyboardInterrupt:
        logging.warning("Database got an KeyboardInterrupt")
    finally:
        db.close()
        logging.info("Database is closed.")
