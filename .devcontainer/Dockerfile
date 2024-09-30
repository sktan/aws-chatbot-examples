FROM mcr.microsoft.com/vscode/devcontainers/python:3.12
ENV EDITOR=vim

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive && \
    apt-get install -y vim gnupg2 ripgrep && \
    pip install pipenv
