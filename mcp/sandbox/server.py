import subprocess
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("sandbox", host="0.0.0.0", port=8003)

@mcp.tool()
def run_shell(command: str, timeout: int = 60) -> str:
    """Run a bash command as root in a disposable Linux box (internet allowed)."""
    try:
        r = subprocess.run(["bash", "-lc", command], capture_output=True,
                           text=True, timeout=min(timeout, 300))
        out = r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        out = "[timed out]"
    return out[-8000:]  # keep the tail so context doesn't flood
mcp.run(transport="streamable-http")
