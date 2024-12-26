# from threaded_loader import ThreadedLoader
from console_helpers import run_console_command_with_life_output


def load_total_label_map():
    command = ["curl", "https://drive.usercontent.google.com/download?id=1hGpT4UYSNtfEXayuzcRJzE5XkFVRVd3m&confirm=xxx", "-o", "total_label_map.json"]
    run_console_command_with_life_output(command)
    pass
