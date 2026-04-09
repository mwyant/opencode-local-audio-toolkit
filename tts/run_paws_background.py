import subprocess
import os
import sys
import time

# Paths
current_script_dir = os.path.dirname(os.path.abspath(__file__))
toolkit_root = os.path.dirname(current_script_dir)

# Explicitly look for the local venv first
local_venv_python = os.path.join(toolkit_root, "venv", "Scripts", "python.exe") if sys.platform == 'win32' else os.path.join(toolkit_root, "venv", "bin", "python")

if os.path.exists(local_venv_python):
    venv_python = local_venv_python
elif sys.prefix != sys.base_prefix:
    if sys.platform == 'win32':
        venv_python = os.path.join(sys.prefix, "Scripts", "python.exe")
    else:
        venv_python = os.path.join(sys.prefix, "bin", "python")
else:
    venv_python = sys.executable

script_to_run = os.path.join(current_script_dir, "tts_book.py")

# Custom log and status files for Paws and Effect
log_file = os.path.join(toolkit_root, "synthesis_paws.log")
status_file = os.path.join(toolkit_root, "SYNTHESIS_STATUS_PAWS.txt")

# Target book and output dir
book_path = r"C:\Users\mwyant\Dropbox\Writing\Books\9_The Misadventures of Darren Whitestone\3_Paws and Effect\PawsAndEffect.v3.md"
output_dir = os.path.join(toolkit_root, "output_audio_paws")

def log_status(message):
    with open(status_file, "w") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
    print(message)

def run_background():
    log_status("Starting background synthesis process for Paws and Effect...")
    
    with open(log_file, "a") as log:
        process = subprocess.Popen(
            [venv_python, script_to_run, book_path, output_dir],
            cwd=toolkit_root,
            stdout=log,
            stderr=log,
            creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
        )
    
    log_status(f"Synthesis started with PID {process.pid}. Monitor '{log_file}' for details.")

if __name__ == "__main__":
    run_background()
