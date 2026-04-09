import os
import sys
import time
import re
import numpy as np
import soundfile as sf

# Windows DLL path fix for nvidia pip packages
if sys.platform == "win32":
    try:
        import site
        # Search for nvidia packages in site-packages
        # We'll use a more direct approach by checking common venv structure
        venv_base = os.path.dirname(sys.executable)
        site_packages = os.path.join(venv_base, "Lib", "site-packages")
        nvidia_base = os.path.join(site_packages, "nvidia")
        
        if os.path.exists(nvidia_base):
            for root, dirs, files in os.walk(nvidia_base):
                if "bin" in dirs:
                    bin_path = os.path.abspath(os.path.join(root, "bin"))
                    os.add_dll_directory(bin_path)
                    os.environ["PATH"] = bin_path + os.pathsep + os.environ["PATH"]
    except Exception:
        pass

from kokoro_onnx import Kokoro
from kokoro_onnx.config import KoKoroConfig, SAMPLE_RATE, MAX_PHONEME_LENGTH
from kokoro_onnx.log import log

# Patching Kokoro class for the onnx-community model
class KokoroCommunity(Kokoro):
    def _create_audio(self, phonemes, voice, speed):
        start_t = time.time()
        tokens = np.array(self.tokenizer.tokenize(phonemes), dtype=np.int64)
        
        idx = min(len(tokens), len(voice) - 1)
        v = voice[idx]
        
        inputs = {
            "input_ids": [[0, *tokens, 0]],
            "style": v.reshape(1, -1).astype(np.float32),
            "speed": np.array([speed], dtype=np.float32)
        }
        
        audio = self.sess.run(None, inputs)[0]
        if len(audio.shape) > 1:
            audio = audio.squeeze()
        
        return audio, SAMPLE_RATE

    def create(self, text, voice, speed=1.0, lang="en-us"):
        if isinstance(voice, str):
            voice = self.get_voice_style(voice)
            
        phonemes = self.tokenizer.phonemize(text, lang)
        batched_phonemes = self._split_phonemes(phonemes)
        audio = []
        for p in batched_phonemes:
            a, _ = self._create_audio(p, voice, speed)
            audio.append(a)
        return np.concatenate(audio), SAMPLE_RATE


def clean_text(text):
    # Remove Table of Contents
    text = re.sub(r'\[Chapter.*?\)\n', '', text)
    # Basic cleaning
    text = text.replace('---', '-')
    return text

def split_into_scenes(text):
    scenes = re.split(r'## Scene \d+', text)
    return [s.strip() for s in scenes if s.strip()]

def split_into_chunks(text, max_chars=500):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_chars:
            current_chunk += " " + sentence
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def run_tts():
    # Use command line argument if provided, otherwise default to book.md
    book_path = sys.argv[1] if len(sys.argv) > 1 else "book.md"
    
    # Ensure paths are relative to the toolkit root
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    toolkit_root = os.path.dirname(current_script_dir)
    
    model_path = os.path.join(toolkit_root, "onnx", "model.onnx")
    voices_path = os.path.join(toolkit_root, "voices.bin")
    
    # Optional output directory argument
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
        if not os.path.isabs(output_dir):
            output_dir = os.path.join(toolkit_root, output_dir)
    else:
        output_dir = os.path.join(toolkit_root, "output_audio")
    
    # If book_path is not absolute, make it relative to root
    if not os.path.isabs(book_path):
        book_path = os.path.join(toolkit_root, book_path)
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Initializing Kokoro TTS (Community Model) on GPU...")
    kokoro = KokoroCommunity(model_path, voices_path)

    print(f"Reading {book_path}...")
    with open(book_path, "r", encoding="utf-8") as f:
        full_text = f.read()

    # Skip front matter: Skip everything until Scene 1
    if "## Scene 1" in full_text:
        full_text = "## Scene 1" + full_text.split("## Scene 1", 1)[1]

    cleaned_text = clean_text(full_text)
    scenes = split_into_scenes(cleaned_text)
    
    print(f"Detected {len(scenes)} scenes.")
    
    list_file = os.path.join(output_dir, "list.txt")
    
    for i, scene in enumerate(scenes):
        scene_num = i + 1
        scene_filename = f"scene_{scene_num:03d}.wav"
        scene_output = os.path.join(output_dir, scene_filename)
        
        # Add to list file immediately if it exists or when created
        def update_list():
            existing_lines = []
            if os.path.exists(list_file):
                with open(list_file, "r") as f:
                    existing_lines = f.readlines()
            
            line = f"file '{scene_filename}'\n"
            if line not in existing_lines:
                with open(list_file, "a") as f:
                    f.write(line)

        # Skip if already exists
        if os.path.exists(scene_output):
            print(f"Skipping Scene {scene_num} (already exists).")
            update_list()
            continue
            
        print(f"Processing Scene {scene_num}/{len(scenes)}...")
        
        chunks = split_into_chunks(scene)
        scene_audio = []
        
        start_scene = time.time()
        for j, chunk in enumerate(chunks):
            if not chunk.strip():
                continue
            try:
                # Log chunk start for debugging hangs
                print(f"    - Chunk {j+1}/{len(chunks)} ({len(chunk)} chars)...", flush=True)
                samples, sample_rate = kokoro.create(chunk, voice="af_heart", speed=1.0)
                scene_audio.append(samples)
            except Exception as e:
                print(f"\n  Error in Scene {scene_num}, Chunk {j+1}: {e}")

        if scene_audio:
            final_audio = np.concatenate(scene_audio)
            sf.write(scene_output, final_audio, sample_rate)
            update_list()
            print(f"  Scene {scene_num} completed in {time.time() - start_scene:.2f}s")

    print("\nFull book synthesis completed.")

    print("\nDone. Concatenate with: ffmpeg -f concat -safe 0 -i output_audio/list.txt -c copy audiobook.wav")

if __name__ == "__main__":
    run_tts()
