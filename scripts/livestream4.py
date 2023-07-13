# import time
# from picamera2.outputs import FfmpegOutput
# from picamera2.encoders import H264Encoder, Quality
# from picamera2 import Picamera2


# picam2 = Picamera2()
# picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
# encoder = H264Encoder(bitrate=1000000, repeat=True, iperiod=15)
# output = FfmpegOutput("-f hls -hls_time 4 -hls_list_size 5 -hls_flags delete_segments -hls_allow_cache 0 stream.m3u8")
# picam2.start_recording(encoder, output)
# time.sleep(9999999)
# import time
# from picamera2.outputs import FfmpegOutput
# from picamera2.encoders import H264Encoder, Quality
# from picamera2 import Picamera2

# def create_ffmpeg_command(stream_key):
#     return "rtmp://x.rtmp.youtube.com/live2/{}".format(stream_key)

# stream_key = "dktr-20au-bqkh-3gac-cy62"
# ffmpeg_cmd = create_ffmpeg_command(stream_key)

# # print(create_ffmpeg_command(stream_key))
# picam2 = Picamera2()
# picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
# encoder = H264Encoder(bitrate=4500000, repeat=True, iperiod=40)
# output = FfmpegOutput(ffmpeg_cmd, audio = True)
# picam2.start_recording(encoder, output)
# time.sleep(9999999)

# import time
# from picamera2.outputs import FfmpegOutput
# from picamera2.encoders import H264Encoder, Quality
# from picamera2 import Picamera2

# def create_ffmpeg_command(stream_key):
#     return "-re -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 -i pipe:0 -c:v copy -c:a aac -f flv rtmp://x.rtmp.youtube.com/live2/{}".format(stream_key)

# stream_key = "dktr-20au-bqkh-3gac-cy62"
# ffmpeg_cmd = create_ffmpeg_command(stream_key)

# picam2 = Picamera2()
# picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
# encoder = H264Encoder(bitrate=4500000, repeat=True, iperiod=40)
# output = FfmpegOutput(ffmpeg_cmd, audio = True)
# picam2.start_recording(encoder, output)
# time.sleep(9999999)

import time
from picamera2.outputs import FfmpegOutput
from picamera2.encoders import H264Encoder, Quality
from picamera2 import Picamera2

def create_ffmpeg_command(stream_key):
    # This command will push a live stream to the specified YouTube RTMP URL
    return "-f flv rtmp://x.rtmp.youtube.com/live2/{}".format(stream_key)

stream_key = "dktr-20au-bqkh-3gac-cy62"
ffmpeg_cmd = create_ffmpeg_command(stream_key)

picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
encoder = H264Encoder(bitrate=4500000, repeat=True, iperiod=40)

# Creating FfmpegOutput instance with the specified command and audio parameters
output = FfmpegOutput(ffmpeg_cmd, audio=True, audio_device="default", audio_sync=-0.3, audio_samplerate=48000, audio_codec="aac", audio_bitrate=128000)

picam2.start_recording(encoder, output)
time.sleep(10)

for i in range(10):
    request = picam2.capture_request()
    request.save("main", f"stillCapture{i}.jpg")
    request.release()
    print(f"Captured image {i+1}")
    time.sleep(6)

time.sleep(9999999)

