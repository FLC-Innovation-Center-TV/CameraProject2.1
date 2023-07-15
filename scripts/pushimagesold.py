import subprocess

def transfer_folder_with_scp(src_folder, dest_username, dest_ip, dest_path):
    try:
        scp_command = ["scp", "-r", src_folder, f"{dest_username}@{dest_ip}:{dest_path}"]
        # scp -r /home/pi/Desktop/timelapsestorage picam@10.54.0.210:C:\Users\flcin\Documents 
        subprocess.run(scp_command, check=True)

        print("Folder transfer completed successfully.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred during folder transfer: {str(e)}")


src_folder = "/home/pi/Desktop/timelapsestorage"
beelink_username = "picam"
beelink_ip = "10.54.0.210"
# dest_path = "C:\Users\flcin\Documents"
dest_path = r"C:\Users\flcin\Documents"
ssh_password = "tract0rSpy2.1"

# ssh-keygen -t rsa -b 2048
# ssh-copy-id picam@10.54.0.210


transfer_folder_with_scp(src_folder, beelink_username, beelink_ip, dest_path)

# import subprocess

# def transfer_folder_with_scp(src_folder, dest_username, dest_ip, dest_path, ssh_password):
#     try:
#         sshpass_command = ["sshpass", "-p", ssh_password]
#         ssh_command = ["ssh", f"{dest_username}@{dest_ip}", f"mkdir -p {dest_path}"]

#         subprocess.run(sshpass_command + ssh_command, check=True)

#         scp_command = ["scp", "-r", src_folder, f"{dest_username}@{dest_ip}:{dest_path}"]
#         subprocess.run(sshpass_command + scp_command, check=True)

#         print("Folder transfer completed successfully.")

#     except subprocess.CalledProcessError as e:
#         print(f"An error occurred during folder transfer: {str(e)}")


# src_folder = "/home/pi/Desktop/timelapsestorage"
# beelink_username = "picam"
# beelink_ip = "10.54.0.210"
# dest_path = r"C:\Users\flcin\Documents"
# ssh_password = "tract0rSpy2.1"

# transfer_folder_with_scp(src_folder, beelink_username, beelink_ip, dest_path, ssh_password)

# import subprocess

# def transfer_folder_with_scp(src_folder, dest_username, dest_ip, dest_path, ssh_password):
#     try:
#         sshpass_command = 'sshpass -p ' + ssh_password
#         ssh_command = "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null " + dest_username + "@" + dest_ip + " mkdir -p " + dest_path

#         full_command = sshpass_command + ' ' + ssh_command
#         subprocess.run(full_command, shell=True, check=True)

#         scp_command = "scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -r " + src_folder + ' ' + dest_username + "@" + dest_ip + ":" + dest_path

#         full_scp_command = sshpass_command + ' ' + scp_command
#         subprocess.run(full_scp_command, shell=True, check=True)

#         print("Folder transfer completed successfully.")

#     except subprocess.CalledProcessError as e:
#         print(f"An error occurred during folder transfer: {str(e)}")


# src_folder = "/home/pi/Desktop/timelapsestorage"
# beelink_username = "picam"
# beelink_ip = "10.54.0.210"
# dest_path = "/home/picam/Documents"  # adjusted the path to match Unix-like convention
# ssh_password = "tract0rSpy2.1"

# transfer_folder_with_scp(src_folder, beelink_username, beelink_ip, dest_path, ssh_password)
