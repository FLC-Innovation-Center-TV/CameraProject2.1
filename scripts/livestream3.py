import os
import time
import threading
from PIL import Image
import subprocess
from picamera2 import Picamera2

# These two are only needed for the demo code below the FrameServer class.

from threading import Condition, Thread




class FrameServer:
    def __init__(self, picam2, stream='main'):
        """A simple class that can serve up frames from one of the Picamera2's configured streams to multiple other threads.

        Pass in the Picamera2 object and the name of the stream for which you want
        to serve up frames.
        """
        self._picam2 = picam2
        self._stream = stream
        self._array = None
        self._condition = Condition()
        self._running = True
        self._count = 0
        self._thread = Thread(target=self._thread_func, daemon=True)

    @property
    def count(self):
        """A count of the number of frames received."""
        return self._count

    def start(self):
        """To start the FrameServer, you will also need to start the Picamera2 object."""
        self._thread.start()

    def stop(self):
        """To stop the FrameServer

        First stop any client threads (that might be
        blocked in wait_for_frame), then call this stop method. Don't stop the
        Picamera2 object until the FrameServer has been stopped.
        """
        self._running = False
        self._thread.join()

    def _thread_func(self):
        while self._running:
            array = self._picam2.capture_array(self._stream)
            self._count += 1
            with self._condition:
                self._array = array
                self._condition.notify_all()

    def wait_for_frame(self, previous=None):
        """You may optionally pass in the previous frame that you got last time you called this function.

        This will guarantee that you don't get duplicate frames
        returned in the event of spurious wake-ups, and it may even return more
        quickly in the case where a new frame has already arrived.
        """
        with self._condition:
            if previous is not None and self._array is not previous:
                return self._array
            while True:
                self._condition.wait()
                if self._array is not previous:
                    return self._array


# Function to capture time-lapse images
def time_lapse(server, interval, path):
    frame = None
    while True:
        frame = server.wait_for_frame(frame)
        image = Image.fromarray(frame)
        image.save(os.path.join(path, f'image_{time.time()}.jpg'))
        time.sleep(interval)

# Create commands
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
    return [
        "ffmpeg",
        "-re",
        # "-ar", str(audio_rate),
        # "-ac", str(audio_channels),
        "-acodec", audio_codec,
        "-f", format,
        # "-ac", str(audio_channels),
        # "-i", "/dev/zero",
        "-i", "pipe:0",
        "-c:v", "copy",
        "-b:v", str(bit_rate),
        "-f", flv_format,
        f"rtmp://x.rtmp.youtube.com/live2/{stream_key}"
    ]

# Execute commands
def execute_commands(libcamera_vid_command, ffmpeg_command, frame_server, time_lapse_interval, image_path):
    try:
        # Launch the libcamera_vid subprocess
        libcamera_vid_process = subprocess.Popen(libcamera_vid_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Launch the ffmpeg subprocess that takes the output of libcamera_vid_process
        ffmpeg_process = subprocess.Popen(ffmpeg_command, stdin=libcamera_vid_process.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        libcamera_vid_process.stdout.close()  # Make sure libcamera_vid_process.stdout is closed so ffmpeg_process reads EOF.

        # Start the FrameServer and the time-lapse thread
        frame_server.start()
        time_lapse_thread = threading.Thread(target=time_lapse, args=(frame_server, time_lapse_interval, image_path))
        time_lapse_thread.start()

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

# Configure and start everything
stream_key = "dktr-20au-bqkh-3gac-cy62"  # replace this with your actual stream key
libcamera_vid_command = create_libcamera_vid_command(1920, 1080, 30, 40)
ffmpeg_command = create_ffmpeg_command(stream_key, 44100, 2, "pcm_s16le", "s16le", 4500000, "flv")

picam2 = Picamera2()
server = FrameServer(picam2)
time_lapse_interval = 5  # Change this to the desired interval between photos
image_path = "/home/pi/Desktop/"  # Change this to the directory where you want to save the images

execute_commands(libcamera_vid_command, ffmpeg_command, server, time_lapse_interval, image_path)
