import os
from gpu_utils import get_available_gpu
# Environment variables haven't been fully tested yet, use with caution

CODEC = os.getenv('v2x_codec', 'libx265')

valid_codecs = ['libx265', 'libx264']
NVIDIA, AMD, INTEL = get_available_gpu()
if NVIDIA:
    valid_codecs.append('hvec_nvenc')
if AMD:
    valid_codecs.append('hvec_amf')
if INTEL:
    valid_codecs.append('hvec_qsv')

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
--- libplacebo ---
anime4k-v4-a, anime4k-v4-a+a,
anime4k-v4-b, anime4k-v4-b+b,
anime4k-v4-c, anime4k-v4-c+a,
anime4k-v4.1-gan

--- RealESRGAN ---
realesr-animevideov3, realesrgan-plus-anime, realesrgan-plus

--- RealCUGAN ---
models-nose, models-pro, models-se
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

print(f"Using processor: {PROCESSOR} with model: {MODEL}")