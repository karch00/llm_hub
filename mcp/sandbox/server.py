import subprocess
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("sandbox", host="0.0.0.0", port=8003)

@mcp.tool()
def run_shell(command: str, timeout: int = 60) -> str:
    """Run a bash command as root in a disposable Linux box (internet allowed).
    /data/memories persists; /data/temporary is this chat's scratch. Write there
    ONLY with the `save` command (save [-a] <temporary|memories> <path.md>, text via heredoc).
    
    Commands ending with & are backgrounded and return immediately."""
    print(repr(command), flush=True)
    
    # Detect if command is backgrounded
    is_backgrounded = command.rstrip().endswith("&")
    
    if is_backgrounded:
        log_file = f"/tmp/{command.split()[0]}.log"
        detached_cmd = f"nohup bash -lc '{command}' >> {log_file} 2>&1"
        try:
            subprocess.Popen(detached_cmd, shell=True, 
                           stdin=subprocess.DEVNULL,
                           start_new_session=True)
            return f"[backgrounded → {log_file}] {command}"
        except Exception as e:
            return f"[failed] {e}"
    
    # Normal foreground command
    try:
        r = subprocess.run(["bash", "-lc", command], 
                          stdin=subprocess.DEVNULL,
                          capture_output=True, text=True, 
                          timeout=min(timeout, 300))
        out = r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        out = "[timed out]"
    except Exception as e:
        out = f"[error] {e}"
    
    return out[-8000:] if out else "(no output)"

subprocess.run(["save", "--reindex"], capture_output=True)
mcp.run(transport="streamable-http")
