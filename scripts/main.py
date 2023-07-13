# livestream libraries 
import time
from picamera2.outputs import FfmpegOutput
from picamera2.encoders import H264Encoder, Quality
from picamera2 import Picamera2

# timelapse libraries 
import os
import time
from datetime import datetime
from picamera2 import Picamera2

# Define sizes for common displays
display_sizes = {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "1440p": (2560, 1440),
    "4K": (3840, 2160)
}

# You can then choose a size from this dictionary for your video configuration
chosen_display = "1080p"  # The "p" in these names stands for "progressive scan", and the number refers to the vertical resolution (the number of pixels in each column).
video_size = display_sizes[chosen_display]

def create_ffmpeg_command(stream_key):
    # This command will push a live stream to the specified YouTube RTMP URL
    return "-f flv rtmp://x.rtmp.youtube.com/live2/{}".format(stream_key)

stream_key = "dktr-20au-bqkh-3gac-cy62" # remove this and put it in the config folder 
ffmpeg_cmd = create_ffmpeg_command(stream_key)

picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": video_size}))
encoder = H264Encoder(bitrate=4500000, repeat=True, iperiod=40)

# Creating FfmpegOutput instance with the specified command and audio parameters
output = FfmpegOutput(ffmpeg_cmd, audio=True, audio_device="default", audio_sync=-0.3, audio_samplerate=48000, audio_codec="aac", audio_bitrate=128000)

# Define the path to store the images
imagestoragepath = '/home/pi/Desktop/timelapsestorage'

def save_image(imagestoragepath):
    """
    Function to save image in the save directory with a timestamp.
    """
    # Use datetime to get current year, month, and day
    now = datetime.now()
    year, month, day = now.strftime('%Y'), now.strftime('%m'), now.strftime('%d')

    # Append year, month, and day to your image storage path
    save_directory = os.path.join(imagestoragepath, year, month, day)

    # Create directory if it doesn't exist
    os.makedirs(save_directory, exist_ok=True)
    
    timestamp = now.strftime('%Y%m%d_%H%M%S')  # e.g., '20230627_142536'
    file_name = f"{timestamp}.jpg"
    file_path = os.path.join(save_directory, file_name)
    
    # Capture and save image directly
    request = picam2.capture_request()
    request.save("main", file_path)
    request.release()

    return file_path

def take_timelapse(interval, duration, imagestoragepath):
    """
    Function to capture images at regular intervals.
    """
    # Determine end time based on current time and duration
    end_time = time.time() + duration

    while time.time() < end_time:
        # Capture and save image
        save_image(imagestoragepath)

        # Wait for the next capture
        time.sleep(interval)

# Usage
if __name__ == "__main__":
    picam2.start_recording(encoder, output)
    time.sleep(10)

    take_timelapse(interval=15, duration=60*30, imagestoragepath=imagestoragepath)

    time.sleep(9999999)