#!/usr/bin/python3
import os
import time
import subprocess
from pathlib import Path
import ffmpeg
import v2xvars

# TODO add config (in progress)
# TODO resolve naming conflicts (error handling)
# TODO add verbose logging
# TODO add progress logging
# TODO add support for multiple output formats (in progress)
# TODO add support for multiple upscale resolutions
# TODO add database to keep track of broken files
print("Starting up...")

def get_video_resolution(file_path):
    try:
        probe = ffmpeg.probe(file_path, select_streams = "v")
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        if video_stream:
            width = int(video_stream['width'])
            height = int(video_stream['height'])
            return width, height
        else:
            return None, None
    except ffmpeg.Error:
        return None, None

def main():
    while True:
        Path('/input/processed').mkdir(parents=True, exist_ok=True)
        ext = ".mp4"
        file = None
        for ext in ['.mp4', '.mkv', '.avi']:
            file = next(Path('/input').glob("*" + ext), None)
            if file:
                break
        if file:
            output_filename = f"{file.name.rsplit('.', 1)[0]}_upscaled" + ext
            
            # Test if output filename already exists
            if (Path('/output') / output_filename).exists():
                print(f"Output file {output_filename} already exists! Skipping...")
                try:
                    os.rename(file, Path('/input/processed') / file.name)
                except PermissionError:
                    print(f"Permission denied: unable to move {file} to /input/processed")
                    exit(1)
                except Exception as e:
                    print(f"Error moving file {file} to /input/processed: {e}")
                    exit(1)
                time.sleep(5)
                continue

            stable = 0
            prev_size = 0
            prev_mtime = 0

            while stable < 3:
                if not file.exists():
                    print(f"File {file} no longer exists. Restarting loop...")
                    continue

                curr_size = file.stat().st_size
                curr_mtime = file.stat().st_mtime

                if curr_size == prev_size and curr_mtime == prev_mtime:
                    stable += 1
                else:
                    stable = 0

                prev_size = curr_size
                prev_mtime = curr_mtime
                time.sleep(1)

            width, height = get_video_resolution(str(file))

            if width and height:
                print(f"Video resolution: {width}x{height} for {file.name}")
                scale_int = None
                fixed_resolution = False
                resolution_x = None
                resolution_y = None
                if v2xvars.SCALE_METHOD == 'flat':
                    scale_int = int(v2xvars.SCALE_FACTOR)
                    print(f"Running flat scaling for {file.name} using scale factor {scale_int}")
                elif v2xvars.SCALE_METHOD == 'target_resolution':
                    target_height = v2xvars.TARGET_RESOLUTION
                    scale = target_height / height
                    scale_int = round(scale)
                    scale_int = max(1, min(scale_int, 4))
                    print(f"Scale factor set to {scale_int} for {file.name}")
                elif v2xvars.SCALE_METHOD == 'fixed_resolution':
                    fixed_resolution = True
                    resolution_str = v2xvars.FIXED_RESOLUTION.split('x')
                    resolution_x = int(resolution_str[0])
                    resolution_y = int(resolution_str[1])
                    print(f"Running fixed resolution scaling for {file.name} using resolution {resolution_x}x{resolution_y}")

                if not file.exists():
                    print(f"File {file} no longer exists. Restarting loop...")
                    continue
                try:
                    # ['video2x', '-i', str(file), '-o', f"/output/{output_filename}", '-p', 'realesrgan', '-s', str(scale_int), '--realesrgan-model', 'realesr-animevideov3', '-c', v2xvars.CODEC],
                    # NEED: -s (scale_int), --realesrgan-model (v2xvars.MODEL), 
                    base_process = ['video2x', '-i', str(file), '-o', f"/output/{output_filename}", '-p', v2xvars.PROCESSOR, '-c', v2xvars.CODEC]
                    if not fixed_resolution:
                        base_process.extend(['-s', str(scale_int)])
                    else:
                        base_process.extend(['-w', str(resolution_x), '-h', str(resolution_y)])
                    match v2xvars.PROCESSOR:
                        case 'realesrgan':
                            base_process.extend(['--realesrgan-model', v2xvars.MODEL])
                        case 'libplacebo':
                            base_process.extend(['--libplacebo-shader', v2xvars.MODEL])
                        case 'realcugan':
                            base_process.extend(['--realcugan-model', v2xvars.MODEL])
                    subprocess.run(
                        base_process,
                        check=True
                    )
                    print(f"video2x processing successful for {file.name} (scale: {scale_int})")
                    Path('/input/processed').mkdir(parents=True, exist_ok=True)
                    os.rename(file, Path('/input/processed') / file.name)
                except subprocess.CalledProcessError:
                    print(f"video2x processing failed for {file.name}")
                    exit(1)
            else:
                print(f"Failed to get video resolution for {file.name}")
                exit(1)
        else:
            print("No files found. Sleeping for 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    main()