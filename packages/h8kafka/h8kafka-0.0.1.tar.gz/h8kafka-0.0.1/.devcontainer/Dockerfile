FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye
SHELL ["/bin/bash", "-c"]

# Upgrade PIP
RUN pip install --upgrade pip

# Install Python depencencies
RUN pip install pylint isort pyright pre-commit autoflake

USER vscode
ENV PATH="$PATH:/home/vscode/.local/bin"
