#!/usr/bin/python3

import json
import time
import os
import psutil
import logging
from datetime import datetime
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
from logging.handlers import RotatingFileHandler

print("Current PATH:", os.environ.get("PATH"))
print(f"Script ran at: {datetime.now()}")

# Load config
dir_path = os.path.dirname(os.path.realpath(__file__))

# Use the information from the config file
stream_key = "d6w1-xaz9-szub-vy45-8rj0"

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
    
    def log_parameters(self, parameters: dict):
        """
        Function to log parameters.
        """
        self.logger.info(parameters)

    def log_system_health(self):
        while True:
            system_health = self.get_system_health()
            self.logger.info(system_health)
            time.sleep(60)  # Log every 60 seconds

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
        self.picam2 = Picamera2()

    @staticmethod
    def create_ffmpeg_command(stream_key):
        # This command will push a live stream to the specified YouTube RTMP URL
        return "-f flv rtmp://x.rtmp.youtube.com/live2/{}".format(stream_key)

if __name__ == "__main__":
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
        logger.log_system_health()
            
    except KeyboardInterrupt:
        print(f"Interrupted by keyboard exception, stopping...")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        camera.picam2.stop_recording()

        
