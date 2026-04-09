import os
import sys
import platform

def init_gpu():
    """
    Handles Windows-specific DLL injection for NVIDIA pip packages.
    This allows onnxruntime-gpu and ctranslate2 to find their dependencies
    without manual PATH modification or brute-force copying.
    """
    if sys.platform != "win32":
        return

    # print("Initializing GPU runtime environment...")
    
    # Common locations for nvidia packages in a venv
    venv_base = sys.prefix
    site_packages = os.path.join(venv_base, "Lib", "site-packages")
    nvidia_base = os.path.join(site_packages, "nvidia")
    
    if not os.path.exists(nvidia_base):
        # print("NVIDIA packages not found in current venv. GPU acceleration may fail.")
        return

    # Add all 'bin' directories found in nvidia packages to the DLL search path
    added_paths = []
    for root, dirs, files in os.walk(nvidia_base):
        if "bin" in dirs:
            bin_path = os.path.abspath(os.path.join(root, "bin"))
            try:
                os.add_dll_directory(bin_path)
                # Also add to PATH as a fallback for older libraries
                os.environ["PATH"] = bin_path + os.pathsep + os.environ["PATH"]
                added_paths.append(bin_path)
            except Exception as e:
                # print(f"Failed to add {bin_path} to DLL path: {e}")
                pass
    
    # if added_paths:
    #     print(f"Added {len(added_paths)} NVIDIA bin directories to DLL search path.")

if __name__ == "__main__":
    init_gpu()
    import onnxruntime as rt
    print(f"Available providers: {rt.get_available_providers()}")
