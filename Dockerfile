FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

# System packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    git \
    python3 \
    python3-pip \
    python3-venv \
    unzip \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Node.js 20 LTS
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

# Hugo extended (latest stable ≥ 0.147.0)
ARG HUGO_VERSION=0.147.0
RUN curl -fsSL "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.deb" \
        -o /tmp/hugo.deb \
    && dpkg -i /tmp/hugo.deb \
    && rm /tmp/hugo.deb

# Python tools (djlint, yamllint) — install into a venv to avoid PEP 668 issues
RUN python3 -m venv /opt/pyenv \
    && /opt/pyenv/bin/pip install --no-cache-dir djlint yamllint
ENV PATH="/opt/pyenv/bin:${PATH}"

# lychee link checker
ARG LYCHEE_VERSION=0.15.1
RUN curl -fsSL "https://github.com/lycheeverse/lychee/releases/download/v${LYCHEE_VERSION}/lychee-v${LYCHEE_VERSION}-x86_64-unknown-linux-gnu.tar.gz" \
        -o /tmp/lychee.tar.gz \
    && tar -xzf /tmp/lychee.tar.gz -C /usr/local/bin lychee \
    && rm /tmp/lychee.tar.gz

# npm dependencies (including Playwright)
WORKDIR /workspace
COPY package.json package-lock.json ./
RUN npm ci

# Playwright system dependencies and browsers
RUN npx playwright install --with-deps chromium

WORKDIR /workspace
CMD ["/bin/bash"]
