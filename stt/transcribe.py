import time
import os
import sys

# Windows DLL path fix for nvidia pip packages
if sys.platform == "win32":
    print("Detected Windows, checking for local NVIDIA DLLs...")
    try:
        import faster_whisper
        # Find where faster_whisper is installed (likely venv site-packages)
        site_packages = os.path.dirname(os.path.dirname(faster_whisper.__file__))
        nvidia_base = os.path.join(site_packages, "nvidia")
        
        if os.path.exists(nvidia_base):
            print(f"Searching for DLLs in: {nvidia_base}")
            for root, dirs, files in os.walk(nvidia_base):
                if "bin" in dirs:
                    bin_path = os.path.abspath(os.path.join(root, "bin"))
                    print(f"Adding to DLL search path: {bin_path}")
                    os.add_dll_directory(bin_path)
                    # Also add to PATH as a fallback for some libraries
                    os.environ["PATH"] = bin_path + os.pathsep + os.environ["PATH"]
        else:
            print(f"Warning: nvidia base directory not found at {nvidia_base}")
    except ImportError:
        print("faster_whisper not imported yet, skipping DLL path fix")

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
        print("Usage: .\\venv\\Scripts\\python.exe transcribe.py <path_to_audio_file>")
        print("Example: .\\venv\\Scripts\\python.exe transcribe.py sample.mp3")
