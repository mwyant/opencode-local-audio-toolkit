import numpy as np
import os

def create_mock_voices_bin():
    # The onnx-community model expects style vectors of length 256
    # af_heart.bin has 130560 elements. 130560 / 256 = 510.
    raw_data = np.fromfile('voices/af_heart.bin', dtype=np.float32)
    voice_data = raw_data.reshape(-1, 256)
    
    # Save as .npz
    np.savez('voices.bin', af_heart=voice_data)
    print(f"Created voices.bin with {voice_data.shape[0]} style vectors of size {voice_data.shape[1]} for 'af_heart'.")

if __name__ == "__main__":
    create_mock_voices_bin()

if __name__ == "__main__":
    create_mock_voices_bin()

if __name__ == "__main__":
    create_mock_voices_bin()
