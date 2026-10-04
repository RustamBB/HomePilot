#!/bin/sh
# One container, two processes: MCP server (loopback only) + FastAPI gateway on $PORT.
set -e
python -m homepilot_mcp.server &
for i in $(seq 1 30); do python -c "import socket;socket.create_connection(('127.0.0.1',8765),1)" 2>/dev/null && break; sleep 1; done
exec python -m uvicorn homepilot_api.app:app --host 0.0.0.0 --port "${PORT:-8000}"
