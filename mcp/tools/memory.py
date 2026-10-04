import re, datetime, pathlib
from mcp.server.fastmcp import FastMCP

ROOT = pathlib.Path("/data/memories")
mcp = FastMCP("memory", host="0.0.0.0", port=8004)

SECRET = re.compile(
    r"password|passwd|passphrase|secret|api[ _-]?key|private key|access token|auth token"
    r"|bearer |-----BEGIN|\b\d{1,3}(\.\d{1,3}){3}\b|[A-Za-z0-9+=_]{32,}", re.I)
REFUSED = ("REFUSED: looks like a secret, password, key or IP address. Never store those. "
           "Do not retry; tell the user it was not stored.")

def clean(s): return re.sub(r"password managers?", "", s, flags=re.I)
def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
def squash(s): return s.replace("-", "").rstrip("s")
def bullet(l): l = l.strip().lstrip("-").strip(); return f"- {l}"

def match(existing, name):
    """Reuse an existing name that differs only by hyphens or a plural s."""
    for e in existing:
        if e != name and squash(e) == squash(name):
            return e
    return name

def locate(category, topic):
    c, t = slug(category), slug(topic)
    if not c or not t:
        return c, t, None
    cats = [d.name for d in ROOT.iterdir() if d.is_dir()] if ROOT.exists() else []
    c = match(cats, c)
    topics = [f.stem for f in (ROOT / c).glob("*.md")] if (ROOT / c).is_dir() else []
    t = match(topics, t)
    return c, t, ROOT / c / f"{t}.md"

def reindex():
    ROOT.mkdir(parents=True, exist_ok=True)
    rows = []
    for f in sorted(ROOT.glob("*/*.md")):
        first = (f.read_text().splitlines() or [""])[0]
        day = datetime.date.fromtimestamp(f.stat().st_mtime)
        rows.append(f"{f.parent.name}/{f.stem} | {first} | {day}")
    (ROOT / "index.md").write_text(
        "# memory index: category/topic | summary | updated\n" + "\n".join(rows) + "\n")

@mcp.tool()
def memory_read(path: str = "index") -> str:
    """Read the memory index (default) or one note, e.g. "homelab/network"."""
    if path in ("", "index"):
        f = ROOT / "index.md"
        return f.read_text() if f.exists() else "(memory is empty)"
    cat, _, topic = path.strip("/").removesuffix(".md").partition("/")
    _, _, f = locate(cat, topic)
    return f.read_text() if f and f.exists() else "(no such note: check the index)"

@mcp.tool()
def memory_save(category: str, topic: str, summary: str, details: str) -> str:
    """Create a NEW note about the user (use memory_update for an existing note).
    category: broad area (environment, homelab, preferences). topic: the note's single subject (os, answer-style).
    summary: one-line label of what the note covers, not the facts. details: the facts, one per line."""
    if SECRET.search(clean(f"{summary}\n{details}")):
        return REFUSED
    c, t, f = locate(category, topic)
    if f is None:
        return "ERROR: category and topic need letters or digits."
    if "\n" in summary.strip() or len(summary) > 150 or not summary.strip():
        return "ERROR: summary must be one line, max 150 characters."
    body = "\n".join(bullet(l) for l in details.splitlines() if l.strip())
    if not body or len(body) > 3000:
        return "ERROR: details must be 1-3000 characters."
    if f.exists():
        return f"EXISTS: {c}/{t} already exists. Change it with memory_update."
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(f"{summary.strip()}\n{body}\n")
    reindex()
    moved = f" (mapped from {slug(category)}/{slug(topic)})" if (c, t) != (slug(category), slug(topic)) else ""
    return f"saved {c}/{t}{moved}"

@mcp.tool()
def memory_update(category: str, topic: str, find: str = "", replace: str = "", summary: str = "") -> str:
    """Change ONE line of an existing note. find: distinctive words of the line to change ("" to add a line).
    replace: the new line ("" to remove the matched line). summary: new one-line label (optional)."""
    if SECRET.search(clean(f"{replace}\n{summary}")):
        return REFUSED
    c, t, f = locate(category, topic)
    if f is None or not f.exists():
        return "no such note: check the index, or create it with memory_save."
    if "\n" in replace.strip() or "\n" in summary.strip() or len(summary) > 150:
        return "ERROR: replace and summary must be a single line (summary max 150 characters)."
    if not (find.strip() or replace.strip() or summary.strip()):
        return "ERROR: nothing to change."
    lines = f.read_text().splitlines()
    head, body = lines[0], lines[1:]
    if summary.strip():
        head = summary.strip()
    if find.strip():
        hits = [i for i, l in enumerate(body) if find.strip().lower() in l.lower()]
        if not hits:
            return "ERROR: no line contains that text. Current note:\n" + "\n".join(lines)
        if len(hits) > 1:
            return "ERROR: several lines match; use more specific text:\n" + "\n".join(body[i] for i in hits)
        if replace.strip():
            body[hits[0]] = bullet(replace)
        else:
            del body[hits[0]]
    elif replace.strip():
        if bullet(replace) in body:
            return "already present"
        body.append(bullet(replace))
    out = "\n".join([head] + body) + "\n"
    if len(out) > 3000:
        return "ERROR: note would exceed 3000 characters; remove or shorten a line first."
    f.write_text(out)
    reindex()
    return f"updated {c}/{t}"

@mcp.tool()
def memory_delete(category: str, topic: str) -> str:
    """Delete a note, only when the user asks to forget it."""
    _, _, f = locate(category, topic)
    if not f or not f.exists():
        return "no such note"
    f.unlink()
    reindex()
    return "deleted"

reindex()
mcp.run(transport="streamable-http")
