# import subprocess

# stream_key = "dktr-20au-bqkh-3gac-cy62"  # replace this with your actual stream key

# # command = [
# #     "libcamera-vid",
# #     "-t", "0",
# #     "-g", "10",
# #     "--bitrate", "4500000",
# #     "--inline",
# #     "--width", "1920",
# #     "--height", "1080",
# #     "--framerate", "30",
# #     "--rotation", "0",
# #     "--codec", "libav",
# #     "--libav-format", "flv",
# #     "--libav-audio",
# #     "--audio-bitrate", "192000",
# #     "--av-sync", "200000",
# #     "-n",
# #     "-o", f"rtmp://x.rtmp.youtube.com/live2/{stream_key}"
# # ]
# #-ar 44100 -ac 2 -acodec pcm_s16le -f s16le -ac 2 -i /dev/zero
# command = [
#     "libcamera-vid",
#     "-o", "-",
#     "-t", "0",
#     "--width", "1920",
#     "--height", "1080",
#     "--brightness", "0.1",
#     "--inline",
#     "--framerate", "30",
#     "-g", "50",
#     "|",
#     "ffmpeg",
#     "-ar", "44100",
#     "-ac", "2",
#     "-acodec", "pcm_s16le",
#     "-f", "s16le",
#     "-ac", "2",
#     "-i", "/dev/zero",
#     "-thread_queue_size", "1024",
#     "-i", "pipe:0",
#     "-c:v", "copy",
#     "-b:v", "4500000",
#     "-f", "flv",
#     "rtmp://x.rtmp.youtube.com/live2/mykey"
# ]

    
# try:
#     process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     stdout, stderr = process.communicate()
# except subprocess.TimeoutExpired:
#     print("Error: Command execution exceeded the timeout.")
# except subprocess.SubprocessError as e:
#     print(f"An error occurred while executing the subprocess: {str(e)}")
# else:
#     if process.returncode != 0:
#         print(f"Error occurred: {stderr.decode()}")
#     else:
#         print(stdout.decode())

####################################
# no function versoin this works   #
####################################

# import subprocess

# stream_key = "dktr-20au-bqkh-3gac-cy62"  # replace this with your actual stream key

# libcamera_vid_command = [
#     "libcamera-vid",
#     "-o", "-",
#     "-t", "0",
#     "--width", "1920",
#     "--height", "1080",
#     # "--brightness", "0.1",
#     # "--inline",
#     "--framerate", "30",
#     "-g", "40"
# ]

# ffmpeg_command = [
#     "ffmpeg",
#     "-re",
#     "-ar", "44100",
#     "-ac", "2",
#     "-acodec", "pcm_s16le",
#     "-f", "s16le",
#     "-ac", "2",
#     "-i", "/dev/zero",
#     # "-thread_queue_size", "8192",
#     "-i", "pipe:0",
#     "-c:v", "copy",
#     "-b:v", "4500000",
#     "-f", "flv",
#     f"rtmp://x.rtmp.youtube.com/live2/{stream_key}"
# ]

# try:
#     # Launch the libcamera_vid subprocess
#     libcamera_vid_process = subprocess.Popen(libcamera_vid_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#     # Launch the ffmpeg subprocess that takes the output of libcamera_vid_process
#     ffmpeg_process = subprocess.Popen(ffmpeg_command, stdin=libcamera_vid_process.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     libcamera_vid_process.stdout.close()  # Make sure libcamera_vid_process.stdout is closed so ffmpeg_process reads EOF.

#     # Communicate with the ffmpeg process
#     stdout, stderr = ffmpeg_process.communicate()
# except subprocess.TimeoutExpired:
#     print("Error: Command execution exceeded the timeout.")
# except subprocess.SubprocessError as e:
#     print(f"An error occurred while executing the subprocess: {str(e)}")
# else:
#     if ffmpeg_process.returncode != 0:
#         print(f"Error occurred: {stderr.decode()}")
#     else:
#         print(stdout.decode())


#####################################################
# This streams for at least 4 minutes its called v2 #
#####################################################

# import subprocess

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
#     image_output_path = "/home/pi/Desktop/timelapsestorage2/img%03d.jpg"
#     frame_rate_for_images = "1/25"

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
#         # "-map", "1:v",  # map video from second input
#         # "-vf", f"fps={frame_rate_for_images}",
#         # "-update", "1",
#         # image_output_path,
#         # "-map", "0:a",  # map audio from first input
#         # "-c:v", "copy",
#         "-f", flv_format,
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

#####################################################
# This streams for at least 4 minutes its called v3 #
#####################################################
import subprocess

def create_libcamera_vid_command(width, height, framerate, g_value):
    return [
        "libcamera-vid",
        "-o", "-",
        "-t", "0",
        "--width", str(width),
        "--height", str(height),
        "--framerate", str(framerate),
        "-g", str(g_value)
    ]

def create_ffmpeg_command(stream_key, audio_rate, audio_channels, audio_codec, format, bit_rate, flv_format):
    image_output_path = "/home/pi/Desktop/timelapsestorage2/img%03d.jpg"
    frame_rate_for_images = "1/25"

    return [
        "ffmpeg",
        "-re",
        "-ar", str(audio_rate),
        "-ac", str(audio_channels),
        "-acodec", audio_codec,
        "-f", format,
        "-ac", str(audio_channels),
        "-i", "/dev/zero",
        "-i", "pipe:0",
        "-c:v", "copy",
        "-b:v", str(bit_rate),
        # "-map", "1:v",  # map video from second input
        # "-vf", f"fps={frame_rate_for_images}",
        # "-update", "1",
        # image_output_path,
        # "-map", "0:a",  # map audio from first input
        # "-c:v", "copy",
        "-f", flv_format,
        f"rtmp://x.rtmp.youtube.com/live2/{stream_key}"
    ]


def execute_commands(libcamera_vid_command, ffmpeg_command):
    try:
        # Launch the libcamera_vid subprocess
        libcamera_vid_process = subprocess.Popen(libcamera_vid_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Launch the ffmpeg subprocess that takes the output of libcamera_vid_process
        ffmpeg_process = subprocess.Popen(ffmpeg_command, stdin=libcamera_vid_process.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        libcamera_vid_process.stdout.close()  # Make sure libcamera_vid_process.stdout is closed so ffmpeg_process reads EOF.

        # Communicate with the ffmpeg process
        stdout, stderr = ffmpeg_process.communicate()
    except subprocess.TimeoutExpired:
        print("Error: Command execution exceeded the timeout.")
    except subprocess.SubprocessError as e:
        print(f"An error occurred while executing the subprocess: {str(e)}")
    else:
        if ffmpeg_process.returncode != 0:
            print(f"Error occurred: {stderr.decode()}")
        else:
            print(stdout.decode())


stream_key = "dktr-20au-bqkh-3gac-cy62"  # replace this with your actual stream key
libcamera_vid_command = create_libcamera_vid_command(1920, 1080, 30, 40)
ffmpeg_command = create_ffmpeg_command(stream_key, 44100, 2, "pcm_s16le", "s16le", 4500000, "flv")

execute_commands(libcamera_vid_command, ffmpeg_command)

# def create_ffmpeg_command(stream_key, audio_rate, audio_channels, audio_codec, format, bit_rate, flv_format):
#     image_output_path = "/home/pi/Desktop/timelapsestorage2/img%03d.jpg"
#     frame_rate_for_images = "1/5"

#     return [
#         "ffmpeg",
#         "-re",
#         "-ar", str(audio_rate),
#         "-ac", str(audio_channels),
#         "-acodec", audio_codec,
#         "-f", format,
#         "-i", "/dev/zero",
#         "-i", "pipe:0",
#         "-vf", f"fps={frame_rate_for_images}",
#         "-map", "1:v",  # map video from second input
#         "-c:v", "copy",
#         "-b:v", str(bit_rate),
#         "-update", "1",
#         image_output_path,
#         "-map", "0:a",  # map audio from first input
#         "-c:v", "copy",
#         "-f", flv_format,
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

#         if libcamera_vid_process.returncode != 0:
#             print(f"Error occurred in libcamera_vid process: {stderr.decode()}")
#         if ffmpeg_process.returncode != 0:
#             print(f"Error occurred in ffmpeg process: {stderr.decode()}")

#     except subprocess.TimeoutExpired:
#         print("Error: Command execution exceeded the timeout.")
#     except subprocess.SubprocessError as e:
#         print(f"An error occurred while executing the subprocess: {str(e)}")

# stream_key = "dktr-20au-bqkh-3gac-cy62"  # replace this with your actual stream key
# libcamera_vid_command = create_libcamera_vid_command(1920, 1080, 30, 40)
# ffmpeg_command = create_ffmpeg_command(stream_key, 44100, 2, "pcm_s16le", "s16le", 4500000, "flv")

# execute_commands(libcamera_vid_command, ffmpeg_command)

# import subprocess

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


# # def create_ffmpeg_command(stream_key, audio_rate, audio_channels, audio_codec, format, bit_rate, flv_format):
# #     image_output_path = "/home/pi/Desktop/timelapsestorage2/img%04d.jpg"
# #     frame_rate_for_images = "1/25"

# #     return [
# #         "ffmpeg",
# #         "-re",
# #         "-ar", str(audio_rate),
# #         "-ac", str(audio_channels),
# #         "-acodec", audio_codec,
# #         "-f", format,
# #         "-i", "/dev/zero",
# #         "-i", "pipe:0",
# #         "-vf", f"fps={frame_rate_for_images}",
# #         "-map", "1:v",  # map video from second input
# #         "-c:v", "libx264",  # use libx264 codec for video encoding
# #         "-b:v", str(bit_rate),
# #         "-update", "1",
# #         image_output_path,
# #         "-map", "0:a",  # map audio from first input
# #         "-c:v", "libx264",  # use libx264 codec for video encoding
# #         "-f", flv_format,
# #         f"rtmp://x.rtmp.youtube.com/live2/{stream_key}"
# #     ]

# def create_ffmpeg_command(stream_key, audio_rate, audio_channels, audio_codec, format, bit_rate, flv_format):
#     image_output_path = "/home/pi/Desktop/timelapsestorage2/img%04d.jpg"
#     frame_rate_for_images = "1/500"

#     return [
#         "ffmpeg",
#         "-re",
#         "-ar", str(audio_rate),
#         "-ac", str(audio_channels),
#         "-acodec", audio_codec,
#         "-f", format,
#         "-i", "/dev/zero",
#         "-i", "pipe:0",
#         "-map", "1:v",  # map video from second input
#         "-c:v", "libx264",  # use libx264 codec for video encoding
#         "-b:v", str(bit_rate),
#         "-f", flv_format,
#         f"rtmp://x.rtmp.youtube.com/live2/{stream_key}",
#         # "-map", "1:v",  # map video from second input for image sequence
#         # "-vf", f"fps={frame_rate_for_images}",
#         # "-f", "image2",  # explicitly set the muxer to image2 for image sequence
#         # image_output_path
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

#         if libcamera_vid_process.returncode != 0:
#             print(f"Error occurred in libcamera_vid process: {stderr.decode()}")
#         if ffmpeg_process.returncode != 0:
#             print(f"Error occurred in ffmpeg process: {stderr.decode()}")

#     except subprocess.TimeoutExpired:
#         print("Error: Command execution exceeded the timeout.")
#     except subprocess.SubprocessError as e:
#         print(f"An error occurred while executing the subprocess: {str(e)}")

# # stream_key = "dktr-20au-bqkh-3gac-cy62"  # replace this with your actual stream key
# # libcamera_vid_command = create_libcamera_vid_command(1280, 720, 30, 40)
# # ffmpeg_command = create_ffmpeg_command(stream_key, 44100, 2, "pcm_s16le", "s16le", 4500000, "flv")

# # execute_commands(libcamera_vid_command, ffmpeg_command)

# stream_key = "dktr-20au-bqkh-3gac-cy62"  # replace this with your actual stream key
# libcamera_vid_command = create_libcamera_vid_command(1280, 720, 30, 40)
# ffmpeg_command = create_ffmpeg_command(stream_key, 44100, 2, "pcm_s16le", "s16le", 4500000, "flv")

# execute_commands(libcamera_vid_command, ffmpeg_command)
