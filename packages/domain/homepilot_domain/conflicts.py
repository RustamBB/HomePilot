"""Deterministic, LLM-independent conflict rules."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

from .models import Conflict, Event, Household, Task


@dataclass
class Fit:
    ok: bool
    blocking: Event | None = None
    next_event: Event | None = None
    slack_after_min: int | None = None  # spare minutes before the person's next commitment


def person_events(person_id: str, events: list[Event]) -> list[Event]:
    return sorted(
        (e for e in events if person_id in e.attendees or e.owner == person_id),
        key=lambda e: e.start,
    )


def _need(a: Event, b: Event) -> timedelta:
    return timedelta(minutes=max(a.travel_minutes, b.travel_minutes))


def _gap_too_small(a: Event, b: Event) -> bool:
    """True when two non-overlapping events leave less than the travel time between them."""
    first, second = (a, b) if a.start <= b.start else (b, a)
    return second.start - first.end < _need(a, b)


def fit(person_id: str, candidate: Event, events: list[Event]) -> Fit:
    """Can `person_id` attend `candidate` given their other commitments and travel time?"""
    nxt: Event | None = None
    for e in person_events(person_id, events):
        if e.id == candidate.id:
            continue
        overlaps = candidate.start < e.end and e.start < candidate.end
        if overlaps or _gap_too_small(candidate, e):
            return Fit(False, blocking=e)
        if e.start >= candidate.end and nxt is None:
            nxt = e
    slack = None
    if nxt is not None:
        slack = int((nxt.start - candidate.end - _need(candidate, nxt)).total_seconds() // 60)
    return Fit(True, next_event=nxt, slack_after_min=slack)


def detect(household: Household, events: list[Event], tasks: list[Task], now: datetime) -> list[Conflict]:
    out: list[Conflict] = []
    name = lambda pid: (household.person(pid).display_name if household.person(pid) else pid)  # noqa: E731

    # 1. Time conflicts between events that share a person.
    for i, a in enumerate(events):
        for b in events[i + 1:]:
            for pid in set(a.attendees) & set(b.attendees):
                if a.start < b.end and b.start < a.end:
                    out.append(Conflict(
                        kind="time_overlap", severity="high", subjects=[a.id, b.id, pid],
                        message=f"{name(pid)} is double-booked: '{a.title}' overlaps '{b.title}'.",
                        options=[f"Reschedule '{a.title}'", f"Reschedule '{b.title}'",
                                 "Ask another family member to cover one of them"]))
                elif _gap_too_small(a, b):
                    out.append(Conflict(
                        kind="travel_buffer", severity="medium", subjects=[a.id, b.id, pid],
                        message=f"{name(pid)} lacks travel time between '{a.title}' and '{b.title}'.",
                        options=["Leave early", "Ask another family member to cover one of them"]))

    # 2. Events that need an adult but have none.
    for e in events:
        adults = [pid for pid in e.attendees + ([e.owner] if e.owner else [])
                  if (p := household.person(pid)) and p.is_adult]
        if e.needs_adult and not adults and e.end > now:
            out.append(Conflict(
                kind="unowned_event", severity="high", subjects=[e.id],
                message=f"'{e.title}' needs an adult but nobody is assigned.",
                options=["Assign an adult", "Reschedule"]))

    # 3. Tasks: unowned critical/soon-due, overdue, overloaded owners.
    open_tasks = [t for t in tasks if t.status == "open"]
    for t in open_tasks:
        soon = t.due_at is not None and t.due_at - now <= timedelta(hours=48)
        if t.due_at is not None and t.due_at < now:
            out.append(Conflict(kind="overdue", severity="high", subjects=[t.id],
                                message=f"'{t.title}' is overdue.", options=["Do it now", "Move the deadline"]))
        elif t.owner is None and (t.priority == "high" or soon):
            out.append(Conflict(kind="unowned_task", severity="high", subjects=[t.id],
                                message=f"'{t.title}' has no owner and is {'high priority' if t.priority == 'high' else 'due soon'}.",
                                options=["Assign an owner"]))
    by_day: dict[tuple[str, object], int] = {}
    for t in open_tasks:
        if t.owner and t.due_at:
            by_day[(t.owner, t.due_at.date())] = by_day.get((t.owner, t.due_at.date()), 0) + 1
    for (pid, day), n in by_day.items():
        if n >= 3:
            out.append(Conflict(kind="overloaded", severity="medium", subjects=[pid],
                                message=f"{name(pid)} has {n} tasks due on {day:%a %b %d}.",
                                options=["Reassign one task"]))
    return out
