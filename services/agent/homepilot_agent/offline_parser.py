"""Deterministic rule-based extractor used when Bedrock is unavailable (and for stable demos/tests).

It emits the same `Commitment` schema the LLM is asked to produce, so everything downstream is identical.
"""
from __future__ import annotations

import re
from datetime import datetime, timedelta

_WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
_TIME = r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)?"


def _to_dt(day: datetime, h: str, m: str | None, ap: str | None, school_hours: bool = True) -> datetime:
    hour, minute = int(h), int(m or 0)
    if ap == "pm" and hour < 12:
        hour += 12
    elif ap == "am" and hour == 12:
        hour = 0
    elif ap is None and school_hours and 1 <= hour <= 6:
        hour += 12  # "at 3" in a family context means afternoon
    return day.replace(hour=hour, minute=minute, second=0, microsecond=0)


def _day_for(sentence: str, now: datetime) -> datetime:
    s = sentence.lower()
    base = now.replace(hour=0, minute=0, second=0, microsecond=0)
    if "tomorrow" in s:
        return base + timedelta(days=1)
    if "today" in s or "tonight" in s:
        return base
    for i, d in enumerate(_WEEKDAYS):
        if d in s:
            return base + timedelta(days=(i - now.weekday()) % 7 or 7)
    return base + timedelta(days=1)


def parse(message: str, household: dict, actor_id: str, now: datetime) -> list[dict]:
    people = household["people"]
    names = {p["display_name"].lower(): p["id"] for p in people}
    children = [p for p in people if p["role"] == "child"]
    sole_child = children[0]["id"] if len(children) == 1 else None
    default_day = _day_for(message, now)
    out: list[dict] = []

    def who(sentence: str) -> str | None:
        s = sentence.lower()
        for name, pid in names.items():
            if re.search(rf"\b{re.escape(name)}\b", s):
                return pid
        if re.search(r"\b(i|i'm|i’m)\b", s):
            return actor_id
        return None

    for raw in re.split(r"[.;]|,\s*(?:and\s+)?|\band\b(?=\s+(?:[A-Z]|the|we|our|i)\b)", message):
        s = raw.strip()
        if not s:
            continue
        sl = s.lower()
        day = _day_for(sl, now) if re.search(r"tomorrow|today|tonight|" + "|".join(_WEEKDAYS), sl) else default_day
        t = re.search(rf"\bat\s+{_TIME}", sl) or re.search(rf"\b{_TIME}\b(?=\s*$)", sl)

        if re.search(r"doctor|dentist|pediatric|appointment|checkup|vaccin", sl) and t:
            subject = who(sl) if re.search(r"\b(?:"+"|".join(map(re.escape, names))+r")\b", sl) else None
            subject = subject or (sole_child if re.search(r"\b(child|kid|son|daughter)\b", sl) else sole_child)
            kind_title = "dentist" if "dentist" in sl else "doctor"
            title = f"{next((p['display_name'] for p in people if p['id'] == subject), 'Child')}: {kind_title} appointment"
            out.append({"kind": "appointment", "title": title, "person": subject,
                        "start": _to_dt(day, *t.groups(), school_hours=False).isoformat(), "needs_adult": True})
        elif re.search(r"start(?:s)? work|work starts|have to be at work|shift", sl) and t:
            out.append({"kind": "constraint", "title": "starts work", "person": who(sl) or actor_id,
                        "start": _to_dt(day, *t.groups(), school_hours=False).isoformat()})
        elif re.search(r"\bclass\b|lecture|meeting|practice|game", sl) and t:
            start = _to_dt(day, *t.groups())
            out.append({"kind": "constraint", "title": "has class" if "class" in sl else "is busy", "person": who(sl),
                        "start": start.isoformat(), "end": (start + timedelta(hours=2)).isoformat()})
        elif m := re.search(r"(?:out of|need|low on|running low on|buy|get)\s+(?:some\s+)?([a-z][a-z ]{1,30})", sl):
            item = re.sub(r"\b(from|at|on|for|tomorrow|today|and)\b.*", "", m.group(1)).strip()
            if item:
                out.append({"kind": "shopping", "title": item.title(), "priority": "normal"})
        elif m := re.search(r"(?:the\s+)?([a-z ]*?(?:project|homework|essay|report|form|permission slip))\b.*?due\s+(\w+)", sl):
            due_day = _day_for(m.group(2), now)
            out.append({"kind": "task", "title": m.group(1).strip().title(), "priority": "high",
                        "due_at": due_day.replace(hour=8).isoformat()})
    return out
