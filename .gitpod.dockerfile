FROM gitpod/workspace-full:latest

USER root
RUN apt-get update && apt-get install -y qemu qemu-system-x86

USER gitpod
ENV PINTOS_HOME /workspace/pintos_base
ENV PATH ${PATH}:${PINTOS_HOME}/pintos/src/utils

USER root
