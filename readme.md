# Video2X Runner

*This project is in ALPHA! It is under active development and is not yet ready for production use.*

This project provides a Dockerized setup for running Video2X, a tool for upscaling videos using machine learning models. The setup includes a Dockerfile for building the image and a `process.sh` script for processing videos in a specified input directory.

## Project Structure

```
video2x-runner/
├── Dockerfile
├── process.sh
└── docker-compose.yaml
```

- `Dockerfile`: Defines the Docker image for running Video2X.
- `process.sh`: Script for processing videos in the input directory.
- `docker-compose.yaml`: Docker Compose configuration for running the Video2X container.

## Prerequisites

- Docker
- NVIDIA GPU with drivers and nvidia-container-toolkit installed

### process.sh

The process.sh script continuously monitors the `/input` directory for new `.mp4` files. When a new file is detected, it waits until the file is stable (not being copied), then processes it using Video2X. The upscaled video is saved to the `/output` directory.

### docker-compose.yaml

The Docker Compose configuration defines the video2x-runner service, which mounts the input and output directories and sets up the necessary GPU resources.

## Usage

1. Place your `.mp4` files in the input directory.
2. The process.sh script will automatically detect and process the files.
3. Upscaled videos will be saved to the output directory.

## Features
- Automatically detects and processes new `.mp4` files in the input directory.
- Supports GPU acceleration for faster processing.
- Dynamically chooses the appropriate scale factor to target 1080p.
- More features coming soon

## Environment Variables

- `VIDEO2X_VERSION`: The version of Video2X to use (default: `6.4.0`).

## License

This project is licensed under the MIT License.
