# Use the official Python image from the Docker Hub
FROM python:3.9

# Install dependencies
RUN apt-get update && apt-get install -y \
    libsm6 libxext6 libxrender-dev ffmpeg sshpass libcap-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /CameraProject2.1

# Copy the requirements.txt file into our work directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Set a volume for the project directory
VOLUME /CameraProject2.1

# Run the command
CMD ["python", "scripts/main.py"]

