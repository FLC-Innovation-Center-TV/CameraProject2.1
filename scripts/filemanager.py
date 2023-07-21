import os
from datetime import datetime

root = "C:\\test"

def upload_images():
    
    unuploaded = "C:\\test\\unuploaded"
    uploaded = "C:\\test\\uploaded"

    for folder, _, images in os.walk(unuploaded):
        for image_name in images:
            upload_successful = True
            if(upload_successful):
                print("Uploaded an image")

                date = os.path.relpath(folder, unuploaded)

                old_day_folder = os.path.join(unuploaded, date)
                new_day_folder = os.path.join(uploaded, date)

                old_image_path = os.path.join(old_day_folder, image_name)
                new_image_path = os.path.join(new_day_folder, image_name)

                os.makedirs(new_day_folder, exist_ok=True)
                try:
                    os.rename(old_image_path, new_image_path)
                except:
                    print("Failed to transfer image to backup, likely because there's already an image with the exact same name.")
            else:
                print("Upload failed")
                return


def simulate_save_image():
    image_storage_path = "C:\\test\\unuploaded"
    """
    Function to save image in the save directory with a timestamp.
    """
    # Use datetime to get current year, month, and day
    now = datetime.now()
    year, month, day = now.strftime('%Y'), now.strftime('%m'), now.strftime('%d')

    # Append year, month, and day to your image storage path
    save_directory = os.path.join(image_storage_path, year, month, day)

    # Create directory if it doesn't exist
    os.makedirs(save_directory, exist_ok=True)
    
    timestamp = now.strftime('%Y%m%d_%H%M%S')  # e.g., '20230627_142536'
    file_name = f"{timestamp}.jpg"
    file_path = os.path.join(save_directory, file_name)
    
    # Simulate capturing an image by transfering the first image in this folder
    test_images_path = "C:\\test\\testimages"
    test_images = os.listdir(test_images_path)
    if test_images:
        image_path = os.path.join(test_images_path, test_images[0])
        os.rename(image_path, file_path)
        print("Saving a new image")
    else:
        print("No test images exist.")

    #request = self.picam2.capture_request()
    #request.save("main", file_path)
    #request.release()

    return file_path

if __name__ == "__main__":
    image_path = "C:\\test\\testimages\\image.jpg"
    simulate_save_image()
    upload_images()