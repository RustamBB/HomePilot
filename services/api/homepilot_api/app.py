"""FastAPI gateway: web UI -> agent -> MCP. The API holds no household state; the MCP server owns it."""
from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from homepilot_agent.agent import get_agent
from homepilot_agent.mcp_client import McpCallError, connect, selftest

WEB_DIR = Path(os.environ.get("HOMEPILOT_WEB_DIR", Path(__file__).resolve().parents[3] / "apps" / "web"))
HID = "demo"  # the public demo only has the synthetic household

app = FastAPI(title="HomePilot API")


class ChatIn(BaseModel):
    message: str
    actor_id: str = "sam"


class ActorIn(BaseModel):
    actor_id: str = "sam"
    overrides: dict[str, str] | None = None


def _err(e: McpCallError) -> HTTPException:
    msg = str(e)
    code = 404 if "not_found" in msg else 403 if "not_in_household" in msg else 409 if "not_pending" in msg or "override_conflict" in msg or "hard_conflict" in msg else 400
    return HTTPException(code, msg)


@app.get("/api/health")
async def health():
    try:
        info = await selftest()
        return {"ok": True, "mcp_protocol": info["protocol"], "tools": len(info["tools"]), "agent": get_agent().mode}
    except Exception as e:  # graceful degradation: report, don't crash
        return {"ok": False, "error": f"MCP server unreachable: {e}"}


@app.get("/api/state")
async def state():
    async with connect() as m:
        return {
            "context": await m.call("get_household_context", household_id=HID),
            "events": await m.call("list_events", household_id=HID),
            "tasks": await m.call("list_tasks", household_id=HID),
            "shopping": (await m.call("shopping_list", household_id=HID))["items"],
            "conflicts": await m.call("detect_conflicts", household_id=HID),
            "brief": await m.call("daily_brief", household_id=HID),
            "proposals": await m.call("list_proposals", household_id=HID, status="pending"),
            "audit": await m.call("get_audit_log", household_id=HID, limit=30),
        }


@app.get("/api/people/{person_id}/next")
async def next_actions(person_id: str):
    try:
        async with connect() as m:
            return {"next": await m.call("next_actions", household_id=HID, person_id=person_id),
                    "brief": await m.call("daily_brief", household_id=HID, person_id=person_id)}
    except McpCallError as e:
        raise _err(e)


@app.post("/api/chat")
async def chat(body: ChatIn):
    try:
        res = await get_agent().handle(body.message, body.actor_id, HID)
    except McpCallError as e:
        raise _err(e)
    except Exception as e:
        raise HTTPException(502, f"The agent could not complete this request ({type(e).__name__}). "
                                 "Household data was not changed.")
    return {"reply": res.reply, "proposal": res.proposal, "trace": res.trace, "mode": res.mode}


async def _human(tool: str, proposal_id: str, body: ActorIn):
    args = {"household_id": HID, "proposal_id": proposal_id, "actor_id": body.actor_id}
    if tool == "confirm_plan":
        args["overrides"] = body.overrides
    try:
        async with connect() as m:
            return await m.call(tool, **args)
    except McpCallError as e:
        raise _err(e)


@app.post("/api/proposals/{proposal_id}/confirm")
async def confirm(proposal_id: str, body: ActorIn):
    return await _human("confirm_plan", proposal_id, body)


@app.post("/api/proposals/{proposal_id}/reject")
async def reject(proposal_id: str, body: ActorIn):
    return await _human("reject_plan", proposal_id, body)


@app.post("/api/proposals/{proposal_id}/undo")
async def undo(proposal_id: str, body: ActorIn):
    return await _human("undo_plan", proposal_id, body)


@app.post("/api/demo/reset")
async def reset():
    async with connect() as m:
        return await m.call("demo_reset")


if WEB_DIR.exists():
    app.mount("/assets", StaticFiles(directory=WEB_DIR), name="assets")

    @app.get("/")
    async def index():
        return FileResponse(WEB_DIR / "index.html")
