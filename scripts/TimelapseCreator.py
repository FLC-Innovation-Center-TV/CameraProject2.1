import cv2
import glob
import os
import imageio
import numpy as np
from pathlib import Path

class TimelapseCreator:

    def __init__(self, root_directory, output_directory, fps=24):
        self.root_directory = root_directory
        self.output_directory = output_directory
        self.fps = fps

    def _get_sorted_images(self, directory):
        file_list = sorted(glob.glob(f'{directory}/*.jpg'), key=os.path.getmtime)
        return [cv2.imread(file) for file in file_list]

    def _create_mp4(self, directory, img_array):
        output_filename = os.path.join(self.output_directory, directory.replace(self.root_directory, '').lstrip(os.sep))
        os.makedirs(os.path.dirname(output_filename), exist_ok=True)
        
        mp4_filename = f'{output_filename}.mp4'
        if Path(mp4_filename).is_file():
            print(f"MP4 {mp4_filename} already exists. Skipping...")
            return

        height, width, layers = img_array[0].shape
        size = (width, height)
        out = cv2.VideoWriter(mp4_filename, cv2.VideoWriter_fourcc(*'mp4v'), self.fps, size)
        for img in img_array:
            out.write(img)
        out.release()

    def _create_gif(self, directory, img_array):
        output_filename = os.path.join(self.output_directory, directory.replace(self.root_directory, '').lstrip(os.sep))
        
        gif_filename = f'{output_filename}.gif'
        if Path(gif_filename).is_file():
            print(f"GIF {gif_filename} already exists. Skipping...")
            return

        imageio.mimsave(gif_filename, [cv2.cvtColor(img, cv2.COLOR_BGR2RGB) for img in img_array], fps=self.fps)

    def create_timelapses(self):
        for root, dirs, files in os.walk(self.root_directory):
            if files:  # only process directories that have files
                img_array = self._get_sorted_images(root)
                if img_array:  # only process directories that have images
                    self._create_mp4(root, img_array)
                    self._create_gif(root, img_array)


# usage
creator = TimelapseCreator('/home/pi/Desktop/timelapsestorage', '/home/pi/Desktop/gif_mp4_test', fps=24)
creator.create_timelapses()
