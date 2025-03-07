import os
# from gpu_utils import get_available_gpu
# Environment variables haven't been fully tested yet, use with caution
# hardware decoding is currently not working.
CODEC = os.getenv('v2x_codec', 'libx265')

valid_codecs = ['libx265', 'libx264']
# NVIDIA, AMD, INTEL = get_available_gpu()
# print(f"NVIDIA: {NVIDIA}, AMD: {AMD}, INTEL: {INTEL}")
# if NVIDIA:
#     valid_codecs.append('hevc_nvenc')
# if AMD:
#     valid_codecs.append('hevc_amf')
# if INTEL:
#     valid_codecs.append('hevc_qsv')
# Validate codec
if CODEC not in valid_codecs:
    raise ValueError(f"Unsupported codec: {CODEC}")

# Scaling method - either a target resolution or a scale factor
# Valid values: target_resolution, fixed_resolution, flat
SCALE_METHOD = os.getenv('v2x_scale_method', 'target_resolution')
# Validate scale method
if SCALE_METHOD not in ['target_resolution', 'fixed_resolution', 'flat']:
    raise ValueError(f"Invalid scale method: {SCALE_METHOD}")

# Target resolution for scaling. Only used if v2x_scale_method is set to target_resolution
# Valid values: 480, 720, 1080, 1440, 2160
TARGET_RESOLUTION = os.getenv('v2x_target_res', '1080')
# Validate
if TARGET_RESOLUTION not in ['480', '720', '1080', '1440', '2160']:
    raise ValueError(f"Invalid target resolution: {TARGET_RESOLUTION}")

# Fixed resolution for scaling. Only used if v2x_scale_method is set to fixed_resolution
# Format: WIDTHxHEIGHT
FIXED_RESOLUTION = os.getenv('v2x_fixed_res', '1920x1080')


# Scale factor. Only used if v2x_scale_method is set to flat
# Valid values: 2, 3, 4
SCALE_FACTOR = os.getenv('v2x_scale_factor', '4')
# Validate
if SCALE_FACTOR not in ['2', '3', '4']:
    raise ValueError(f"Invalid scale factor: {SCALE_FACTOR}")

# Model to use for upscaling
# TODO add limitations for models in terms of x[n] scaling
MODEL=os.getenv('v2x_model', 'realesrgan-plus-anime')
"""
Valid Models:
--- libplacebo --- # must set fixed resolution to use libplacebo
anime4k-v4-a, anime4k-v4-a+a,
anime4k-v4-b, anime4k-v4-b+b,
anime4k-v4-c, anime4k-v4-c+a,
anime4k-v4.1-gan

--- RealESRGAN --- # must set scale factor to use RealESRGAN
realesr-animevideov3, # can have scale factor set to 2, 3, or 4
realesrgan-plus-anime, realesrgan-plus # must have scale factor set to 4

--- RealCUGAN --- # must set scale factor to use RealCUGAN
models-nose, # must have scale factor set to 2
models-pro, # must have scale factor set to 2 or 3
models-se, # scale factor can be set to 2, 3, or 4
"""

PROCESSOR = None
# Set PROCESSOR based on model
if MODEL in ['anime4k-v4-a', 'anime4k-v4-a+a', 'anime4k-v4-b', 'anime4k-v4-b+b', 'anime4k-v4-c', 'anime4k-v4-c+a', 'anime4k-v4.1-gan']:
    PROCESSOR = 'libplacebo'
elif MODEL in ['realesr-animevideov3', 'realesrgan-plus-anime', 'realesrgan-plus']:
    PROCESSOR = 'realesrgan'
elif MODEL in ['models-nose', 'models-pro', 'models-se']:
    PROCESSOR = 'realcugan'
else:
    raise ValueError(f"Unsupported model: {MODEL}")

# Validate model and scale method
if PROCESSOR == 'libplacebo' and SCALE_METHOD != 'fixed_resolution':
    raise ValueError(f"Model {MODEL} requires fixed resolution scaling")
if PROCESSOR in ['realcugan', 'realesrgan'] and (SCALE_METHOD == 'fixed_resolution'):
    raise ValueError(f"Model {MODEL} is incompatible with fixed resolution scaling")


SCALE_2_ONLY = ['models-nose']
SCALE_2_OR_3 = ['models-pro']
SCALE_2_3_4 = ['models-se', 'realesr-animevideov3']
SCALE_4_ONLY = ['realesrgan-plus-anime', 'realesrgan-plus']
SCALE_MAX = 4
SCALE_MIN = 2

if MODEL in SCALE_2_ONLY:
    if SCALE_METHOD == 'flat' and SCALE_FACTOR != '2':
        raise ValueError(f"Model {MODEL} only supports scale factor 2")
    elif SCALE_METHOD == 'target_resolution':
        SCALE_MAX = 2
elif MODEL in SCALE_2_OR_3:
    if SCALE_METHOD == 'flat' and SCALE_FACTOR not in ['2', '3']:
        raise ValueError(f"Model {MODEL} only supports scale factor 2 or 3")
    elif SCALE_METHOD == 'target_resolution':
        SCALE_MAX = 3
elif MODEL in SCALE_4_ONLY:
    if SCALE_METHOD == 'flat' and SCALE_FACTOR != '4':
        raise ValueError(f"Model {MODEL} only supports scale factor 4")
    elif SCALE_METHOD == 'target_resolution':
        SCALE_MIN = 4

REALCUGAN_THREADS = os.getenv('v2x_realcugan_threads', '1')
REALCUGAN_SYNCGAP = os.getenv('v2x_realcugan_syncgap', '3')

# TODO: enable NOISE_LEVEL
# TODO: enable ENCODING_THREADS


if REALCUGAN_SYNCGAP not in ['0', '1', '2', '3']:
    raise ValueError(f"Invalid RealCUGAN sync gap value: {REALCUGAN_SYNCGAP}")

print(f"Using processor: {PROCESSOR} with model: {MODEL}")