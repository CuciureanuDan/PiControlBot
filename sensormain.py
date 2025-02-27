import time
import logging
import bme680   

# Configure logging
logger = logging.getLogger(__name__)

class SensorManager:

    """
    Manages the BME680 sensor, handling initialization, stabilization and data retrieval.

    Attributes:
      stabilization_time (int): Time in seconds for sensor stabilization.
      read_interval (int): Interval in seconds between stabilization readings.
      sensor : BME680 sensor object.
      gas_baseline (float): Baseline gas resistance value.
      is_stabilized (bool): Indicates whether the sensor is stabilized.
    """

    def __init__(self, stabilization_time=300, read_interval=2):
        """
        Initialize the BME680 sensor manager.

        Args:
            stabilization_time (int): Time in seconds for sensor stabilization.
            read_interval (int): Interval in seconds between stabilization readings.
        """
        
        try:
            self.sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
        except (RuntimeError, IOError):
            self.sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)
        try:
            self.stabilization_time = stabilization_time
            self.read_interval = read_interval
            self.baseline = None
            self.is_stabilized = False
            self.gas_baseline = -1

            self.sensor.set_humidity_oversample(bme680.OS_2X)
            self.sensor.set_pressure_oversample(bme680.OS_4X)
            self.sensor.set_temperature_oversample(bme680.OS_8X)
            self.sensor.set_filter(bme680.FILTER_SIZE_3)
            self.sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

            self.sensor.set_gas_heater_temperature(320)
            self.sensor.set_gas_heater_duration(150)
            self.sensor.select_gas_heater_profile(0)

            logger.info("Sensor initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize sensor: {e}")
            raise

    def stabilize_sensor(self):
        """
        Run the stabilization process to calculate baseline values.
        Reads data every `read_interval` for `stabilization_time` seconds.
        """

        start_time = time.time()
        curr_time = time.time()
        burn_in_data = []
        logger.info("Starting sensor stabilization.")
        while curr_time - start_time < self.stabilization_time:
            curr_time = time.time()
            if self.sensor.get_sensor_data() and self.sensor.data.heat_stable:
                gas = self.sensor.data.gas_resistance
                burn_in_data.append(gas)
                #print('Gas: {0} Ohms'.format(gas))
                time.sleep(self.read_interval) 

        self.gas_baseline = sum(burn_in_data[-50:]) / 50.0

        self.is_stabilized = True
        logger.info("The stabilization has finished.")


    def read_sensor(self) -> str:
        """
        Read data from the BME680 sensor.

        Returns:
            str: A string with temperature, data pressure, humidity, and air quality (if the sensor is stabilized).
        """
        output = "No sensor data available."
        if self.sensor.get_sensor_data():
            output =("Temperature: {0:.2f} C\n"
                      "Pressure: {1:.2f} hPa \n"
                      "Humidity: {2:.2f} %RH").format(
                self.sensor.data.temperature, 
                self.sensor.data.pressure, 
                self.sensor.data.humidity) 

        if  self.is_stabilized:
            logger.info("All the data will be sent.")
            return self.air_quality(output)
        else:
            logger.warning("Gas Sensor is not stabilized. No data about gas")
            return output
    
    def get_read_sensor(self) -> dict:
       """
       Read data from the BME680 sensor for database population.

       Returns:
         dict: A dictionary with temperature and humidity.
       """
       # FUTURE TO DO: combine this function with simple read_sensor
       while self.sensor.get_sensor_data():
            return {
                  "temperature": self.sensor.data.temperature, 
                  "humidity": self.sensor.data.humidity
            }
   

    def air_quality(self, output):
        """
        Calculate the air quality score using humidity and gas resistance data.
        Retries up to three times if sensor data is not heat-stable or unavailable.

        Args:
            output (str): Base output string from the sensor.

        Returns:
            str: Output string with the air quality score or an error message.
        """

        # Set the humidity baseline to 50%, an optimal indoor humidity.
        hum_baseline = 50.0

        # This sets the balance between humidity and gas reading in the
        # calculation of air_quality_score (25:75, humidity:gas)
        hum_weighting = 0.25

        for attempt in range(3):  # Retry up to 3 times
            try:
                #if self.sensor.get_sensor_data() and self.sensor.data.heat_stable:
                
                if self.sensor.data.heat_stable:
                    gas = self.sensor.data.gas_resistance
                    gas_offset = self.gas_baseline - gas

                    hum = self.sensor.data.humidity
                    hum_offset = hum - hum_baseline

                    # Calculate hum_score as the distance from the hum_baseline.
                    if hum_offset > 0:
                        hum_score = (100 - hum_baseline - hum_offset)
                        hum_score /= (100 - hum_baseline)
                        hum_score *= (hum_weighting * 100)
                    else:
                        hum_score = (hum_baseline + hum_offset)
                        hum_score /= hum_baseline
                        hum_score *= (hum_weighting * 100)

                    # Calculate gas_score as the distance from the gas_baseline.
                    if gas_offset > 0:
                        gas_score = (gas / self.gas_baseline)
                        gas_score *= (100 - (hum_weighting * 100))
                    else:
                        gas_score = 100 - (hum_weighting * 100)

                    # Calculate air_quality_score.
                    air_quality_score = hum_score + gas_score

                    # Return the result with air quality score.
                    return f"{output}\nAir Quality score: {air_quality_score:.2f}"

                logger.warning(f"Attempt {attempt + 1}: Sensor data not heat-stable or unavailable.")
            except Exception as e:
                logger.error(f"Attempt {attempt + 1}: Error reading sensor data: {e}")

            time.sleep(1)  # Small delay before retrying

        # If all attempts fail, return an error message.
        logger.error("Failed to retrieve air quality data after 3 attempts.")
        return f"{output}, Air Quality data unavailable"



if __name__ == "__main__":
    sensor_manager = SensorManager()
    sensor_manager.stabilize_sensor()

