import wave
import struct

def create_silent_wav(output_path, duration_sec=2, sample_rate=16000):
    print(f"Creating {duration_sec}s silent WAV file for testing...")
    
    # 16-bit PCM, mono
    num_samples = int(duration_sec * sample_rate)
    with wave.open(output_path, 'wb') as wav_file:
        wav_file.setparams((1, 2, sample_rate, num_samples, 'NONE', 'not compressed'))
        for _ in range(num_samples):
            wav_file.writeframes(struct.pack('<h', 0))
    
    print(f"Created: {output_path}")

if __name__ == "__main__":
    create_silent_wav("test_silent.wav")
