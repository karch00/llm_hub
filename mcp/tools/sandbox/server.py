import subprocess
from mcp.server.fastmcp import FastMCP
import os

os.umask(0)
mcp = FastMCP("sandbox", host="0.0.0.0", port=8003)

@mcp.tool()
def run_shell(command: str, timeout: int = 60) -> str:
    """Run a bash command as root in a disposable Linux box (internet allowed).
    Nothing persists: the box resets when it restarts."""
    print(repr(command), flush=True)  # shows the exact command in `docker compose logs sandbox`
    try:
        r = subprocess.run(
            ["bash", "-lc", command],
            cwd="/work",
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=min(timeout, 300),
        )
        out = r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        out = "[timed out]"
    return out[-8000:] if out else "(no output)"

mcp.run(transport="streamable-http")
