import json
import time
import os
import threading
import psutil
import logging
import subprocess
import cv2
import glob
from datetime import datetime
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, Quality
from picamera2.outputs import FfmpegOutput
from logging.handlers import RotatingFileHandler

# Load config
dir_path = os.path.dirname(os.path.realpath(__file__))
info_path = os.path.join(dir_path, "..", "config", "info.json")


with open(info_path) as f:
    info = json.load(f)

# Use the information from the config file
stream_key = info['stream_key']
bee_username = info['bee_username']
bee_password = info['bee_password']
bee_host = info['bee_host']

class SystemHealthLogger:
    def __init__(self, log_file=os.path.join(dir_path, "..", 'logs', 'system_health.log'), log_level=logging.INFO, max_bytes=1e6, backup_count=10):
        # Set up logging
        self.logger = logging.getLogger('system_health')
        self.logger.setLevel(log_level)

        # Create a rotating file handler which rotates when the log file reaches 1MB
        handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)

        # Create a formatter that formats the log message as a JSON string
        formatter = logging.Formatter(json.dumps({
            'level': '%(levelname)s',
            'time': '%(asctime)s',
            'message': '%(message)s',
        }))

        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    import json


    def get_system_health(self):
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
    
    def log_system_health(self):
        """
        Function to continuously log system health data.
        """
        while True:
            system_health = self.get_system_health()
            self.logger.info(system_health)
            time.sleep(60)  # Log every 60 seconds 
    
    def log_parameters(self, parameters: dict):
        """
        Function to log parameters.
        """
        self.logger.info(parameters)


class Camera:
    # Define sizes for common displays
    DISPLAY_SIZES = {
        "480p": (640, 480),
        "720p": (1280, 720),
        "1080p": (1920, 1080),
        "1440p": (2560, 1440),
        "4K": (3840, 2160)
    }

    def __init__(self, stream_key, chosen_display="1080p"):
        self.chosen_display = chosen_display
        self.video_size = self.DISPLAY_SIZES[chosen_display]
        self.stream_key = stream_key
        self.unuploaded = os.path.join(dir_path, "..", "timelapsestorage", "unuploaded")
        self.uploaded = os.path.join(dir_path, "..", "timelapsestorage", "uploaded")
        self.picam2 = Picamera2()

    @staticmethod
    def create_ffmpeg_command(stream_key):
        # This command will push a live stream to the specified YouTube RTMP URL
        return "-f flv rtmp://x.rtmp.youtube.com/live2/{}".format(stream_key)

    def save_image(self):
        """
        Function to save image in the save directory with a timestamp.
        """
        # Use datetime to get current year, month, and day
        now = datetime.now()
        year, month, day = now.strftime('%Y'), now.strftime('%m'), now.strftime('%d')

        # Append year, month, and day to your image storage path
        save_directory = os.path.join(self.unuploaded, year, month, day)

        # Create directory if it doesn't exist
        os.makedirs(save_directory, exist_ok=True)
        
        timestamp = now.strftime('%Y%m%d_%H%M%S')  # e.g., '20230627_142536'
        file_name = f"{timestamp}.jpg"
        file_path = os.path.join(save_directory, file_name)
        
        # Capture and save image directly
        request = self.picam2.capture_request()
        request.save("main", file_path)
        request.release()

        return file_path
    
    def transfer_file(self, file_path, destination_path):
        """
        Transfer a file to the remote server.
        """
        newcommand = ["sshpass", "-p", bee_password, "scp", file_path, f"{bee_username}@{bee_host}:{destination_path}"]
        completed_process = subprocess.run(newcommand, text=True, capture_output=True)
        upload_successful = completed_process.returncode == 0

        if upload_successful:
            print(f"File {file_path} transferred successfully!")
        else:
            print(f"File transfer failed with the following error:\n{completed_process.stderr}")

        return upload_successful

    def upload_images(self):

        unuploaded = self.unuploaded
        uploaded = self.uploaded
        destination_path = r"C:\Users\flcin\Documents"

        for folder, _, images in os.walk(unuploaded):
            for image_name in images:
                image_path = os.path.join(folder, image_name)
                if self.transfer_file(image_path, destination_path):
                    print(f"Image {image_path} uploaded successfully!")
                    date = os.path.relpath(folder, unuploaded)

                    old_day_folder = os.path.join(unuploaded, date)
                    new_day_folder = os.path.join(uploaded, date)

                    new_image_path = os.path.join(new_day_folder, image_name)

                    os.makedirs(new_day_folder, exist_ok=True)
                    try:
                        os.rename(image_path, new_image_path)
                    except:
                        print("Failed to transfer image to backup, likely because there's already an image with the exact same name.")
                else:
                    print(f"Image upload failed")

    def take_timelapse(self, interval):
        """
        Function to capture images at regular intervals.
        """
        start_time = time.time()
        
        while True:
            # Capture and save image
            self.save_image()
            self.upload_images()
        
            # Wait for the next capture
            time.sleep(interval)
            
            # Calculate elapsed time in hours
            elapsed_time_hours = (time.time() - start_time) / 3600
            
            if elapsed_time_hours > 0.00833333:  # approximately 0.5 minutes
                break   

    def compile_images_to_video(self, dir_to_compile):

        framerate = 24 # frames per second 
        
        # Get the date from the directory name (assuming it ends with yyyy/mm/dd)
        dir_date = dir_to_compile.split('/')[-3:]
        date_str = "".join(dir_date)  # join year, month, day into a single string

        # Get all .jpg files from the directory
        img_array = []
        for filename in sorted(glob.glob(os.path.join(dir_to_compile, '*.jpg'))):
            img = cv2.imread(filename)
            height, width, layers = img.shape
            size = (width,height)
            img_array.append(img)

        # Check if any .jpg files were found
        if not img_array:
            print(f"No images found in {dir_to_compile}. Skipping video compilation.")
            return None  # or handle this situation differently if needed

        # Specify the video name with date prefix and create a VideoWriter object
        video_name = os.path.join(dir_to_compile, f'{date_str}_timelapse.mp4')
        out = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'MP4V'), framerate, size)
        
        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()

        return video_name  # return the path of the created video for further use



if __name__ == "__main__":
    timelapse_photo_interval = 6

    logger = SystemHealthLogger()
    camera = Camera(stream_key)

    # Log camera parameters
    logger.log_parameters({"Display Size": camera.chosen_display, "Video Size": camera.video_size})
    
    ffmpeg_cmd = Camera.create_ffmpeg_command(stream_key)

    camera.picam2.configure(camera.picam2.create_video_configuration(main={"size": camera.video_size}))

    # Encoder parameters
    encoder_bitrate = 4500000
    encoder_repeat = True
    encoder_iperiod = 40

    encoder = H264Encoder(bitrate=encoder_bitrate, repeat=encoder_repeat, iperiod=encoder_iperiod)

    # Log encoder parameters
    logger.log_parameters({"Encoder Bitrate": encoder_bitrate, "Repeat": encoder_repeat, "IPeriod": encoder_iperiod})

    # FfmpegOutput parameters
    ffmpeg_audio = True
    ffmpeg_audio_device = "default"
    ffmpeg_audio_sync = -0.3
    ffmpeg_audio_samplerate = 48000
    ffmpeg_audio_codec = "aac"
    ffmpeg_audio_bitrate = 128000

    output = FfmpegOutput(
        ffmpeg_cmd,
        audio=ffmpeg_audio,
        audio_device=ffmpeg_audio_device,
        audio_sync=ffmpeg_audio_sync,
        audio_samplerate=ffmpeg_audio_samplerate,
        audio_codec=ffmpeg_audio_codec,
        audio_bitrate=ffmpeg_audio_bitrate,
    )

    # Log FfmpegOutput parameters
    logger.log_parameters({
        "FFmpeg Command": ffmpeg_cmd, 
        "Audio Device": ffmpeg_audio_device, 
        "Audio Sync": ffmpeg_audio_sync, 
        "Audio Sample Rate": ffmpeg_audio_samplerate, 
        "Audio Codec": ffmpeg_audio_codec, 
        "Audio Bitrate": ffmpeg_audio_bitrate
    })

    try:
        # start livestream
        camera.picam2.start_recording(encoder, output)
        
        # Start logging in a separate thread
        threading.Thread(target=logger.log_system_health, daemon=True).start()
        
        camera.take_timelapse(interval=timelapse_photo_interval)
            
    except KeyboardInterrupt:
        print("Interrupted by user, stopping recording...")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        camera.picam2.stop_recording()
        # Use datetime to get current year, month, and day
        now = datetime.now()
        year, month, day = now.strftime('%Y'), now.strftime('%m'), now.strftime('%d')

        # Get the path for today's images
        today_directory = os.path.join(camera.uploaded, year, month, day)

        # Compile images into a video
        video_path = camera.compile_images_to_video(today_directory)

        # You may want to print or log the path of the created video
        print(f"Created video at {video_path}")

        destination_path = r"C:\Users\flcin\Documents"
        if(camera.transfer_file(video_path, destination_path)):
            print("Video uploaded successfully")
        else:
            print("Video upload failed")

        os.remove(video_path)
        print("Deleted video from local storage")
