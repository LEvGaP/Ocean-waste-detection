
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

def load_total_label_map():
    command = ["curl", "https://drive.usercontent.google.com/download?id=1hGpT4UYSNtfEXayuzcRJzE5XkFVRVd3m&confirm=xxx", "-o", "total_label_map.json"]
    run_console_command_with_life_output(command)
    pass

# from threaded_loader import ThreadedLoader

def load_photos():
    ThreadedLoader.get_instance().download_folder_threaded('photos')
    pass