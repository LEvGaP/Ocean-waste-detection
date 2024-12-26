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
