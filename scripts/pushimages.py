import subprocess

def send_files_with_rsync(src_path, dest_username, dest_ip, dest_path):
    try:
        command = f"rsync -avz -e ssh {src_path} {dest_username}@{dest_ip}:{dest_path}"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        if process.returncode != 0:
            raise Exception("Error occurred while sending files.")
    except Exception as e:
        print(f"An error occurred while sending files: {str(e)}")

src_path = "/home/pi/Desktop/timelapsestorage/"
beelink_username = "picam"
beelink_ip = "10.54.0.210"
dest_path = "/mnt/c/Users/flcin/Documents"

send_files_with_rsync(src_path, beelink_username, beelink_ip , dest_path)

picam123
tract0rSpy2.1
tract0