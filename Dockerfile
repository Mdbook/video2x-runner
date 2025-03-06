FROM nvidia/cuda:12.8.0-runtime-ubuntu24.04 AS base
RUN apt-get update && apt-get install wget fuse ffmpeg -y
RUN wget -qO- https://packages.lunarg.com/lunarg-signing-key-pub.asc | tee /etc/apt/trusted.gpg.d/lunarg.asc
RUN wget -qO /etc/apt/sources.list.d/lunarg-vulkan-noble.list http://packages.lunarg.com/vulkan/lunarg-vulkan-noble.list
RUN apt update
RUN apt install vulkan-sdk nvidia-driver-570 -y
# nvidia-vulkan-icd -y


RUN wget https://github.com/k4yt3x/video2x/releases/download/6.4.0/Video2X-x86_64.AppImage
RUN chmod +x Video2X-x86_64.AppImage
RUN ./Video2X-x86_64.AppImage --appimage-extract
RUN mv squashfs-root /appimage

WORKDIR /appimage
RUN ln -s usr/share/video2x/models models

COPY process.sh /process.sh
RUN chmod +x /process.sh
ENTRYPOINT ["/process.sh"]