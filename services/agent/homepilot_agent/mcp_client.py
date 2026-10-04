"""Thin async client for the HomePilot MCP server (Streamable HTTP) that records a readable trace."""
from __future__ import annotations

import json
import os
import time
from contextlib import asynccontextmanager
from typing import Any

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

MCP_URL = os.environ.get("HOMEPILOT_MCP_URL", "http://127.0.0.1:8765/mcp")


class McpCallError(RuntimeError):
    pass


class HomePilotMcp:
    def __init__(self, session: ClientSession, trace: list[dict] | None = None):
        self.session = session
        self.trace = trace if trace is not None else []

    async def call(self, tool: str, **args: Any) -> Any:
        t0 = time.perf_counter()
        res = await self.session.call_tool(tool, args)
        ms = int((time.perf_counter() - t0) * 1000)
        if res.isError:
            text = "".join(getattr(c, "text", "") for c in res.content)
            self.trace.append({"tool": tool, "args": args, "ms": ms, "error": text})
            raise McpCallError(text)
        data = _unwrap(res)
        self.trace.append({"tool": tool, "args": args, "ms": ms, "summary": _summary(tool, data)})
        return data


def _unwrap(res) -> Any:
    sc = res.structuredContent
    if sc is not None:
        return sc["result"] if set(sc) == {"result"} else sc
    text = "".join(getattr(c, "text", "") for c in res.content)
    return json.loads(text) if text else None


def _summary(tool: str, data: Any) -> str:
    if isinstance(data, list):
        return f"{len(data)} item(s)"
    if isinstance(data, dict):
        if "actions" in data:
            return f"{len(data['actions'])} action(s), {len(data.get('conflicts', []))} conflict note(s)"
        if "household" in data:
            return f"{len(data['household']['people'])} people"
        if "status" in data:
            return str(data["status"])
    return "ok"


@asynccontextmanager
async def connect(url: str = MCP_URL, trace: list[dict] | None = None):
    async with streamable_http_client(url) as (read, write, _):
        async with ClientSession(read, write) as session:
            init = await session.initialize()
            client = HomePilotMcp(session, trace)
            client.protocol_version = init.protocolVersion  # type: ignore[attr-defined]
            yield client


async def selftest(url: str = MCP_URL) -> dict:
    """Startup self-test from the risk register: confirm protocol version and tool listing."""
    async with connect(url) as c:
        tools = [t.name for t in (await c.session.list_tools()).tools]
        required = {"get_household_context", "detect_conflicts", "propose_plan", "confirm_plan"}
        missing = sorted(required - set(tools))
        if missing:
            raise McpCallError(f"MCP server is missing tools: {missing}")
        return {"protocol": c.protocol_version, "tools": tools}


if __name__ == "__main__":
    import asyncio
    print(json.dumps(asyncio.run(selftest()), indent=2))
