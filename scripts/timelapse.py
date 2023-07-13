import os
import time
from datetime import datetime
from picamera2 import Picamera2
import time


picam2 = Picamera2()
config = picam2.create_preview_configuration({"size": (1920, 1080)})
# config["main"]
# #{'format': 'XBGR8888', 'size': (808, 606)}
# picam2.align_configuration(config)
# # Picamera2 has decided an 800x606 image will be more efficient.
# config["main"]
# #{'format': 'XBGR8888', 'size': (800, 606)}
# picam2.configure(config)


# Define the path to store the images
imagestoragepath = '/home/pi/Desktop/timelapsestorage'

# Create directory if it doesn't exist
os.makedirs(imagestoragepath, exist_ok=True)

def save_image(save_directory):
    """
    Function to save image in the save directory with a timestamp.
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')  # e.g., '20230627_142536'
    file_name = f"{timestamp}.jpg"
    file_path = os.path.join(save_directory, file_name)
    
    # Capture and save image directly
    picam2.start_and_capture_file(file_path)

    return file_path

def take_timelapse(interval, duration, save_directory):
    """
    Function to capture images at regular intervals.
    """
    # Determine end time based on current time and duration
    end_time = time.time() + duration

    while time.time() < end_time:
        # Capture and save image
        save_image(save_directory)

        # Wait for the next capture
        time.sleep(interval)



# Usage
if __name__ == "__main__":
    #take_timelapse(interval=900, duration=44000, save_directory=imagestoragepath)
    take_timelapse(interval=15, duration=60*30, save_directory=imagestoragepath)

#!/usr/bin/python3

import time

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder

# Encode a VGA stream, and capture a higher resolution still image half way through.

picam2 = Picamera2()
half_resolution = [dim // 2 for dim in picam2.sensor_resolution]
main_stream = {"size": half_resolution}
lores_stream = {"size": (640, 480)}
video_config = picam2.create_video_configuration(main_stream, lores_stream, encode="lores")
picam2.configure(video_config)

encoder = H264Encoder(10000000)

picam2.start_recording(encoder, 'test.h264')
time.sleep(5)

# It's better to capture the still in this thread, not in the one driving the camera.
request = picam2.capture_request()
request.save("main", "test.jpg")
request.release()
print("Still image captured!")

time.sleep(5)
picam2.stop_recording()