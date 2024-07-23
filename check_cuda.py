import onnxruntime as ort
import torch

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
