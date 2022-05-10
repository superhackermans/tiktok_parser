import os
import subprocess
from datetime import datetime
import json

# milliseconds_buffer = '5'
vid_dir_in = "./files/INPUT/"
vid_dir_out = "./files/OUTPUT/"

file_suffix = ".mp4"


def input_to_output_filename(filename, filesuffix):
    dot_index = filename.rfind(".")
    return filename[:dot_index] + filesuffix


def before_last_colon(time):
    dot_index = time.rfind(":")
    return time[:dot_index]


def after_dot(time):
    dot_index = time.rfind(".")
    return time[dot_index:]


def before_dot(time):
    dot_index = time.rfind(".")
    return time[:dot_index]


def force_time_format(time):
    # force format into 00:00:00.00
    correct_time_format = '%H:%M:%S.%f'
    while True:
        try:
            datetime.strptime(time, correct_time_format)
            return time
        except ValueError:
            # '%M:%S'
            if time.count(":") == 1 and '.' not in time:
                time = f"{time}.00"
                if len(time) < 8:
                    time = time.zfill(8)
                else:
                    pass
            # '%M:%S.%f'
            elif time.count(":") == 1 and '.' in time:
                if len(before_last_colon(time)) == 1:
                    time = f"0{time}"
                    time = f"00:{time}"
                else:
                    time = f"00:{time}"
            # '%H:%M:%S' -> add %f
            elif time.count(":") == 2 and '.' not in time:
                if len(before_last_colon(before_last_colon(time))) == 1:
                    time = f"0{time}.00"
                else:
                    time = f"{time}.00"
            elif time.count(":") < 2 and '.' not in time:
                time = f"{time}.00"
            elif time.count(":") == 0 and '.' in time:
                if len(before_dot(time)) == 1:
                    time = f"0{time}"
                else:
                    time = f"00:{time}"
            elif time.count(":") == 2 and '.' in time:
                if len(before_last_colon(before_last_colon(time))) == 1:
                    time = f"0{time}"


def trim(time_segment, directory):
    # print("Time segments to trim:")
    input_times = time_segment
    # input_times = "1:15:40-01:15:42, 15:45 - 15:55, 16:00 - 16:07"
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

        start_time = force_time_format(time[0])
        end_time = force_time_format(time[1])

        fmt = '%H:%M:%S.%f'
        tdelta = str(datetime.strptime(end_time, fmt) - datetime.strptime(start_time, fmt))

        input_file = f"{vid_dir_in}{video}"
        assert input_file != None, "No Input File Detected"
        # temp_file = f"{vid_dir_out}{times}temp{file_suffix}"
        output_file = f"{vid_dir_out}{times}{file_suffix}"

        command = f"ffmpeg -y -ss {start_time} -i {input_file} -to {tdelta} -c:v copy -c:a copy {output_file} " \
                  "-hide_banner -loglevel error "
        subprocess.call(command, shell=True)
        # command = f"ffmpeg -i {temp_file} -af apad -c:v copy <audio encoding params> -shortest -avoid_negative_ts " \
        #           f"make_zero -fflags +genpts {output_file} -hide_banner -loglevel error "
        # subprocess.call(command, shell=True)


def concat(directory):
    global newly_trimmed_clip
    video_files = []
    for file in os.listdir(directory):
        if file.endswith(".MP4") or file.endswith(".mp4") and "FINAL" not in file:
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

    concated_output_file = f"{directory}FINAL{video_files[0]}"
    temp_file = f"{vid_dir_in}TEMP{newly_trimmed_clip}"
    # concatenate
    command = f"ffmpeg -y -f concat -safe 0 -i {text_file} -c:v copy -c:a copy {temp_file} -hide_banner -loglevel error"
    subprocess.call(command, shell=True)
    # remove first black frame
    command = f'ffmpeg -y -i {temp_file} -vf select="gte(n\, 1)" {concated_output_file} -hide_banner -loglevel error'
    subprocess.call(command, shell=True)
    os.remove(text_file)
    os.remove(temp_file)

    for newly_trimmed_clip in video_files:
        os.remove(f"{directory}{newly_trimmed_clip}")


def move_and_crop_file(directory):
    width = 1080
    height = 1880 # originally 1920
    startx = 1380
    starty = 138
    video_files = []
    for file in os.listdir(directory):
        if file.endswith(".MP4") or file.endswith(".mp4") and "FINAL" in file and "cropped" not in file:
            video_files.append(file)
    if not video_files:
        print("No input video detected")
    video_files = sorted(video_files)

    for video in video_files:
        input_file = f"{directory}{video}"
        output_file = f"{directory}{video}".replace('cropped', '')
        command = f'ffmpeg -y -i {input_file} -filter:v "crop={width}:{height}:{startx}:{starty}" {output_file}'
        subprocess.call(command, shell=True)
        os.remove(input_file)


def run():
    print("What are the time segments?")
    time_segments = input()
    # if the input is a list of time segments, load as lists. else just one at a time.
    if time_segments[0] == "[":
        time_segments = json.loads(time_segments)
        for time_segment in time_segments:
            trim(time_segment, vid_dir_in)
        concat(vid_dir_out)
    else:
        trim(time_segments, vid_dir_in)
        concat(vid_dir_out)
    #
    move_and_crop_file(vid_dir_out)


if __name__ == '__main__':
    run()

["15:28 - 15:40, 15:45 - 15:55, 16:00 - 16:07", "8:44 - 8:52, 9:20 - 9:35, 9:47 - 10:01", "25:21 - 25:26, 25:33 - 25:39, 26:00 - 26:19, 26:30 - 26:38"]