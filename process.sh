#!/bin/bash
./AppRun -l
./AppRun -i /input/standard-test.mp4 -o /output/standard-test.mp4 -s 2 -p realesrgan --realesrgan-model realesr-animevideov3
exit 1
while true; do
  file=$(find /input -type f -name "*.mp4" -print -quit)
  
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

    # Try-Catch for video2x
    if video2x -i "$file" -o "/output/$output_filename" -p realesrgan -s 4 --realesrgan-model realesr-animevideov3; then
      echo "video2x processing successful for $filename"
      mkdir -p /input/processed
      mv "$file" /input/processed/
    else
      echo "video2x processing failed for $filename"
      exit 0
      # Optionally, you might want to move the file to an error folder
      # mkdir -p /input/error
      # mv "$file" /input/error/
    fi

  else
    echo "No files found. Sleeping for 5 seconds..."
    sleep 5
  fi
done