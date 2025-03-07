#!/usr/bin/python3
import os
import time
import subprocess
from pathlib import Path
import ffmpeg

# TODO resolve naming conflicts (error handling)
# TODO add verbose logging
# TODO add progress logging
# TODO add support for multiple input formats (in progress)
# TODO add support for multiple output formats (in progress)
# TODO add support for hvec_nvenc, hvec_amf, and hvec_qsv
# TODO add support for multiple upscale models
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
            print(file)
            filename = file.name
            output_filename = f"{filename.rsplit('.', 1)[0]}_upscaled" + ext
            
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
                print(f"Video resolution: {width}x{height} for {filename}")
                target_height = 1080
                scale = target_height / height
                scale_int = round(scale)

                scale_int = max(1, min(scale_int, 4))

                print(f"Scale factor set to {scale_int} for {filename}")

                if not file.exists():
                    print(f"File {file} no longer exists. Restarting loop...")
                    continue
                try:
                    subprocess.run(
                        ['video2x', '-i', str(file), '-o', f"/output/{output_filename}", '-p', 'realesrgan', '-s', str(scale_int), '--realesrgan-model', 'realesr-animevideov3', '-c', "libx265"],
                        check=True
                    )
                    print(f"video2x processing successful for {filename} (scale: {scale_int})")
                    Path('/input/processed').mkdir(parents=True, exist_ok=True)
                    os.rename(file, Path('/input/processed') / file.name)
                except subprocess.CalledProcessError:
                    print(f"video2x processing failed for {filename}")
                    exit(1)
            else:
                print(f"Failed to get video resolution for {filename}")
                exit(1)
        else:
            print("No files found. Sleeping for 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    main()