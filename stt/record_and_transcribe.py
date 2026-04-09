import time
import os
import sys
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

# Windows DLL path fix for nvidia pip packages
if sys.platform == "win32":
    try:
        import faster_whisper
        site_packages = os.path.dirname(os.path.dirname(faster_whisper.__file__))
        nvidia_base = os.path.join(site_packages, "nvidia")
        if os.path.exists(nvidia_base):
            for root, dirs, files in os.walk(nvidia_base):
                if "bin" in dirs:
                    bin_path = os.path.abspath(os.path.join(root, "bin"))
                    os.add_dll_directory(bin_path)
                    os.environ["PATH"] = bin_path + os.pathsep + os.environ["PATH"]
    except ImportError:
        pass

from faster_whisper import WhisperModel

def record_audio(filename, duration=5, fs=16000):
    print(f"Recording for {duration} seconds...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    print("Recording finished.")
    write(filename, fs, recording)  # Save as WAV file

def transcribe(audio_file):
    model_size = "distil-large-v3"
    print(f"Loading model {model_size} on CUDA...")
    model = WhisperModel(model_size, device="cuda", compute_type="float16")
    
    print(f"Transcribing {audio_file}...")
    start_time = time.time()
    segments, info = model.transcribe(audio_file, beam_size=5)
    
    print("-" * 30)
    for segment in segments:
        print(f"[{segment.start:5.2f}s -> {segment.end:5.2f}s] {segment.text}")
    print("-" * 30)
    print(f"Finished in {time.time() - start_time:.2f}s")

if __name__ == "__main__":
    temp_file = "voice_input.wav"
    duration = 5
    if len(sys.argv) > 1:
        duration = int(sys.argv[1])
    
    try:
        record_audio(temp_file, duration=duration)
        transcribe(temp_file)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if os.path.exists(temp_file):
            # os.remove(temp_file)
            pass
