from mcp.server.fastmcp import FastMCP
import shutil
from datetime import datetime
from pathlib import Path

mcp = FastMCP("journal", host="0.0.0.0", port=8005)
JOURNALS = "/data/journals"

@mcp.tool()
def create_journal(user_entry: str, model_reflexion: str, overwrite: bool = False) -> str:
    """
    Create a journal with the initial main user entry and your final reflexion at the end of the exchange.
    Entry and Reflexion must be entered respecting: 1. Formatting: Max 80 characters per line; 2. Input form: User or Model inputted newlines.
    If journal already exists, prompt the user for overwrite confirmation.
    """
    today = datetime.today().strftime("%Y-%m-%d")
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
