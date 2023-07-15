import subprocess

bee_host = "10.54.0.210"
bee_username = "picam"
bee_password = "tract0rSpy2.1"

destination = r"C:\Users\flcin\Documents"
folder_file = "/home/pi/Desktop/timelapsestorage" # whole folder
image_file = "/home/pi/Desktop/timelapsestorage/0firstImage.jpg" # one image at a time

newcommand = ["sshpass", "-p", bee_password, "scp", "-r", image_file, f"{bee_username}@{bee_host}:{destination}"]

completed_process = subprocess.run(newcommand, text=True, capture_output=True)