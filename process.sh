#!/bin/bash

echo "Running as user $(whoami)"
# Add /video2x to PATH
export PATH=$PATH:/video2x
video2x -l

while true; do
  file=$(find /input -maxdepth 1 -type f -name "*.mp4" -print -quit)
  
  if [ -n "$file" ]; then
    # Check if the file is still being copied
    stable=0
    prev_size=0
    prev_mtime=0

    while [ $stable -lt 3 ]; do # Require 3 stable checks
      curr_size=$(stat -c %s "$file")
      curr_mtime=$(stat -c %Y "$file")

      if [ "$curr_size" -eq "$prev_size" ] && [ "$curr_mtime" -eq "$prev_mtime" ]; then
        stable=$((stable + 1))
      else
        stable=0
      fi

      prev_size="$curr_size"
      prev_mtime="$curr_mtime"
      sleep 1 # Check every second
    done

    filename=$(basename "$file")
    output_filename="${filename%.*}_upscaled.mp4"

    # Get video resolution using ffprobe
    width=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of default=noprint_wrappers=1:nokey=1 "$file")
    height=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of default=noprint_wrappers=1:nokey=1 "$file")

    if [[ -n "$width" && -n "$height" ]]; then
        echo "Video resolution: ${width}x${height} for $filename"
        # Calculate the upscale factor to approximate 1080p (1920x1080)
        target_height=1080
        scale=$(echo "scale=2; $target_height / $height" | bc)

        # Round the scale to the nearest integer
        scale_int=$(printf "%.0f" "$scale")

        # Ensure scale is at least 1 and at most 4
        if [ "$scale_int" -lt 1 ]; then
            scale_int=4
        fi
        if [ "$scale_int" -gt 4 ]; then
            scale_int=4
        fi

        echo "Scale factor set to $scale_int for $filename"

        # Try-Catch for video2x
        if video2x -i "$file" -o "/output/$output_filename" -p realesrgan -s "$scale_int" --realesrgan-model realesr-animevideov3; then
            echo "video2x processing successful for $filename (scale: $scale_int)"
            mkdir -p /input/processed
            mv "$file" /input/processed/
        else
            echo "video2x processing failed for $filename"
            exit 1
            # Optionally, you might want to move the file to an error folder
            # mkdir -p /input/error
            # mv "$file" /input/error/
        fi
    else
        echo "Failed to get video resolution for $filename"
        exit 1
    fi

  else
    echo "No files found. Sleeping for 5 seconds..."
    sleep 5
  fi
done