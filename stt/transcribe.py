r"""
Usage: .\venv\Scripts\python.exe stt/transcribe.py <path_to_audio_file>
Example: .\venv\Scripts\python.exe stt/transcribe.py sample.mp3
"""
import time
import os
import sys

# Centralized GPU/DLL initialization
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.gpu_init import init_gpu
init_gpu()

from faster_whisper import WhisperModel

def test_transcribe(audio_file):
    # Check if file exists
    if not os.path.exists(audio_file):
        print(f"Error: File {audio_file} not found.")
        return

    # Use distil-large-v3 for best speed/accuracy balance on your 4060
    model_size = "distil-large-v3"
    
    print(f"--- Local STT PoC ---")
    print(f"Model: {model_size}")
    print(f"Device: CUDA (NVIDIA RTX 4060)")
    
    try:
        # Load model
        # compute_type="float16" is recommended for RTX 40-series
        start_load = time.time()
        model = WhisperModel(model_size, device="cuda", compute_type="float16")
        print(f"Model loaded in {time.time() - start_load:.2f}s")

        # Transcribe
        print(f"Transcribing: {os.path.basename(audio_file)}...")
        start_transcribe = time.time()
        
        # beam_size=5 is standard, lower is faster
        segments, info = model.transcribe(audio_file, beam_size=5)
        
        print(f"Detected language: '{info.language}' (p={info.language_probability:.2f})")
        print("-" * 30)

        for segment in segments:
            print(f"[{segment.start:5.2f}s -> {segment.end:5.2f}s] {segment.text}")

        print("-" * 30)
        print(f"Transcription finished in {time.time() - start_transcribe:.2f}s")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        print("\nNote: If you see CUDA errors, ensure NVIDIA drivers and cuDNN are correctly installed.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_transcribe(sys.argv[1])
    else:
        print("Usage: .\\venv\\Scripts\\python.exe stt/transcribe.py <path_to_audio_file>")
        print("Example: .\\venv\\Scripts\\python.exe stt/transcribe.py sample.mp3")
