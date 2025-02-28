# PiControlBot

This project is a Telegram bot that monitors environmental data using a BME680 sensor connected to a Raspberry Pi 5. The bot provides real-time sensor data, system information, and generates graphs for temperature and humidity over time.

## Features

- **Telegram Bot Integration**: Interact with the bot via Telegram commands to get sensor data and system information.
- **Sensor Data Monitoring**: Retrieve real-time temperature, humidity, pressure, and air quality data from the BME680 sensor.
- **System Information**: Get CPU temperature, memory usage, and system uptime of the Raspberry Pi.
- **Graph Generation**: Generate and view graphs of temperature and humidity data over a specified time period.

## Prerequisites

- **Hardware**:
  - Raspberry Pi 5
  - BME680 sensor
- **Software**:
  - Python 3.11.2 (tested, other versions may not work)
  - `python3-venv` (optional, for virtual environment)
  - Required Python packages (listed in `requirements.txt`)

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/CuciureanuDan/PiControlBot.git
   cd PiControlBot
   ```

2. **Set Up a Virtual Environment (Optional)**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set Up the DataBase:**
   - Run the `init_db_sensor.py` script to create the SQLite database:
   ```bash
   python3 init_db_sensor.py
   ```
5. **Configure Environment Variables:**
   - Create a `credentials.env` file in the root directory with the following content:
   ```env
   TEL_API_KEY=your_telegram_bot_api_key
   ALLOWED_USERS=user_id1,user_id2
   ```
   - Replace `your_telegram_bot_api_key` with your actual Telegram bot API key. Check [Obtain Your Bot Token](https://core.telegram.org/bots/tutorial#obtain-your-bot-token) section.
   - Replace `user_id1,user_id2` with the Telegram user IDs of the users allowed to interact with the bot.
6. **Run the bot:**
   - Start the bot by running the `botmain.py` script:
   ```bash
   python3 botmain.py
   ```
## Usage

Once the bot is running, you can interact with it using the following commands in Telegram:

 - **/start**: Start the bot and get a welcome message with available commands.
 - **/status**: Get the current sensor data (temperature, humidity, pressure, and air quality).
 - **/inforpi**: Get system information (CPU temperature and memory usage).
 - **/uptime**: Get the system uptime of the Raspberry Pi.
 - **/graph [hours]**: Generate and view a graph of temperature and humidity data over the specified number of hours (default is 12 hours).

## File Structure

- **botmain.py**: The main script to run the Telegram bot.
- **data_filler.py**: Script to populate the database with sensor data at regular intervals.
- **db_handler.py**: Handles interactions with the SQLite database.
- **graph.py**: Generates graphs from the sensor data.
- **init_db_sensor.py**: Initializes the SQLite database (must be run first).
- **sensormain.py**: Manages the BME680 sensor and retrieves sensor data.
- **systeminfo.py**: Retrieves system information from the Raspberry Pi.

## License

[MIT](https://choosealicense.com/licenses/mit/)
##
**Note**: Ensure that your `credentials.env` file is not shared publicly, as it contains sensitive information.
