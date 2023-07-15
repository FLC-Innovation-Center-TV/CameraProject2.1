import subprocess

pi_host = "10.54.0.210"
pi_username = "picam"
pi_password = "tract0rSpy2.1"

remote_file = r"C:\Users\flcin\Documents"
local_file = "/home/pi/Desktop/timelapsestorage" # whole folder
image = "/home/pi/Desktop/timelapsestorage/0firstImage.jpg" # one image at a time

newcommand = ["sshpass", "-p", pi_password, "scp", "-r", local_file, f"{pi_username}@{pi_host}:{remote_file}"]

completed_process = subprocess.run(newcommand, input=pi_password, text=True, capture_output=True)