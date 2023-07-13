# import subprocess
# import time
# from picamera2 import Picamera2

# #picam2 = Picamera2()

# def create_libcamera_vid_command(width, height, framerate, g_value):
#     return [
#         "libcamera-vid",
#         "-o", "-",
#         "-t", "0",
#         "--width", str(width),
#         "--height", str(height),
#         "--framerate", str(framerate),
#         "-g", str(g_value)
#     ]

# def create_ffmpeg_command(stream_key, audio_rate, audio_channels, audio_codec, format, bit_rate, flv_format):
#     return [
#         "ffmpeg",
#         "-re",
#         "-ar", str(audio_rate),
#         "-ac", str(audio_channels),
#         "-acodec", audio_codec,
#         "-f", format,
#         "-ac", str(audio_channels),
#         "-i", "/dev/zero",
#         "-i", "pipe:0",
#         "-c:v", "copy",
#         "-b:v", str(bit_rate),
#         "-f", flv_format,
#         # "-f", "mp4",
#         # "-movflags", "frag_keyframe+empty_moov",
#         f"rtmp://x.rtmp.youtube.com/live2/{stream_key}"
#     ]


# def execute_commands(libcamera_vid_command, ffmpeg_command):
#     try:
#         # Launch the libcamera_vid subprocess
#         libcamera_vid_process = subprocess.Popen(libcamera_vid_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#         # Launch the ffmpeg subprocess that takes the output of libcamera_vid_process
#         ffmpeg_process = subprocess.Popen(ffmpeg_command, stdin=libcamera_vid_process.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#         libcamera_vid_process.stdout.close()  # Make sure libcamera_vid_process.stdout is closed so ffmpeg_process reads EOF.

#         # Communicate with the ffmpeg process
#         stdout, stderr = ffmpeg_process.communicate()
#     except subprocess.TimeoutExpired:
#         print("Error: Command execution exceeded the timeout.")
#     except subprocess.SubprocessError as e:
#         print(f"An error occurred while executing the subprocess: {str(e)}")
#     else:
#         if ffmpeg_process.returncode != 0:
#             print(f"Error occurred: {stderr.decode()}")
#         else:
#             print(stdout.decode())


# stream_key = "dktr-20au-bqkh-3gac-cy62"  # replace this with your actual stream key
# libcamera_vid_command = create_libcamera_vid_command(1920, 1080, 30, 40)
# ffmpeg_command = create_ffmpeg_command(stream_key, 44100, 2, "pcm_s16le", "s16le", 4500000, "flv")

# execute_commands(libcamera_vid_command, ffmpeg_command)

# # time.sleep(3)

# # request = picam2.capture_request()
# # request.save("main", "testTODAY.jpg")
# # request.release()
# # print("Still image captured!")


# # import time

# # from picamera2.encoders import H264Encoder

# # # Encode a VGA stream, and capture a higher resolution still image half way through.


# # # half_resolution = [dim // 2 for dim in picam2.sensor_resolution]
# # # main_stream = {"size": half_resolution}
# # # lores_stream = {"size": (640, 480)}
# # # video_config = picam2.create_video_configuration(main_stream, lores_stream, encode="lores")
# # # picam2.configure(video_config)

# # # encoder = H264Encoder(10000000)

# # # picam2.start_recording(encoder, 'test.h264')
# # # time.sleep(5)

# # # It's better to capture the still in this thread, not in the one driving the camera.
# # request = picam2.capture_request()
# # request.save("main", "testTODAY.jpg")
# # request.release()
# # print("Still image captured!")

# # # time.sleep(5)
# # # picam2.stop_recording()

import time
import subprocess

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput

# Function to create ffmpeg command for streaming video to YouTube
def create_ffmpeg_command(input_file, stream_key):
    return [
        "ffmpeg",
        "-re",
        "-i", input_file,
        "-c:v", "copy",
        "-f", "flv",
        f"rtmp://x.rtmp.youtube.com/live2/{stream_key}"
    ]

def create_string(input_file, stream_key):
    return "ffmpeg -re -i " + input_file + " -c:v copy -f flv rtmp://x.rtmp.youtube.com/live2/" + stream_key

def create_ff2(input_file, stream_key):
    return [
        "-i", input_file,
        "-re",
        "-c:v", "copy",
        "-f", "flv",
        f"rtmp://x.rtmp.youtube.com/live2/{stream_key}"
    ]

# Function to execute ffmpeg command
def execute_command(ffmpeg_command):
    print("before 2")
    process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print("after 2")

    if process.returncode != 0:
        print(f"Error occurred: {stderr.decode()}")
    else:
        print(stdout.decode())

    return process

# Start recording
picam2 = Picamera2()
video_config = picam2.create_video_configuration()
picam2.configure(video_config)

encoder = H264Encoder(10000000)

# Stream the recorded video to YouTube
stream_key = "dktr-20au-bqkh-3gac-cy62"  # replace this with your actual stream key
ffmpeg_command = create_ffmpeg_command("test.mp4", stream_key)
ff2 = create_ff2("test.mp4", stream_key)
#execute_command(ffmpeg_command)

string_command = create_string("test.mp4", stream_key)
output = FfmpegOutput(string_command, audio=True)


print("before")
picam2.start_recording(encoder, execute_command(ff2))
print("after")
time.sleep(3)


request = picam2.capture_request()
request.save("main", "stillCapture.jpg")
request.release()
print("Capturing image")


time.sleep(30)
picam2.stop_recording()