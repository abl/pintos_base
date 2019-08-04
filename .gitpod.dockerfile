FROM gitpod/workspace-full:latest

USER root
RUN apt-get update && apt-get install -y qemu \
    && apt-get clean && rm -rf /var/cache/apt/* && rm -rf /var/lib/apt/lists/* && rm -rf /tmp/*

USER gitpod
ENV PINTOS_HOME /workspace/pintos_base

USER root
