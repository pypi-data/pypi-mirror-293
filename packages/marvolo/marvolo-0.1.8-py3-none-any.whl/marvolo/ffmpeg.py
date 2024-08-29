import os


def resize(video, output, height, width):
    height = int(height)
    width = int(width)
    command = f'ffmpeg -i {video} -vf "scale={height}:{width}" {output} -y'
    os.system(command)


def cat_same_size(video1, video2, output, overlay=0):
    overlay = int(overlay)
    command = f'ffmpeg -i {video1} -i {video2} -filter_complex "[0:v]pad=iw*2:ih*1[a];[a][1:v]overlay=w+{overlay}" {output} -y'
    os.system(command)


def change_fps(video, output, new_fps):
    new_fps = int(new_fps)
    command = f"ffmpeg -i {video} -r {new_fps} {output} -y"
    os.system(command)


def split_video(video, output, length):
    command = f"ffmpeg -i {video} -ss 00:00:00 -to {length} {output} -y"
    os.system(command)


if __name__ == "__main__":
    split_video("./a.mp4", "./b.mp4", 2)
