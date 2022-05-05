import os
import subprocess
from datetime import datetime

# milliseconds_buffer = '5'
vid_dir_in = "./files/INPUT/"
vid_dir_out = "./files/OUTPUT/"
width = 0
height = 0
startx = 0
starty = 0

file_suffix = ".mp4"


def input_to_output_filename(filename, filesuffix):
    dot_index = filename.rfind(".")
    return filename[:dot_index] + filesuffix


def find_colon(time):
    dot_index = time.rfind(":")
    return time[:dot_index]


def force_time_format(time):
    # force format into 00:00:00.00
    incorrect_time_formats = ['%H:%M:%S', '%M:%S.%f', '%M:%S']
    while time:
        pass


def trim(directory):
    print("Time segments to trim:")
    # input_times = input()
    input_times = "6:28 - 1:15:40.25, 15:45 - 15:55, 16:00 - 16:07"
    input_times = input_times.replace(" ", "")  # remove spaces
    times_to_cut = input_times.split(",")  # split into

    video_files = []

    for file in os.listdir(directory):
        if file.endswith(".MP4") or file.endswith(".mp4"):
            video_files.append(file)
    if not video_files:
        print("No input video detected")
    video = video_files[0]
    video_loc = f"{vid_dir_in}{video}"
    os.rename(video_loc, video_loc.replace(" ", ""))  # remove spaces from file name
    video = video.replace(" ", "")

    for times in times_to_cut:
        time = times.split("-")

        start_time = time[0]
        end_time = time[1]

        # if len(findcolon(start_time)) == 1:
        #     findcolon(start_time).zfill(2)

        # # match start_time and end_time to correct formatting
        # if '.' in start_time:
        #     start_time = start_time.ljust(11, '0')
        # else:
        #     start_time = f"{start_time}.00"

        fmt = '%H:%M:%S.%f'
        tdelta = str(datetime.strptime(end_time, fmt) - datetime.strptime(start_time, fmt))

        input_file = f"{vid_dir_in}{video}"
        assert input_file != None, "No Input File Detected"
        output_file = f"{vid_dir_out}{times}{file_suffix}"

        command = f"ffmpeg -y -ss {start_time} -i {input_file} -to {tdelta} -c:v copy -c:a copy {output_file} -hide_banner -loglevel error "
        subprocess.call(command, shell=True)


def concat(directory):
    global newly_trimmed_clip
    video_files = []
    for file in os.listdir(directory):
        if file.endswith(".MP4") or file.endswith(".mp4"):
            video_files.append(file)
    if not video_files:
        print("No input video detected")
    video_files = sorted(video_files)
    text_file = 'concat_clips.txt'

    for newly_trimmed_clip in video_files:
        # with open(text_file, 'w') as fp:
        #     pass
        trimmed_clip_loc = f"{directory}{newly_trimmed_clip}"

        # write it into the text file
        with open("concat_clips.txt", "a") as file:
            file.write(f"file '{trimmed_clip_loc}'\n")

    concated_output_file = f"{directory}full{video_files[0]}"
    temp_file = input_file = f"{vid_dir_in}{newly_trimmed_clip}TEMP{file_suffix}"
    # concatenate
    command = f"ffmpeg -y -f concat -safe 0 -i {text_file} -c:v copy -c:a copy {temp_file} -hide_banner -loglevel error"
    subprocess.call(command, shell=True)
    # remove first black frame
    command = f'ffmpeg -i {temp_file} -vf select="gte(n\, 1)" {concated_output_file} -hide_banner -loglevel error'
    subprocess.call(command, shell=True)
    os.remove(text_file)
    os.remove(temp_file)

    for newly_trimmed_clip in video_files:
        os.remove(newly_trimmed_clip)


# def crop_file(directory):
#     command = f'ffmpeg -i {input_file} -filter:v "crop=out_{width}:out_{height}:{startx}:{starty}" {output_file}'
#     subprocess.call(command, shell=True)


if __name__ == '__main__':
    trim(vid_dir_in)
    concat(vid_dir_out)
    # crop_file(vid_dir_in)

# Video 1 - What surprised you about your MBA experience?
# 15:28 - 15:40, 15:45 - 15:55, 16:00 - 16:07
# Video 2 - HBS’ culture
# 8:44 - 8:52, 9:20 - 9:35, 9:47 - 10:01
# Video 3 - Any HBS essay tips?
# 25:21 - 25:26, 25:33 - 25:39, 26:00 - 26:19, 26:30 - 26:38'
