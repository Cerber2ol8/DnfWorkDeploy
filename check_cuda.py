import os
import sys
current_path = os.environ.get('PATH', '')
new_path = os.path.abspath("./lib")
os.environ['PATH'] = current_path + os.pathsep + new_path

import onnxruntime as ort
def add_library_path():
    if sys.platform.startswith('linux'):
        lib_path = os.path.abspath('lib_linux')
        current_path = os.environ.get('LD_LIBRARY_PATH', '')
        if lib_path not in current_path:
            os.environ['LD_LIBRARY_PATH'] = f"{lib_path}:{current_path}"
            os.system(f'export LD_LIBRARY_PATH={os.environ["LD_LIBRARY_PATH"]}')
        print(f"Linux: Added {lib_path} to LD_LIBRARY_PATH")

    elif sys.platform.startswith('win'):
        lib_path = os.path.abspath('lib_win')
        current_path = os.environ.get('PATH', '')
        if lib_path not in current_path:
            os.environ['PATH'] = f"{lib_path};{current_path}"
        print(f"Windows: Added {lib_path} to PATH")

    else:
        print(f"Unsupported OS: {sys.platform}")


def check_cuda_available():
    providers = ort.get_available_providers()
    cuda_available = 'CUDAExecutionProvider' in providers
    if cuda_available:
        print("CUDA is available.")
    else:
        print("CUDA is not available.")
    return cuda_available

if __name__ == "__main__":
    cuda_available = check_cuda_available()
