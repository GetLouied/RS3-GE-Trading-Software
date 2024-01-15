# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.224.3/containers/python-3/.devcontainer/base.Dockerfile

# [Choice] Python version (use -bullseye variants on local arm64/Apple Silicon): 3, 3.10, 3.9, 3.8, 3.7, 3.6, 3-bullseye, 3.10-bullseye, 3.9-bullseye, 3.8-bullseye, 3.7-bullseye, 3.6-bullseye, 3-buster, 3.10-buster, 3.9-buster, 3.8-buster, 3.7-buster, 3.6-buster
ARG VARIANT="3.11"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

ARG DEBIAN_FRONTEND=noninteractive
COPY . .
RUN pip3 install -r requirements.txt

RUN git config --global user.name "Louis DeRienzo"
RUN git config --global user.email "DeRienzo_louis@yahoo.com"

ARG USERNAME=vscode

ENV HOME /home/vscode
ENV SHELL /bin/bash

CMD [ "python3", "main.py"]