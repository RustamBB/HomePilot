"""Constraint-aware planner. Pure rules: the LLM extracts commitments, this decides ownership."""
from __future__ import annotations

from datetime import datetime, timedelta

from . import conflicts as cf
from .errors import HomePilotError
from .models import Action, Commitment, Conflict, Event, Household, Person, Proposal
from .sanitize import clean_text
from .store import HouseholdState, new_id

DEFAULT_APPT_MIN = 45
DEFAULT_TRAVEL_MIN = 15


def _fmt(dt: datetime) -> str:
    return dt.strftime("%H:%M").lstrip("0") if dt.minute else dt.strftime("%-H:00")


def build_plan(st: HouseholdState, commitments: list[Commitment], actor_id: str, now: datetime,
               message: str = "") -> Proposal:
    hh = st.household
    working: list[Event] = list(st.events.values())  # existing + hypothetical events
    actions: list[Action] = []
    conflicts: list[Conflict] = []
    rationale: list[str] = []
    considered: list[str] = []
    load: dict[str, int] = {p.id: 0 for p in hh.people if p.is_adult}
    for t in st.tasks.values():
        if t.status == "open" and t.owner in load:
            load[t.owner] += 1
    confidence = "high"
    appointment_owners: list[str] = []

    def person_of(ref: str | None) -> Person | None:
        return hh.person(ref)

    # 1. Constraints -> busy events (hard facts from the message).
    for c in (c for c in commitments if c.kind == "constraint"):
        p = person_of(c.person) or person_of(actor_id)
        if not p or not c.start:
            continue
        end = c.end or c.start + timedelta(hours=8)
        title = clean_text(c.title)
        if any(e.kind == "busy" and p.id in e.attendees and e.start == c.start for e in working):
            considered.append(f"{p.display_name}: {title} from {_fmt(c.start)} (already recorded)")
            continue
        ev = Event(id=new_id("ev"), title=f"{p.display_name}: {title}", start=c.start, end=end, kind="busy",
                   attendees=[p.id], source="agent")
        working.append(ev)
        actions.append(Action(type="create_event", args=ev.model_dump(mode="json"),
                              rationale=f"Recorded from your message: {p.display_name} is busy from {_fmt(c.start)}."))
        considered.append(f"{p.display_name}: {title} from {_fmt(c.start)}")

    # 2. Appointments -> pick an available adult.
    for c in (c for c in commitments if c.kind == "appointment"):
        if not c.start:
            raise HomePilotError("invalid_commitment", f"Appointment '{c.title}' needs a start time.")
        subject = person_of(c.person)
        travel = c.travel_minutes if c.travel_minutes is not None else DEFAULT_TRAVEL_MIN
        ev = Event(id=new_id("ev"), title=clean_text(c.title), start=c.start,
                   end=c.end or c.start + timedelta(minutes=DEFAULT_APPT_MIN), kind="appointment",
                   attendees=[subject.id] if subject else [], needs_adult=True, travel_minutes=travel, source="agent")
        ok: list[tuple[Person, cf.Fit]] = []
        for p in (p for p in hh.people if p.is_adult):
            f = cf.fit(p.id, ev, working)
            if f.ok:
                ok.append((p, f))
            else:
                b = f.blocking
                rationale.append(f"{p.display_name} can't take '{ev.title}': '{b.title}' "
                                 f"({_fmt(b.start)}-{_fmt(b.end)}) conflicts with {_fmt(ev.start)}-{_fmt(ev.end)} "
                                 f"plus {travel} min travel.")
        if not ok:
            confidence = "low"
            conflicts.append(Conflict(
                kind="no_available_adult", severity="high", subjects=[ev.id],
                message=f"No adult is free for '{ev.title}' at {_fmt(ev.start)}.",
                options=["Reschedule the appointment", "Ask a caregiver or relative",
                         "Move one adult's commitment (needs that person's approval)"]))
            actions.append(Action(type="create_event", args=ev.model_dump(mode="json"),
                                  rationale="No adult is available; saved without an owner so it stays visible as a conflict."))
            working.append(ev)
            continue
        pref = hh.preferences.get("appointments")
        ok.sort(key=lambda pf: (pf[0].id != pref, load[pf[0].id], -(pf[1].slack_after_min or 10**6)))
        owner, f = ok[0]
        ev.owner = owner.id
        ev.attendees = list(dict.fromkeys([*ev.attendees, owner.id]))
        load[owner.id] += 1
        appointment_owners.append(owner.id)
        slack = ""
        if f.next_event is not None:
            s = f.slack_after_min or 0
            slack = (f" After the appointment and {travel} min of travel, {owner.display_name} reaches "
                     f"'{f.next_event.title}' at {_fmt(f.next_event.start)} with "
                     f"{'no spare time' if s == 0 else f'{s} min to spare'}.")
        rationale.append(f"{owner.display_name} takes '{ev.title}': free at {_fmt(ev.start)}.{slack}")
        if len(ok) > 1:
            confidence = "medium"
            alts = ", ".join(p.display_name for p, _ in ok[1:])
            conflicts.append(Conflict(kind="ambiguous_owner", severity="low", subjects=[ev.id],
                                      message=f"{alts} could also take '{ev.title}'; {owner.display_name} was chosen by lowest load.",
                                      options=[f"Assign to {p.display_name}" for p, _ in ok[1:]]))
        working.append(ev)
        actions.append(Action(type="create_event", args=ev.model_dump(mode="json"),
                              rationale=f"{owner.display_name} is the only/best available adult."))

    # 3. Shopping -> whoever is already out, else lowest load.
    for c in (c for c in commitments if c.kind == "shopping"):
        who = None
        if appointment_owners:
            who = person_of(appointment_owners[0])
            why = f"{who.display_name} is already out for '{_first_appt(commitments)}'; pick it up on the return route."
        else:
            who = min((p for p in hh.people if p.is_adult), key=lambda p: load[p.id], default=None)
            why = f"{who.display_name} has the lightest load." if who else "No adult available."
        if who:
            load[who.id] += 1
        rationale.append(f"'{clean_text(c.title)}' goes to {who.display_name if who else 'nobody yet'}: {why}")
        actions.append(Action(type="add_shopping",
                              args={"id": new_id("s"), "name": clean_text(c.title), "quantity": "1",
                                    "priority": c.priority, "assigned_to": who.id if who else None,
                                    "note": "return route" if appointment_owners else ""},
                              rationale=why))

    # 4. Tasks -> explicit person, else balance load away from people who already have errands.
    for c in (c for c in commitments if c.kind == "task"):
        who = person_of(c.person) or min((p for p in hh.people if p.is_adult), key=lambda p: load[p.id])
        load[who.id] += 1
        others = [p.display_name for p in hh.people if p.is_adult and p.id != who.id and load[p.id] > load[who.id]]
        why = (f"{others[0]} already has more in this plan, so this keeps the load balanced."
               if others else f"{who.display_name} has the lightest load.")
        rationale.append(f"'{clean_text(c.title)}' goes to {who.display_name}: {why}")
        if c.due_at and c.due_at - now <= timedelta(hours=72):
            considered.append(f"Deadline: {clean_text(c.title)} due {c.due_at:%a %b %d %H:%M}")
        actions.append(Action(type="create_task",
                              args={"id": new_id("t"), "title": clean_text(c.title), "owner": who.id,
                                    "due_at": c.due_at.isoformat() if c.due_at else None, "priority": c.priority,
                                    "source": "agent", "reasoning": why},
                              rationale=why))

    # 5. Notify each assignee (other than the requester) — external, so it needs confirmation too.
    notified: dict[str, list[str]] = {}
    for a in actions:
        if a.type == "create_event" and a.args.get("kind") == "busy":
            continue
        owner = a.args.get("owner") or a.args.get("assigned_to")
        if owner and owner != actor_id:
            notified.setdefault(owner, []).append(a.args.get("title") or a.args.get("name"))
    for pid, titles in notified.items():
        actions.append(Action(type="notify", args={"to": pid, "text": "You're on: " + "; ".join(titles)},
                              rationale="Each person only hears about what they own."))

    return Proposal(id=new_id("prop"), message=clean_text(message, 1000), actions=actions, conflicts=conflicts,
                    rationale=rationale, constraints_considered=considered, confidence=confidence,
                    created_at=now)


def _first_appt(commitments: list[Commitment]) -> str:
    return next((clean_text(c.title) for c in commitments if c.kind == "appointment"), "an errand")
