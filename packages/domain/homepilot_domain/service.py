"""Use-case layer shared by the MCP tools. All state changes funnel through confirm()."""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from . import conflicts as cf
from .errors import HomePilotError
from .models import (Action, Commitment, Event, Notification, Proposal, ShoppingItem, Task)
from .planner import build_plan
from .sanitize import clean_text
from .store import HouseholdState, Store, new_id


def _dump(x: Any) -> Any:
    if isinstance(x, list):
        return [_dump(i) for i in x]
    return x.model_dump(mode="json") if hasattr(x, "model_dump") else x


class Service:
    def __init__(self, store: Store):
        self.store = store

    # ---- reads -------------------------------------------------------------------------
    def state(self, hid: str) -> HouseholdState:
        return self.store.get(hid)

    def context(self, hid: str) -> dict:
        st = self.state(hid)
        return {"household": st.household.model_dump(mode="json"), "now": self.store.now(st).isoformat(),
                "open_tasks": sum(t.status == "open" for t in st.tasks.values()),
                "pending_proposals": sum(p.status == "pending" for p in st.proposals.values())}

    def events(self, hid: str, person_id: str | None = None, on: str | None = None) -> list[dict]:
        st = self.state(hid)
        evs = sorted(st.events.values(), key=lambda e: e.start)
        if person_id:
            pid = self.store.require_member(st, person_id)
            evs = [e for e in evs if pid in e.attendees or e.owner == pid]
        if on:
            day = datetime.fromisoformat(on).date()
            evs = [e for e in evs if e.start.date() == day]
        return _dump(evs)

    def tasks(self, hid: str, owner: str | None = None, status: str | None = "open") -> list[dict]:
        st = self.state(hid)
        ts = [t for t in st.tasks.values() if (not status or t.status == status)
              and (not owner or t.owner == self.store.require_member(st, owner))]
        return _dump(sorted(ts, key=lambda t: (t.due_at is None, t.due_at)))

    def shopping(self, hid: str) -> list[dict]:
        return _dump(list(self.state(hid).shopping.values()))

    def conflicts(self, hid: str) -> list[dict]:
        st = self.state(hid)
        return _dump(cf.detect(st.household, list(st.events.values()), list(st.tasks.values()), self.store.now(st)))

    def audit(self, hid: str, limit: int = 50) -> list[dict]:
        return _dump(self.state(hid).audit[-limit:][::-1])

    def proposal(self, hid: str, proposal_id: str) -> dict:
        return self._prop(self.state(hid), proposal_id).model_dump(mode="json")

    def proposals(self, hid: str, status: str | None = "pending") -> list[dict]:
        return _dump([p for p in self.state(hid).proposals.values() if not status or p.status == status])

    def next_actions(self, hid: str, person_id: str) -> dict:
        st = self.state(hid)
        pid = self.store.require_member(st, person_id)
        now = self.store.now(st)
        items: list[dict] = []
        for e in sorted(st.events.values(), key=lambda e: e.start):
            if e.end >= now and (pid in e.attendees or e.owner == pid) and e.kind != "busy":
                items.append({"kind": "event", "title": e.title, "when": e.start.isoformat(),
                              "why": "You're the responsible adult." if e.owner == pid else "You're attending."})
        for t in st.tasks.values():
            if t.status == "open" and t.owner == pid:
                items.append({"kind": "task", "title": t.title, "when": t.due_at.isoformat() if t.due_at else None,
                              "why": t.reasoning or "Assigned to you."})
        for s in st.shopping.values():
            if s.status == "needed" and s.assigned_to == pid:
                items.append({"kind": "shopping", "title": f"Buy {s.name}", "when": None,
                              "why": s.note or "Assigned to you."})
        items.sort(key=lambda i: (i["when"] is None, i["when"] or ""))
        msgs = [n.text for n in st.notifications if n.to == pid]
        return {"person": pid, "items": items, "notifications": msgs}

    def daily_brief(self, hid: str, person_id: str | None = None) -> dict:
        st = self.state(hid)
        now = self.store.now(st)
        risks = [c for c in self.conflicts(hid) if c["severity"] in ("high", "medium")]
        horizon = now + timedelta(hours=36)
        today = [e for e in st.events.values() if now.date() <= e.start.date() <= horizon.date() and e.end >= now
                 and e.kind != "busy" and (not person_id or person_id in e.attendees or e.owner == person_id)]
        due = [t for t in st.tasks.values() if t.status == "open" and t.due_at and t.due_at <= now + timedelta(hours=72)
               and (not person_id or t.owner == person_id)]
        pending = [p for p in st.proposals.values() if p.status == "pending"]
        parts = []
        if risks:
            parts.append(f"{len(risks)} thing(s) at risk")
        if pending:
            parts.append(f"{len(pending)} plan(s) waiting for approval")
        parts.append(f"{len(today)} event(s) soon, {len(due)} task(s) due within 3 days")
        return {"summary": "; ".join(parts) + ".", "at_risk": risks,
                "events": _dump(sorted(today, key=lambda e: e.start)),
                "tasks_due": _dump(sorted(due, key=lambda t: t.due_at)), "pending_proposals": len(pending)}

    # ---- drafting (never mutates household entities) -------------------------------------
    def propose(self, hid: str, commitments: list[Commitment], actor_id: str, message: str = "") -> dict:
        st = self.state(hid)
        actor = self.store.require_member(st, actor_id)
        with self.store.lock:
            prop = build_plan(st, commitments, actor, self.store.now(st), message)
            st.proposals[prop.id] = prop
            self.store.log(st, "agent", "propose_plan", f"Proposed {len(prop.actions)} action(s)", "proposed",
                           after={"proposal_id": prop.id})
            self.store.flush()
        return prop.model_dump(mode="json")

    def stage(self, hid: str, actor_id: str, action: Action, message: str) -> dict:
        """Single-action draft used by create_event/create_task/assign_task/shopping/send_notification."""
        st = self.state(hid)
        actor = self.store.require_member(st, actor_id)
        with self.store.lock:
            prop = Proposal(id=new_id("prop"), message=message, actions=[action], rationale=[action.rationale],
                            created_at=self.store.now(st))
            st.proposals[prop.id] = prop
            self.store.log(st, actor, action.type, f"Drafted: {message}", "proposed", after={"proposal_id": prop.id})
            self.store.flush()
        return {"status": "pending_confirmation", "proposal_id": prop.id,
                "note": "Nothing was saved. A household member must confirm this proposal."}

    # ---- committing (human-approved only) -------------------------------------------------
    def _prop(self, st: HouseholdState, pid: str) -> Proposal:
        p = st.proposals.get(pid)
        if not p:
            raise HomePilotError("proposal_not_found", f"No proposal '{pid}' in this household.")
        return p

    def confirm(self, hid: str, proposal_id: str, actor_id: str, overrides: dict[str, str] | None = None) -> dict:
        st = self.state(hid)
        actor = self.store.require_member(st, actor_id)
        with self.store.lock:
            prop = self._prop(st, proposal_id)
            if prop.status != "pending":
                raise HomePilotError("not_pending", f"Proposal is already {prop.status}.")
            actions = [a.model_copy(deep=True) for a in prop.actions]
            for idx, who in (overrides or {}).items():
                self._override(st, actions, int(idx), self.store.require_member(st, who))
            created: list[dict[str, str]] = []
            for a in actions:
                created.extend(self._apply(st, a, actor))
            prop.actions, prop.status, prop.created_entities = actions, "confirmed", created
            self.store.log(st, actor, "confirm_plan", f"Confirmed proposal with {len(actions)} action(s)", "confirmed",
                           after={"proposal_id": prop.id, "created": created})
            self.store.flush()
        return {"status": "confirmed", "created": created}

    def _override(self, st: HouseholdState, actions: list[Action], idx: int, who: str) -> None:
        if not 0 <= idx < len(actions):
            raise HomePilotError("invalid_override", f"No action at index {idx}.")
        a = actions[idx]
        if a.type == "create_event":
            ev = Event.model_validate(a.args)
            f = cf.fit(who, ev, list(st.events.values()))
            if not f.ok:
                raise HomePilotError("override_conflict",
                                     f"{st.household.person(who).display_name} is busy: '{f.blocking.title}'.")
            ev.owner = who
            ev.attendees = list(dict.fromkeys([*ev.attendees, who]))
            a.args = ev.model_dump(mode="json")
        elif a.type == "create_task":
            a.args["owner"] = who
        elif a.type == "add_shopping":
            a.args["assigned_to"] = who
        else:
            raise HomePilotError("invalid_override", f"Action type '{a.type}' has no owner to override.")

    def _apply(self, st: HouseholdState, a: Action, actor: str) -> list[dict[str, str]]:
        if a.type == "create_event":
            e = Event.model_validate(a.args)
            st.events[e.id] = e
            self.store.log(st, actor, "create_event", e.title, "confirmed", after=e.model_dump(mode="json"))
            return [{"type": "event", "id": e.id}]
        if a.type == "create_task":
            t = Task.model_validate({**a.args, "title": clean_text(a.args["title"])})
            st.tasks[t.id] = t
            self.store.log(st, actor, "create_task", t.title, "confirmed", after=t.model_dump(mode="json"))
            return [{"type": "task", "id": t.id}]
        if a.type == "add_shopping":
            s = ShoppingItem.model_validate(a.args)
            st.shopping[s.id] = s
            self.store.log(st, actor, "shopping_list", f"Add {s.name}", "confirmed", after=s.model_dump(mode="json"))
            return [{"type": "shopping", "id": s.id}]
        if a.type == "assign_task":
            t = st.tasks.get(a.args["task_id"])
            if not t:
                raise HomePilotError("task_not_found", f"No task '{a.args['task_id']}'.")
            before = t.model_dump(mode="json")
            t.owner = a.args["owner"]
            t.reasoning = clean_text(a.args.get("reason", ""))
            self.store.log(st, actor, "assign_task", f"{t.title} -> {t.owner}", "confirmed", before=before,
                           after=t.model_dump(mode="json"))
            return [{"type": "task_assignment", "id": t.id, "previous_owner": before["owner"] or ""}]
        if a.type == "notify":
            n = Notification(id=new_id("n"), to=a.args["to"], text=clean_text(a.args["text"], 500),
                             created_at=self.store.now(st))
            st.notifications.append(n)
            self.store.log(st, actor, "send_notification", f"To {n.to}: {n.text}", "confirmed")
            return [{"type": "notification", "id": n.id}]
        raise HomePilotError("unknown_action", a.type)

    def reject(self, hid: str, proposal_id: str, actor_id: str) -> dict:
        st = self.state(hid)
        actor = self.store.require_member(st, actor_id)
        with self.store.lock:
            prop = self._prop(st, proposal_id)
            if prop.status != "pending":
                raise HomePilotError("not_pending", f"Proposal is already {prop.status}.")
            prop.status = "rejected"
            self.store.log(st, actor, "reject_plan", "Rejected proposal", "rejected", after={"proposal_id": prop.id})
            self.store.flush()
        return {"status": "rejected"}

    def undo(self, hid: str, proposal_id: str, actor_id: str) -> dict:
        st = self.state(hid)
        actor = self.store.require_member(st, actor_id)
        with self.store.lock:
            prop = self._prop(st, proposal_id)
            if prop.status != "confirmed":
                raise HomePilotError("not_confirmed", "Only confirmed proposals can be undone.")
            for c in reversed(prop.created_entities):
                kind, eid = c["type"], c["id"]
                if kind == "event":
                    st.events.pop(eid, None)
                elif kind == "task":
                    st.tasks.pop(eid, None)
                elif kind == "shopping":
                    st.shopping.pop(eid, None)
                elif kind == "notification":
                    st.notifications = [n for n in st.notifications if n.id != eid]
                elif kind == "task_assignment" and eid in st.tasks:
                    st.tasks[eid].owner = c.get("previous_owner") or None
            prop.status = "undone"
            self.store.log(st, actor, "undo_plan", "Undid confirmed proposal", "undone", after={"proposal_id": prop.id})
            self.store.flush()
        return {"status": "undone"}

    def notify_stage(self, hid: str, actor_id: str, to: str, text: str) -> dict:
        st = self.state(hid)
        to_id = self.store.require_member(st, to)
        return self.stage(hid, actor_id, Action(type="notify", args={"to": to_id, "text": clean_text(text, 500)},
                                                rationale="Notifications are external, so they need approval."),
                          f"Notify {to_id}")
