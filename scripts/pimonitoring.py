import psutil
import os
import time
from datetime import datetime
from gpiozero import CPUTemperature

imagestoragepath = 'logs'

def get_cpu_health():
    """
    Function to get CPU health data.
    """
    # Get CPU usage percentage
    cpu_usage = psutil.cpu_percent(interval=1)

    # Get CPU core temperature (gpiozero library supports this for Raspberry Pi)
    cpu_temp = CPUTemperature().temperature

    return {'cpu_usage': cpu_usage, 'cpu_temp': cpu_temp}


def get_network_health():
    """
    Function to get network health data.
    """
    # Get network stats
    net_io_stats = psutil.net_io_counters()

    # Extract desired stats
    sent_bytes = net_io_stats.bytes_sent
    recv_bytes = net_io_stats.bytes_recv

    return {'sent_bytes': sent_bytes, 'recv_bytes': recv_bytes}

def log_health_data():
    """
    Function to log health data.
    """
    while True:
        try:
            # Get health data
            cpu_health = get_cpu_health()
            network_health = get_network_health()

            # Create timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

            # Create directory if it doesn't exist
            os.makedirs(imagestoragepath, exist_ok=True)

            # Define log file path
            log_file = os.path.join(imagestoragepath, f"{timestamp}_health_log.txt")

            # Write health data to log file
            with open(log_file, 'w') as f:
                f.write(f"Timestamp: {timestamp}\n")
                f.write(f"CPU Usage: {cpu_health['cpu_usage']}%\n")
                f.write(f"CPU Temperature: {cpu_health['cpu_temp']}°C\n")
                f.write(f"Bytes Sent: {network_health['sent_bytes']}\n")
                f.write(f"Bytes Received: {network_health['recv_bytes']}\n")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            send_email_notification("Health Log Error", f"An error occurred: {str(e)}", "youralertemail@gmail.com")

        finally:
            # Wait for the next log, even if an error occurred
            time.sleep(60)  # Log every 60 seconds


