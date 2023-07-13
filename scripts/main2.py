# from threading import Thread
# import pimonitoring
# from emailnotifs import send_email_notification

# # Create a thread to run the log_health_data function
# log_health_data_thread = Thread(target=pimonitoring.log_health_data)

# # Start the thread
# log_health_data_thread.start()

# # Now your main.py script will continue to run while the log_health_data function runs in the background
# # Insert the rest of your main.py code here
# import smtplib
# import configparser
# import psutil
# import os
# import time
# from datetime import datetime
# from gpiozero import CPUTemperature
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText

# # Load the configuration file
# config = configparser.ConfigParser()
# config.read('credentials.ini')

# imagestoragepath = 'logs'

# def send_email_notification(subject, body, to_address):
#     """
#     Function to send an email notification.
#     """
#     from_address = config.get('credentials', 'email')
#     from_password = config.get('credentials', 'password')

#     # Setup the email
#     msg = MIMEMultipart()
#     msg['From'] = from_address
#     msg['To'] = to_address
#     msg['Subject'] = subject
#     msg.attach(MIMEText(body, 'plain'))

#     # Send the email
#     try:
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()
#         server.login(from_address, from_password)
#         text = msg.as_string()
#         server.sendmail(from_address, to_address, text)
#         server.quit()
#         print("Email sent successfully")
#     except Exception as e:
#         print(f"Error occurred while sending email: {str(e)}")


# def get_cpu_health():
#     """
#     Function to get CPU health data.
#     """
#     # Get CPU usage percentage
#     cpu_usage = psutil.cpu_percent(interval=1)

#     # Get CPU core temperature (gpiozero library supports this for Raspberry Pi)
#     cpu_temp = CPUTemperature().temperature

#     return {'cpu_usage': cpu_usage, 'cpu_temp': cpu_temp}


# def get_network_health():
#     """
#     Function to get network health data.
#     """
#     # Get network stats
#     net_io_stats = psutil.net_io_counters()

#     # Extract desired stats
#     sent_bytes = net_io_stats.bytes_sent
#     recv_bytes = net_io_stats.bytes_recv

#     return {'sent_bytes': sent_bytes, 'recv_bytes': recv_bytes}


# def log_health_data():
#     """
#     Function to log health data.
#     """
#     while True:
#         try:
#             # Get health data
#             cpu_health = get_cpu_health()
#             network_health = get_network_health()

#             # Create timestamp
#             timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

#             # Create directory if it doesn't exist
#             os.makedirs(imagestoragepath, exist_ok=True)

#             # Define log file path
#             log_file = os.path.join(imagestoragepath, f"{timestamp}_health_log.txt")

#             # Write health data to log file
#             with open(log_file, 'w') as f:
#                 f.write(f"Timestamp: {timestamp}\n")
#                 f.write(f"CPU Usage: {cpu_health['cpu_usage']}%\n")
#                 f.write(f"CPU Temperature: {cpu_health['cpu_temp']}°C\n")
#                 f.write(f"Bytes Sent: {network_health['sent_bytes']}\n")
#                 f.write(f"Bytes Received: {network_health['recv_bytes']}\n")

#         except Exception as e:
#             print(f"An error occurred: {str(e)}")
#             send_email_notification("Health Log Error", f"An error occurred: {str(e)}", "youralertemail@gmail.com")

#         finally:
#             # Wait for the next log, even if an error occurred
#             time.sleep(5)  # Log every 60 seconds

# def main():
#     """
#     Main function to run the health data logger.
#     """
#     log_health_data()

# if __name__ == '__main__':
#     main()
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():
    #Disable OAuthlib's HTTPS verification when running locally.
    #*DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "/home/pi/Desktop/ColinsLivestreamRewriteStarted062623/client_secret_993425110504-nr8fhtpievmrld10kv5bfj7dnu36j1op.apps.googleusercontent.com.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

    request = youtube.liveStreams().list(
        part="snippet,cdn,contentDetails,status",
        mine=True
    )
    response = request.execute()

    print(response)

if __name__ == "__main__":
    main()