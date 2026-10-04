"""Demo reliability protocol (docs/05): reset -> golden scenario -> verify -> confirm -> verify, five times."""
import asyncio
import sys
from pathlib import Path

from homepilot_agent.agent import get_agent
from homepilot_agent.mcp_client import connect

GOLDEN = Path(__file__).resolve().parents[1].joinpath("demo", "golden_scenario.txt").read_text().strip()


async def once() -> None:
    async with connect() as m:
        await m.call("demo_reset")
    res = await get_agent().handle(GOLDEN, "sam")
    p = res.proposal
    assert p and not [c for c in p["conflicts"] if c["severity"] == "high"], "unexpected hard conflict"
    owners = {a["args"].get("title") or a["args"].get("name"): a["args"].get("owner") or a["args"].get("assigned_to")
              for a in p["actions"] if a["type"] in ("create_event", "create_task", "add_shopping")}
    assert owners["Maya: doctor appointment"] == "ali" and owners["Science Project"] == "sam", owners
    async with connect() as m:
        await m.call("confirm_plan", household_id="demo", proposal_id=p["id"], actor_id="sam")
        assert (await m.call("detect_conflicts", household_id="demo")) == [], "conflicts remain after confirm"
        assert (await m.call("get_audit_log", household_id="demo"))[0]["tool"] == "confirm_plan"


async def main(n: int = 5) -> int:
    for i in range(1, n + 1):
        await once()
        print(f"run {i}/{n}: OK")
    return 0


sys.exit(asyncio.run(main()))
