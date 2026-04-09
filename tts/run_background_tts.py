import subprocess
import os
import sys
import time

# Paths
workdir = r"C:\Users\mwyant\OneDrive\Falstar Publishing Dev\local-tts-poc"
venv_python = os.path.join(workdir, "venv", "Scripts", "python.exe")
script_to_run = os.path.join(workdir, "tts_book.py")
log_file = os.path.join(workdir, "synthesis.log")
status_file = os.path.join(workdir, "SYNTHESIS_STATUS.txt")

def log_status(message):
    with open(status_file, "w") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
    print(message)

def run_background():
    log_status("Starting background synthesis process...")
    
    # We use subprocess.Popen to launch and NOT wait
    # Redirecting both stdout and stderr to the log file
    with open(log_file, "a") as log:
        process = subprocess.Popen(
            [venv_python, script_to_run],
            cwd=workdir,
            stdout=log,
            stderr=log,
            creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
        )
    
    log_status(f"Synthesis started with PID {process.pid}. Monitor '{log_file}' for details.")
    
    # Simple monitoring loop in this script (optional, but good for reporting back once)
    # Actually, the user wants me to start it and NOT monitor until done.
    # So I'll just start it and exit.

if __name__ == "__main__":
    run_background()
