import json
import time
import os
import threading
import psutil
import logging
from datetime import datetime
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, Quality
from picamera2.outputs import FfmpegOutput
from logging.handlers import RotatingFileHandler

# Set up logging
logger = logging.getLogger('system_health')
logger.setLevel(logging.INFO)

# Create a rotating file handler which rotates when the log file reaches 1MB
handler = RotatingFileHandler('logs/system_health.log', maxBytes=1e6, backupCount=10)

# Create a formatter that formats the log message as a JSON string
formatter = logging.Formatter(json.dumps({
    'level': '%(levelname)s',
    'time': '%(asctime)s',
    'message': '%(message)s',
}))

handler.setFormatter(formatter)
logger.addHandler(handler)

def get_system_health():
    """
    Function to get system health data.
    """
    # CPU
    cpu_usage = psutil.cpu_percent(interval=1)

    # Memory
    memory_stats = psutil.virtual_memory()
    memory_usage = memory_stats.percent

    # Disk
    disk_stats = psutil.disk_usage('/')
    disk_usage = disk_stats.percent

    # Network
    net_io_stats = psutil.net_io_counters()
    sent_bytes = net_io_stats.bytes_sent
    recv_bytes = net_io_stats.bytes_recv

    return {
        'cpu_usage': cpu_usage, 
        'memory_usage': memory_usage,
        'disk_usage': disk_usage,
        'sent_bytes': sent_bytes, 
        'recv_bytes': recv_bytes
    }

def log_system_health():
    """
    Function to continuously log system health data.
    """
    while True:
        system_health = get_system_health()
        logger.info(system_health)
        time.sleep(60)  # Log every 60 seconds 

def log_camera_parameters(parameters: dict):
    """
    Function to log camera parameters.
    """
    logger.info(parameters)

# [1]
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

# Log camera parameters
log_camera_parameters({"Display Size": chosen_display, "Video Size": video_size})

# [2]
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

# Log encoder and output parameters
log_camera_parameters({"Encoder Bitrate": 4500000, "Repeat": True, "IPeriod": 40})
log_camera_parameters({"FFmpeg Command": ffmpeg_cmd, "Audio Device": "default", "Audio Sync": -0.3, "Audio Sample Rate": 48000, "Audio Codec": "aac", "Audio Bitrate": 128000})

# [3]
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

    # Log timelapse parameters
    log_camera_parameters({"Timelapse Interval": interval, "Timelapse Duration": duration, "Image Storage Path": imagestoragepath})

# Usage
if __name__ == "__main__":
    try:
        # start livestream
        picam2.start_recording(encoder, output)
        
        # Start logging in a separate thread
        threading.Thread(target=log_system_health, daemon=True).start()
        
        take_timelapse(interval=60, duration=60*60*24*3, imagestoragepath=imagestoragepath)

        # Keep the script running
        while True:
            pass
            
    except KeyboardInterrupt:
        print("Interrupted by user, stopping recording...")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        picam2.stop_recording()

