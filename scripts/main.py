import os
import time
from datetime import datetime
from picamera2.outputs import FfmpegOutput
from picamera2.encoders import H264Encoder
from picamera2 import Picamera2

# Define sizes for common displays
display_sizes = {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "1440p": (2560, 1440),
    "4K": (3840, 2160)
}

# # Configuration Folder and File
# CONFIG_DIR = './config'  # Relative path to the current script's directory
# CONFIG_FILE = 'stream_key.txt'
# os.makedirs(CONFIG_DIR, exist_ok=True)  # Ensure the directory exists

# def get_stream_key():
#     with open(os.path.join(CONFIG_DIR, CONFIG_FILE), 'r') as file:
#         return file.readline().strip()

def create_ffmpeg_command(stream_key):
    return "-f flv rtmp://a.rtmp.youtube.com/live2/{}".format("d6w1-xaz9-szub-vy45-8rj0")

stream_key = get_stream_key()
ffmpeg_cmd = create_ffmpeg_command(stream_key)

picam2 = Picamera2()
chosen_display = "1080p"
video_size = display_sizes[chosen_display]
picam2.configure(picam2.create_video_configuration(main={"size": video_size}))
encoder = H264Encoder(bitrate=4500000, repeat=True, iperiod=40)
output = FfmpegOutput(ffmpeg_cmd, audio=True, audio_device="default", audio_sync=-0.3, 
                      audio_samplerate=48000, audio_codec="aac", audio_bitrate=128000)

# Image Storage Path (relative to the script's location)
imagestoragepath = './timelapsestorage'  # Notice it's a relative path now

def save_image(imagestoragepath):
    now = datetime.now()
    year, month, day = now.strftime('%Y'), now.strftime('%m'), now.strftime('%d')
    save_directory = os.path.join(imagestoragepath, year, month, day)
    os.makedirs(save_directory, exist_ok=True)
    
    timestamp = now.strftime('%Y%m%d_%H%M%S')
    file_name = f"{timestamp}.jpg"
    file_path = os.path.join(save_directory, file_name)
    
    request = picam2.capture_request()
    request.save("main", file_path)
    request.release()

    return file_path

def take_timelapse(interval, duration, imagestoragepath):
    end_time = time.time() + duration
    while time.time() < end_time:
        save_image(imagestoragepath)
        time.sleep(interval)

if __name__ == "__main__":
    picam2.start_recording(encoder, output)
    time.sleep(10)
    take_timelapse(interval=15, duration=60*30, imagestoragepath=imagestoragepath)
    time.sleep(9999999)

