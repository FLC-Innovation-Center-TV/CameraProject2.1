import os

if __name__ == "__main__":
    max_size = 40000
    uploaded = "C:\\test\\uploaded"
    total_size = 0
    for folder, _, images in os.walk(uploaded):
        for image_name in images:
            image_path = os.path.join(folder, image_name)
            image_size = os.path.getsize(image_path)
            total_size += image_size
            print("Image:", image_path, "Size:", image_size)
    if(total_size <= max_size):
        print(f"Total size of backup images: ({total_size} bytes) is under the maximum size of ({max_size} bytes).\nNo deletion needed.")
        exit()
    print(f"Total size of backup images: ({total_size} bytes) exceeds the maximum size of ({max_size} bytes).\nDeleting oldest images to clear up space.")
    for folder, _, images in os.walk(uploaded):
        for image_name in images:
            if(total_size <= 40000):
                exit()
            oldest_image_path = os.path.join(folder, image_name)
            oldest_image_size = os.path.getsize(oldest_image_path)
            os.remove(oldest_image_path)
            total_size -= oldest_image_size
            print(f"Deleted {image_name} ({oldest_image_size} bytes). New total is now: ({total_size} bytes).")