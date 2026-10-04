"""Strands agent over the real MCP server, with a scripted model standing in for Bedrock.

Verifies everything except the Bedrock call itself: MCP tool discovery through Strands, the allow-list
(human-only tools hidden from the model), tool-call execution and draft retrieval."""
import json

import pytest

pytest.importorskip("strands")
from strands.models import Model  # noqa: E402

from homepilot_agent.agent import StrandsAgent  # noqa: E402
from homepilot_agent.mcp_client import connect  # noqa: E402
from tests.test_e2e_mcp import mcp_url  # noqa: E402,F401


class ScriptedModel(Model):
    def __init__(self):
        self.seen_tools: list[str] = []

    def update_config(self, **kw): ...
    def get_config(self): return {}
    async def structured_output(self, output_model, prompt, system_prompt=None, **kw):
        raise NotImplementedError
        yield

    async def stream(self, messages, tool_specs=None, system_prompt=None, **kw):
        self.seen_tools = [t["name"] for t in tool_specs or []]
        last = messages[-1]["content"][0]
        yield {"messageStart": {"role": "assistant"}}
        if "toolResult" in last:
            yield {"contentBlockDelta": {"delta": {"text": "Plan drafted; please confirm."}, "contentBlockIndex": 0}}
            yield {"contentBlockStop": {"contentBlockIndex": 0}}
            yield {"messageStop": {"stopReason": "end_turn"}}
            return
        args = {"household_id": "demo", "actor_id": "sam", "message": "m", "commitments": [
            {"kind": "task", "title": "Permission slip", "person": "ali", "due_at": "2026-10-19T08:00:00"}]}
        yield {"contentBlockStart": {"start": {"toolUse": {"toolUseId": "t1", "name": "propose_plan"}}, "contentBlockIndex": 0}}
        yield {"contentBlockDelta": {"delta": {"toolUse": {"input": json.dumps(args)}}, "contentBlockIndex": 0}}
        yield {"contentBlockStop": {"contentBlockIndex": 0}}
        yield {"messageStop": {"stopReason": "tool_use"}}
        yield {"metadata": {"usage": {"inputTokens": 1, "outputTokens": 1, "totalTokens": 2}, "metrics": {"latencyMs": 1}}}


async def test_strands_agent_drafts_via_mcp_and_cannot_see_human_tools(mcp_url):
    async with connect(mcp_url) as m:
        await m.call("demo_reset")
    model = ScriptedModel()
    res = await StrandsAgent(mcp_url, model=model).handle("ali handles the permission slip", "sam")
    assert "confirm_plan" not in model.seen_tools and "propose_plan" in model.seen_tools
    assert res.proposal and res.proposal["actions"][0]["args"]["title"] == "Permission slip"
    assert [t["tool"] for t in res.trace] == ["propose_plan"]
    async with connect(mcp_url) as m:
        assert await m.call("list_tasks", household_id="demo", owner="ali") == []  # nothing saved
