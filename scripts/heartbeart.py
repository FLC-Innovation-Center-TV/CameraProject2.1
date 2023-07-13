import requests
import time
while True:
    try:
        requests.post("http://10.54.0.25:4000/heartbeat")
    except Exception as e:
        print(f"Failed to send heartbeat: {str(e)}")
    time.sleep(3)  # Send a heartbeat every 60 seconds


