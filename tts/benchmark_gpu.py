import onnxruntime as rt
import numpy as np
import time
import os
import sys

# Windows DLL path fix
venv_base = os.path.dirname(sys.executable)
site_packages = os.path.join(venv_base, "Lib", "site-packages")
nvidia_base = os.path.join(site_packages, "nvidia")
if os.path.exists(nvidia_base):
    for root, dirs, files in os.walk(nvidia_base):
        if "bin" in dirs:
            bin_path = os.path.abspath(os.path.join(root, "bin"))
            print(f"Adding to DLL path: {bin_path}")
            os.add_dll_directory(bin_path)
            os.environ["PATH"] = bin_path + os.pathsep + os.environ["PATH"]
import onnxruntime as rt
providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
print(f"Available: {rt.get_available_providers()}")
print(f"Using: {providers}")

sess = rt.InferenceSession("onnx/model.onnx", providers=providers)
print(f"Session providers: {sess.get_providers()}")

print(f"Session providers: {sess.get_providers()}")

# Mock inputs
# [('input_ids', [1, 'sequence_length']), ('style', [1, 256]), ('speed', [1])]
input_ids = np.zeros((1, 100), dtype=np.int64)
style = np.zeros((1, 256), dtype=np.float32)
speed = np.array([1.0], dtype=np.float32)

inputs = {
    "input_ids": input_ids,
    "style": style,
    "speed": speed
}

print("Running warmup...")
for _ in range(5):
    sess.run(None, inputs)

print("Running benchmark (10 iterations)...")
start = time.time()
for _ in range(10):
    sess.run(None, inputs)
end = time.time()

print(f"Average inference time: {(end - start) / 10:.4f}s")
