import os
import subprocess

def run_console_command_with_life_output(command: list):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
    finally:
        process.stdout.close()
        process.wait()
    pass

def acquire_model_by_filename(filename: str):
    if not os.path.exists(filename):
        command = ["curl", "https://drive.usercontent.google.com/download?id=1gePNe0mX8qxAL63hvaM7US-KW-mdSr_V&confirm=xxx", "-o", filename]
        run_console_command_with_life_output(command)
    return filename

def acquire_yolo11n_3ep_embset_v1():
    return acquire_model_by_filename('yolo11n_3ep_embset_v1.pt')

def acquire_yolo11n_30ep_embset_v1():
    return acquire_model_by_filename('yolo11n_30ep_embset_v1.pt')