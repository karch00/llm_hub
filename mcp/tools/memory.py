import os, pathlib
from datetime import datetime
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("memory", host="0.0.0.0", port=8004)
###ROOT = "/data/memories"
ROOT = ".tests"
INDEX = f"{ROOT}/index.md"

# General tools
def reindex():
    if not pathlib.Path(INDEX).exists():
        dirpath = "/".join(INDEX.split("/")[:-1])

        if not os.path.isdir(dirpath):
            os.makedirs(dirpath)

        with open(INDEX, mode="x+", encoding="utf-8") as f:
            f.write("# Category/Topic | Summary | Created | Updated")

# MCP tools
@mcp.tool()
def memory_read(path: str = "index") -> str:
    """Reads the contents of a memory.
    By default reads index. Always call first to have necessary information about indexed memories.
    `path`: the Category/Topic column of a memory that has been read in the index beforehand.
    """
    if path == "index":
        mempath = INDEX
    else:
        mempath = f"{ROOT}/{path}.md"

    if not pathlib.Path(mempath).exists():
        return f"{path} does not exist"

    with open(mempath, mode="r", encoding="utf-8") as f:
        return f.read()

@mcp.tool()
def memory_create(path: str, summary: str, content: str) -> str:
    """Creates a memory.
    `path`: the Category/Topic. Example: path="setup/computer"
    `summary`: the summary of the contents inside. Keep it short, under 100-120 characters, one line.
    `content`: the content to write separated by \n. Example: "Intel CPU\nNvidia GPU\nDual monitor"
    """
    mempath = f"{ROOT}/{path}.md"
    dirpath = "/".join(mempath.split("/")[:-1])

    if not os.path.isdir(dirpath):
        os.makedirs(dirpath)
    if pathlib.Path(mempath).exists():
        return f"{path} already exists. Check existing contents and either:\n1.reconsider new category if changes are substantial\nor\n2.ask user for memory replace/update with changes"

    # Create content list to write lines
    content_list = ["# Summary", summary, "# Contents"]
    for n, line in enumerate(content.split("\n"), start=1):
        content_list.append(f"{n}. {line}")
        n += 1

    # Write File
    with open(mempath, mode="x+", encoding="utf-8") as f:
        f.write("\n".join(content_list))

    # Update index
    with open(INDEX, mode="a", encoding="utf-8") as f:
        f.write(f"\n{path} | {summary} | {datetime.now().strftime("%Y-%m-%d")} | {datetime.now().strftime("%Y-%m-%d")}")
    return "Succesfully created memory"

@mcp.tool()
def memory_replace(path: str, line_number: int, new_content: str = "") -> str:
    """Replaces a memory line.
    Replaces should be few and used only when strictly necessary. Example: Specific Information changed due to recent events.
    `path`: the Category/Topic. Example: path="people/John"
    `line_number`: line number to replace from the content. Example: 3
    `new_content`: The content that will replace the content of the current line. Do not include the line number here. If ommited, line number will be erased
    """
    mempath = f"{ROOT}/{path}.md"

    if not pathlib.Path(mempath).exists():
       return f"{path} does not exist"
    if line_number < 1:
        return "Line must be >=1"

    # Line bias at 2 since line indexes 0, 1 and 2 are # Summary, (summary) and # Contents
    real_line_n = line_number + 2
    with open(mempath, "r+", encoding="utf-8") as f:
       lines = f.readlines()
       if real_line_n > len(lines)-1:
           return "Line number over the number of existing lines"

       if not new_content: # Erase line
           lines.pop(line_number+2) # Pop targetted line
           for n, line in enumerate(lines[3:], start=1): # Re-index content lines
               lines[n+2] = f"{n}. {line[3:]}"
       else:
           lines[real_line_n] = f"{line_number}. {new_content}\n"

       # Overwrite and truncate possible leftovers
       f.seek(0)
       f.writelines(lines)
       f.truncate()

    return "Line updated succesfully"

@mcp.tool()
def memory_append(path: str, new_line: str) -> str:
    """Appends a line to the memory.
    Appends should be few and used only when strictly necessary. Example: New unkown information that is not infered from other present facts.
    `path`: the Category/Topic. Example: path="hobbies/videogames"
    `new_line`: the line to append. Example: new_line="Really likes Dwarf Fortress"
    """
    mempath = f"{ROOT}/{path}.md"
    if not pathlib.Path(mempath).exists():
       return f"{path} does not exist"

    with open(mempath, mode="a+", encoding="utf-8") as f:
        f.seek(0)
        next_line_n = len(f.readlines()) - 2 # Line bias
        f.write(f"\n{next_line_n}. {new_line}")

    return "Line appended succesfully"

@mcp.tool()
def memory_delete(path: str) -> str:
    """Delete a memory, only when the user asks to forget it. Ask for confirmation before deleting.
    `path`: the Category/Topic. Example: path="projects/mcp_hub"
    """
    mempath = f"{ROOT}/{path}.md"
    if not pathlib.Path(mempath).exists():
       return f"{path} does not exist"

    # Remove file and from index
    os.remove(mempath)
    with open(INDEX, mode="r+", encoding="utf-8") as f:
        lines = [l for l in f.readlines() if path not in l]
        f.seek(0)
        f.write("\n".join(lines))
        f.truncate()

    return "Memory deleted succesfully"

reindex()
###mcp.run(transport="streamable-http")
