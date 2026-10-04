FROM debian:bookworm
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-venv build-essential git curl ca-certificates nodejs \
    procps net-tools htop iotop vim tmux jq strace netcat-openbsd sqlite3 \
    lsof strace time nano less tree wget dnsutils iputils-ping zip unzip gzip bzip2 \
 && python3 -m venv /opt/mcp && /opt/mcp/bin/pip install "mcp<2" 
COPY server.py /opt/server.py
COPY save /usr/local/bin/save
RUN chmod +x /usr/local/bin/save
CMD ["/opt/mcp/bin/python", "/opt/server.py"]
