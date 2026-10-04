"""End-to-end over real Streamable HTTP: spawns the MCP server process and drives the agent against it."""
import os
import socket
import subprocess
import sys
import time

import pytest

from homepilot_agent.agent import OfflineAgent
from homepilot_agent.mcp_client import connect, selftest

GOLDEN = ("Tomorrow our child has the doctor at 9. I start work at 8:30, Ali has class at 10, "
          "we are out of milk, and the science project is due Monday.")


@pytest.fixture(scope="module")
def mcp_url():
    s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
    env = {**os.environ, "HOMEPILOT_MCP_PORT": str(port),
           "PYTHONPATH": os.pathsep.join(["packages/domain", "services/mcp"])}
    proc = subprocess.Popen([sys.executable, "-m", "homepilot_mcp.server"], env=env,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    url = f"http://127.0.0.1:{port}/mcp"
    for _ in range(50):
        try:
            socket.create_connection(("127.0.0.1", port), timeout=0.2).close(); break
        except OSError:
            time.sleep(0.1)
    yield url
    proc.terminate()


async def test_selftest_lists_tools(mcp_url):
    info = await selftest(mcp_url)
    assert info["protocol"] >= "2025-03-26" and "propose_plan" in info["tools"]


async def test_golden_scenario_end_to_end(mcp_url):
    async with connect(mcp_url) as m:
        await m.call("demo_reset")
    res = await OfflineAgent(mcp_url).handle(GOLDEN, "sam")
    p = res.proposal
    assert [t["tool"] for t in res.trace][-1] == "propose_plan"
    kinds = sorted(a["type"] for a in p["actions"])
    assert kinds.count("create_event") == 3 and "add_shopping" in kinds and "create_task" in kinds
    async with connect(mcp_url) as m:
        assert await m.call("list_tasks", household_id="demo", owner="sam") == []  # drafted only
        await m.call("confirm_plan", household_id="demo", proposal_id=p["id"], actor_id="sam")
        ali = await m.call("next_actions", household_id="demo", person_id="ali")
        sam = await m.call("next_actions", household_id="demo", person_id="sam")
        assert any("doctor" in i["title"].lower() for i in ali["items"])
        titles = [i["title"] for i in sam["items"]]
        assert "Science Project" in titles and not any("octor" in t for t in titles)  # only their own items
        audit = await m.call("get_audit_log", household_id="demo")
        assert audit[0]["tool"] == "confirm_plan"


async def test_cross_household_denied(mcp_url):
    async with connect(mcp_url) as m:
        with pytest.raises(Exception, match="household_not_found"):
            await m.call("list_tasks", household_id="someone-else")
