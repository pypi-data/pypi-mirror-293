import os
import re

import imageio
import numpy as np


def _natural_sort_key(s):
    """
    Key function for natural sorting.
    """
    return [int(text) if text.isdigit() else text.lower() for text in re.split("([0-9]+)", s)]


def video_to_image(video_path, image_folder, type="png", stride=1, clear=True):
    video = imageio.get_reader(video_path)

    os.makedirs(image_folder, exist_ok=True)

    if clear:
        os.system(f"rm -rf {image_folder}")
        os.makedirs(image_folder, exist_ok=True)

    for frame_number, frame_data in enumerate(video):
        if frame_number % stride != 0:
            continue
        imageio.imwrite(os.path.join(image_folder, f"{frame_number}.{type}"), frame_data)

    print(f"Total {frame_number + 1} frames, saved {(frame_number + 1) // stride} frames")


def video_to_array(video_path, stride=1):
    """
    Return a numpy array, shape as B * H * W * C
    """
    video = imageio.get_reader(video_path)

    images = []
    for frame_number, frame_data in enumerate(video):
        if frame_number % stride != 0:
            continue
        images.append(frame_data)

    # TODO support for tensor
    return np.array(images)


def image_to_video(video_name, image_path=None, images=None, fps=30, stride=1):
    if images is None:
        files = os.listdir(image_path)
        files = sorted([f for f in files if f.endswith((".png", ".jpg", ".jpeg"))], key=_natural_sort_key)
        images = []
        for image_file in files:
            image_path = os.path.join(image_path, image_file)
            images.append(imageio.imread(image_path))

        images = images[::stride]

    out = imageio.get_writer(video_name, fps=fps)

    for img in images:
        out.append_data(img)
    out.close()
