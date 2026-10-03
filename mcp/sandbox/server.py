import subprocess
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("sandbox", host="0.0.0.0", port=8003)

@mcp.tool()
def run_shell(command: str, timeout: int = 60) -> str:
    """Run a bash command as root in a disposable Linux box (internet allowed).
    /data/memories persists; /data/temporary is this chat's scratch. Write there
    ONLY with the `save` command (save [-a] <temporary|memories> <path.md>, text via heredoc)."""
    print(repr(command), flush=True)
    try:
        r = subprocess.run(["bash", "-lc", command], stdin=subprocess.DEVNULL,
                           capture_output=True, text=True, timeout=min(timeout, 300))
        out = r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        out = "[timed out]"
    return out[-8000:] if out else "(no output)"

mcp.run(transport="streamable-http")
