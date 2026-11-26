from mcp.server.fastmcp import FastMCP
import shutil
import time
from datetime import datetime
from pathlib import Path

mcp = FastMCP("journal", host="0.0.0.0", port=8005, stateless_http=True, json_response=True)
JOURNALS = "/data/journals"

@mcp.tool()
def create_journal(user_entry: str, model_reflexion: str, overwrite: bool = False) -> str:
    """
    Create a journal with the initial main user entry and your final reflexion at the end of the exchange.
    Reflexion must be as-thorough-as-possible and insightful and show where ideas changed by quoting the conversation.
    
    IMPORTANT:
    Entry and Reflexion must be entered respecting newlines with these rules:
        1. All-round Formatting: Max 140 characters per line.
        2. Inputted Formatting: Preserve the original formatting on top of the character limit per line.
    If journal already exists, prompt the user for overwrite confirmation.
    """
    # Handle AM hours, go back one day
    if datetime.today().hour < 4:
        stamp = int(time.time() - 3600 * 5)
    else:
        stamp = int(time.time())
    
    today = datetime.fromtimestamp(stamp).strftime("%Y-%m-%d")
    path = f"{JOURNALS}/{today}"

    if Path(path).exists():
        if overwrite:
            shutil.rmtree(path)
        else:
            return "Journal already exists for this day"

    Path(path).mkdir(parents=True)
    with open(file=f"{path}/Entry", mode="x+") as f:
        f.write(user_entry)
    with open(file=f"{path}/Reflexion", mode="x+") as f:
        f.write(model_reflexion)

    return "Journal created succesfully"

mcp.run(transport="streamable-http")
