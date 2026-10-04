FROM debian:bookworm
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1 PIP_BREAK_SYSTEM_PACKAGES=1
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-venv python3-pip python3-requests python3-httpx python3-bs4 python3-lxml \
    python3-numpy python3-pandas python3-openpyxl python3-pil python3-yaml \
    python3-dateutil python3-jinja2 python3-click python3-tqdm python3-psutil \
    python3-pytest python3-flask python3-aiohttp python3-websockets python3-paramiko \
    python3-paho-mqtt python3-scipy python3-sklearn python3-opencv\
    build-essential git curl ca-certificates nodejs procps net-tools \
    htop iotop vim tmux jq strace netcat-openbsd sqlite3 lsof strace \ 
    time nano less tree wget dnsutils iputils-ping zip unzip gzip bzip2
RUN python3 -m venv /opt/mcp && /opt/mcp/bin/pip install "mcp<2"

WORKDIR /work
COPY server.py /opt/server.py
CMD ["/opt/mcp/bin/python", "/opt/server.py"]
