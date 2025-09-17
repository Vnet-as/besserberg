# vim: set syntax=dockerfile:
FROM python:3.13-slim-bookworm as builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /opt/besserberg

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --no-install-project --no-editable --no-managed-python

ADD . /opt/besserberg

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-editable --no-managed-python

FROM python:3.13-slim-bookworm

LABEL maintainer="VNET a.s. <db@vnet.eu>"

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
 && apt-get install -y \
    xvfb \
    wkhtmltopdf \
    ghostscript \
    fonts-dejavu \
    libssl-dev \
 && rm -rf /var/lib/apt/lists/* \
 && apt-get clean

RUN useradd -ms /bin/bash besserberg
USER besserberg
WORKDIR /opt/besserberg
ENV PATH=$PATH:/opt/besserberg/.venv/bin

COPY --from=builder --chown=besserberg:besserberg /opt/besserberg/.venv /opt/besserberg/.venv

EXPOSE 8000

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "besserberg.app:app"]
