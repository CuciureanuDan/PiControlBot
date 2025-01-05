from telegram import Update
from telegram.ext import filters, MessageHandler, Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os
import logging
from functools import wraps
from sensormain import SensorManager


load_dotenv('credentials.env')

# select only the specific users
ALLOWED_USERS = set(map(int, os.getenv("ALLOWED_USERS","").split(',')))


# This part is for setting up logging module, so you will know when (and why) things don't work as expected:
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

def restricted(func):
    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in ALLOWED_USERS:
            print(f"Unauthorized access denied for {user_id}.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapped

# Bot command handlers
#@restricted
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to IoT Radio Bot! Use /status to get sensor data. ")
    print("Start setted") # just a test

@restricted
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #data = get_sensor_data() # TO BE ADDED
    sensor_manager: SensorManager = context.bot_data['sensor_manager']
    
    output = "Current sensor data:"
    sensor_data = sensor_manager.read_sensor()  # Retrieve sensor data
    await update.message.reply_text(f"{output}\n{sensor_data}")
    #await update.message.reply_text(f"Current Sensor Data:\n{data}")


# must be added last
#@restricted # commented just for test
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")   

# Main function
def main():

    TAPI_KEY = os.getenv('TEL_API_KEY')
    if not TAPI_KEY:
        raise ValueError("Telegram API key not found. Please set TEL_API_KEY in your .env file.")
    

    sensor_manager = SensorManager(90,1)

    try:
        sensor_manager.stabilize_sensor()
    except Exception as e:
        logging.error(f"Failed to stabilize sensor: {e}")
 
    # add longer time to proccess the requests in case of network instability
    application =( Application.builder()
        .token(TAPI_KEY).connect_timeout(30)
        .read_timeout(30).write_timeout(30).build() )
    
    # add SensorManager to bot_data for sharing across handlers
    application.bot_data['sensor_manager'] = sensor_manager

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    # Start the bot (asynchronously)
    application.run_polling()


if __name__ == "__main__":
    main()


