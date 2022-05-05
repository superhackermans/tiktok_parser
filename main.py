import os
import subprocess

vid_dir_in = "./files/INPUT/"
vid_dir_out = "./files/OUTPUT/"

def inputToOutputFilename(filename, filesuffix):
    dotIndex = filename.rfind(".")
    return filename[:dotIndex] + filesuffix



def trim_file(directory):
    print("Time segments to trim:")
    x = input()
    times_to_cut = x.split(",")
    times_to_cut = [x.strip(' ') for x in times_to_cut]

    video_files = []

    for file in os.listdir(directory):
        if file.endswith(".MP4") or file.endswith(".mp4"):
            video_files.append(file)
    if not video_files:
        print("No input videos detected")
    video_files = sorted(video_files)
    print(f"Processing: {video_files[0]} to {video_files[-1]}")

    for video in video_files:
        INPUT_FILE = video
        assert INPUT_FILE != None, "No Input File Detected"
        OUTPUT_FILE = f"{output_dir}{inputToOutputFilename(video)}"

        command = f"ffmpeg -y -i {input} -ss {start_time} -to {end_time} -c:v copy -c:a copy {output} -hide_banner -loglevel error"
        subprocess.call(command, shell=True)

    pass

def crop_file(directory):
    pass


if __name__ == '__main__':
    trim_file(vid_dir_in)
    crop_file(vid_dir_out)

# Video 1 - What surprised you about your MBA experience?
# 15:28 - 15:40, 15:45 - 15:55, 16:00 - 16:07
# Video 2 - HBS’ culture
# 8:44 - 8:52, 9:20 - 9:35, 9:47 - 10:01
# Video 3 - Any HBS essay tips?
# 25:21 - 25:26, 25:33 - 25:39, 26:00 - 26:19, 26:30 - 26:38'