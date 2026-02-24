FROM ghcr.io/astral-sh/uv:debian-slim

# Create a non-root user for development
RUN useradd -m coder \
    && mkdir -p /home/coder/.cache \
    && chown -R coder:coder /home/coder

USER coder
WORKDIR /home/coder/codecrafters-claude-code-python

USER root
RUN apt-get update \
    && apt-get install -y curl bsdmainutils git \
    && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL https://codecrafters.io/install.sh | bash

# Safer user than using root directly
USER coder

COPY --chown=coder:coder pyproject.toml uv.lock .python-version ./

RUN uv sync

CMD ["bash"]