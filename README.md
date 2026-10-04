# LLM_Hub

This repo is dedicated to store the configs and implementations of my personal LLM hub.

Uses llama.cpp as server alongside some docker services + python scripts for MCP, notably:
1. Searxng + python script for custom MCP tool
2. Playwright for website fetch
3. Isolated sandbox environment for draft generation, code execution, etc.
4. Memory-managing MCP server for user information saved in categories

Alongside some neat features, for now:
1. Memories: persistent saving of memories on the sandbox for future uses on other sessions / across models

Hardware tested (assuming base OS is Linux debian-based):
- i7 10700KF
- 32GB DDR4 3200MT/s
- RTX 3080 10GB


