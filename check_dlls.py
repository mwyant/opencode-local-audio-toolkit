import os
import sys
import ctypes

def check_dlls():
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from utils.gpu_init import init_gpu
    init_gpu()
    
    dlls = ["cublas64_12.dll", "cublasLt64_12.dll", "cudnn64_9.dll", "nvJitLink_120_0.dll"]
    for dll in dlls:
        try:
            ctypes.CDLL(dll)
            print(f"LOADED: {dll}")
        except Exception as e:
            print(f"FAILED: {dll} - {e}")

if __name__ == "__main__":
    check_dlls()
