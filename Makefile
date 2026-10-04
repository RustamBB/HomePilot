PY ?= python3
export PYTHONPATH := packages/domain:services/mcp:services/agent:services/api

.PHONY: install mcp api web run test selftest demo-seed rehearse
install:
	$(PY) -m pip install -e ".[dev]"

mcp:            ## MCP server (Streamable HTTP) on :8765
	$(PY) -m homepilot_mcp.server

api:            ## FastAPI gateway + web UI on :8000
	$(PY) -m uvicorn homepilot_api.app:app --port 8000

run:            ## everything: MCP in background, API in foreground
	$(PY) -m homepilot_mcp.server & sleep 2 && $(PY) -m uvicorn homepilot_api.app:app --port 8000

selftest:       ## confirm MCP protocol version + tool listing
	$(PY) -m homepilot_agent.mcp_client

demo-seed:      ## reset the synthetic household to its seed state
	$(PY) scripts/demo_seed.py

test:
	$(PY) -m pytest -q

rehearse:       ## 5 consecutive clean golden-scenario runs against a running MCP server
	$(PY) scripts/rehearse.py
