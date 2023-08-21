print("Starting PiCamera2")
import os
import time
from datetime import datetime
from picamera2.outputs import FfmpegOutput
from picamera2.encoders import H264Encoder
from picamera2 import Picamera2

print("PiCamera2 Started")
print("import libraries") 

# Define sizes for common displays
display_sizes = {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "1440p": (2560, 1440),
    "4K": (3840, 2160)
}

print("define sizes for common displays")

def create_ffmpeg_command(stream_key):
    # Here we introduce the silent audio directly in the command
    return "-f flv rtmp://x.rtmp.youtube.com/live2/{}".format(stream_key)

print("create ffmpeg command")

stream_key = "dktr-20au-bqkh-3gac-cy62"
ffmpeg_cmd = create_ffmpeg_command(stream_key)

print("stream key")
print(create_ffmpeg_command)

picam2 = Picamera2()

print("picam2 intialized")
chosen_display = "1080p"
video_size = display_sizes[chosen_display]

print("video size")
picam2.configure(picam2.create_video_configuration(main={"size": video_size}))

print("picam2 configured")
encoder = H264Encoder(bitrate=4500000, repeat=True, iperiod=40)

print("encoder configured")

# The adjusted output configuration
output = FfmpegOutput(ffmpeg_cmd, audio=True, audio_samplerate=48000, audio_codec="aac", audio_bitrate=128000)

print("output configured")

if __name__ == "__main__":
    print("mainfunction entered")
    picam2.start_recording(encoder, output)
    print("picam2 started recording")
    time.sleep(10)
    time.sleep(9999999)



