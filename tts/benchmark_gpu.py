import os
import sys
import time
import numpy as np

# Centralized GPU/DLL initialization
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.gpu_init import init_gpu
init_gpu()

import onnxruntime as rt

def benchmark():
    # Use the model path relative to toolkit root
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    toolkit_root = os.path.dirname(current_script_dir)
    model_path = os.path.join(toolkit_root, "onnx", "model.onnx")

    if not os.path.exists(model_path):
        print(f"Error: Model not found at {model_path}")
        return

    providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
    print(f"Available Providers: {rt.get_available_providers()}")
    print(f"Targeting: {providers}")

    try:
        sess = rt.InferenceSession(model_path, providers=providers)
        print(f"Session Provider: {sess.get_providers()[0]}")
        
        # Mock inputs
        input_ids = np.zeros((1, 100), dtype=np.int64)
        style = np.zeros((1, 256), dtype=np.float32)
        speed = np.array([1.0], dtype=np.float32)
        inputs = {"input_ids": input_ids, "style": style, "speed": speed}

        print("Warming up...")
        for _ in range(5): sess.run(None, inputs)

        print("Benchmarking (10 iterations)...")
        start = time.time()
        for _ in range(10): sess.run(None, inputs)
        avg = (time.time() - start) / 10
        print(f"Average Inference Time: {avg:.4f}s")
        
        if "CUDA" in sess.get_providers()[0]:
            print("SUCCESS: GPU acceleration is active!")
        else:
            print("WARNING: Falling back to CPU.")

    except Exception as e:
        print(f"Error during benchmark: {e}")

if __name__ == "__main__":
    benchmark()
