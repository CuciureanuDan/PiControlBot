import matplotlib.pyplot as plt
from datetime import datetime
from db_handler import DataBaseHandler
import os
import matplotlib.dates as mdates

def generate_graph(hours):
   
    """
    Generate and saves a graph of temperature and humidity data for the past specified hours.

    Retrieves sensor data from DB using the DataBaseHandler class.
    Creates a figure with two subplots:
     - first subplot displays temperature over time.
     - second subplot displays humidity over time.

    The graph is saved as PNG file ('./tmp/temperature.png'). If the output directory does not exist, it will be created.
    Args:
      hours (int): The number of past hours for which to retrieves and display sensor data.
    """
    db = DataBaseHandler("sensor_data.db")
    data = db.get_hours_data(hours)  
           
    # Extract relevant columns
    timestamps = [datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S') for row in data]
    temperatures = [row[2] for row in data]
    humidity = [row[3] for row in data]

    # Create a figure with 2 subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10.3, 8))  # Two vertical subplots

    # Plot temperature
    ax1.plot(timestamps, temperatures, label='Temperature (°C)', color='red', marker='o')
    ax1.set_title('Temperature Over Time')
    ax1.set_ylabel('Temperature (°C)')
    ax1.grid(True)
    ax1.legend()
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  # Format X-axis
    ax1.tick_params(axis='x', rotation=45)  # Rotate X-axis labels

    # Plot humidity
    ax2.plot(timestamps, humidity, label='Humidity (%)', color='blue', marker='s')
    ax2.set_title('Humidity Over Time')
    ax2.set_xlabel('Time (Hours:Minutes)')
    ax2.set_ylabel('Humidity (%)')
    ax2.grid(True)
    ax2.legend()
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  # Format X-axis
    ax2.tick_params(axis='x', rotation=45)  # Rotate X-axis labels

    # Adjust layout
    plt.tight_layout()

    # Ensure the output directory exists
    os.makedirs('./tmp', exist_ok=True)

    # Save the plot to a file
    output_path = './tmp/temperature.png'
    plt.savefig(output_path, dpi=500)  # Save as a single image
    print(f"Graphs saved to {output_path}")

    # Close the plot to release memory
    plt.close()

if __name__ == "__main__":
   generate_graph(2)   
