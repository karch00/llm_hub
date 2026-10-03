FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-venv build-essential git curl ca-certificates nodejs \
 && python3 -m venv /opt/mcp && /opt/mcp/bin/pip install "mcp<2" 
COPY server.py /opt/server.py
COPY save /usr/local/bin/save
RUN chmod +x /usr/local/bin/save
CMD ["/opt/mcp/bin/python", "/opt/server.py"]
