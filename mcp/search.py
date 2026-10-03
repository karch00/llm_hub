import httpx, trafilatura
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("web", host="0.0.0.0", port=8001)
HDRS = {"X-Forwarded-For": "127.0.0.1", "X-Real-IP": "127.0.0.1"}

@mcp.tool()
def web_search(query: str, max_results: int = 6) -> str:
    """Search the web. Returns title, URL and a short snippet per result."""
    r = httpx.get("http://searxng:8080/search",
                  params={"q": query, "format": "json"}, headers=HDRS, timeout=20)
    if r.status_code != 200:
        return f"Search failed: HTTP {r.status_code} {r.text[:200]}"
    return "\n\n".join(f"{x['title']}\n{x['url']}\n{x.get('content','')[:300]}"
                       for x in r.json()["results"][:max_results])

@mcp.tool()
def fetch_url(url: str, start: int = 0, max_chars: int = 12000) -> str:
    """Fetch a page and return its main text (not HTML). Long pages are paged:
    pass start=<next start> to continue. Use browser_* only if this returns nothing."""
    r = httpx.get(url, follow_redirects=True, timeout=30,
                  headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    text = trafilatura.extract(r.text, include_links=True, include_tables=True) or r.text
    chunk = text[start:start + max_chars]
    end = start + len(chunk)
    more = f"\n\n[{start}-{end} of {len(text)} chars; next start={end}]" if end < len(text) else ""
    return chunk + more

mcp.run(transport="streamable-http")
