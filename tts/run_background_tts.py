import subprocess
import os
import sys
import time

# Paths
# Use relative paths based on script location to ensure portability
current_script_dir = os.path.dirname(os.path.abspath(__file__))
# Toolkit root is one level up from the 'tts' folder
toolkit_root = os.path.dirname(current_script_dir)

# If running from a venv, try to find the python executable
if sys.prefix != sys.base_prefix:
    if sys.platform == 'win32':
        venv_python = os.path.join(sys.prefix, "Scripts", "python.exe")
    else:
        venv_python = os.path.join(sys.prefix, "bin", "python")
else:
    venv_python = sys.executable

script_to_run = os.path.join(current_script_dir, "tts_book.py")
log_file = os.path.join(toolkit_root, "synthesis.log")
status_file = os.path.join(toolkit_root, "SYNTHESIS_STATUS.txt")

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
            cwd=toolkit_root, # Run from root to find book.md, onnx/ etc
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
