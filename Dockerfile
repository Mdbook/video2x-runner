FROM nvidia/cuda:12.8.0-devel-ubuntu24.04 AS builder

ARG VIDEO2X_VERSION=6.4.0

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install wget ffmpeg -y

# Download and extract Video2X
RUN wget https://github.com/k4yt3x/video2x/releases/download/${VIDEO2X_VERSION}/Video2X-x86_64.AppImage && \
    chmod +x Video2X-x86_64.AppImage && \
    ./Video2X-x86_64.AppImage --appimage-extract && \
    mv squashfs-root /video2x_appimage

# Stage 2: Runtime
FROM nvidia/cuda:12.8.0-runtime-ubuntu24.04

ARG VIDEO2X_VERSION=6.4.0

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install ffmpeg wget bc -y

# Vulkan setup
RUN wget -qO- https://packages.lunarg.com/lunarg-signing-key-pub.asc | tee /etc/apt/trusted.gpg.d/lunarg.asc
RUN wget -qO /etc/apt/sources.list.d/lunarg-vulkan-noble.list http://packages.lunarg.com/vulkan/lunarg-vulkan-noble.list
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install vulkan-sdk nvidia-driver-570 -y
RUN apt-get clean && rm -rf /var/lib/apt/lists/*
# Copy Video2X from builder stage
COPY --from=builder /video2x_appimage /video2x

WORKDIR /video2x
RUN ln -s /video2x/usr/share/video2x/models /video2x/models
RUN ln -s AppRun video2x

COPY process.sh /process.sh
RUN chmod +x /process.sh

# Create a non-root user
RUN useradd -ms /bin/bash video2x
USER video2x

ENTRYPOINT ["/process.sh"]