import subprocess

# TODO: is there a better way to check if user is using a GPU?
def check_nvidia_gpu():
    try:
        result = subprocess.run(['nvidia-smi'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            return True
    except FileNotFoundError:
        pass
    return False

def check_amd_gpu():
    try:
        result = subprocess.run(['lspci'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if 'VGA compatible controller: Advanced Micro Devices' in result.stdout.decode():
            return True
    except FileNotFoundError:
        pass
    return False

def check_intel_gpu():
    try:
        result = subprocess.run(['lspci'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if 'VGA compatible controller: Intel Corporation' in result.stdout.decode():
            return True
    except FileNotFoundError:
        pass
    return False

def get_available_gpu():
    return check_nvidia_gpu(),check_amd_gpu(),check_intel_gpu()
