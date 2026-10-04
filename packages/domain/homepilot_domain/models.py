"""Household data model (see docs/spec, section 10)."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

Role = Literal["parent", "caregiver", "teen", "child"]
ADULT_ROLES = ("parent", "caregiver")


class Person(BaseModel):
    id: str
    display_name: str
    role: Role
    notification_style: str = "brief"
    responsibilities: list[str] = Field(default_factory=list)

    @property
    def is_adult(self) -> bool:
        return self.role in ADULT_ROLES


class Household(BaseModel):
    id: str
    name: str
    timezone: str = "America/Los_Angeles"
    quiet_hours: str = "21:00-07:00"
    preferences: dict[str, str] = Field(default_factory=dict)
    people: list[Person] = Field(default_factory=list)

    def person(self, ref: str | None) -> Person | None:
        """Resolve a person by id or (case-insensitive) display name."""
        if not ref:
            return None
        ref_l = ref.strip().lower()
        for p in self.people:
            if p.id.lower() == ref_l or p.display_name.lower() == ref_l:
                return p
        return None


class Event(BaseModel):
    id: str
    title: str
    start: datetime
    end: datetime
    kind: Literal["appointment", "busy", "activity", "other"] = "other"
    attendees: list[str] = Field(default_factory=list)
    owner: str | None = None  # the responsible adult, if any
    needs_adult: bool = False
    travel_minutes: int = 0
    source: str = "user"


class Task(BaseModel):
    id: str
    title: str
    status: Literal["open", "done"] = "open"
    owner: str | None = None
    due_at: datetime | None = None
    priority: Literal["high", "normal", "low"] = "normal"
    dependencies: list[str] = Field(default_factory=list)
    effort_min: int | None = None
    source: str = "user"
    reasoning: str = ""


class ShoppingItem(BaseModel):
    id: str
    name: str
    quantity: str = "1"
    priority: Literal["high", "normal", "low"] = "normal"
    assigned_to: str | None = None
    status: Literal["needed", "done"] = "needed"
    note: str = ""


class Commitment(BaseModel):
    """One obligation extracted from natural language (by an LLM or the offline parser)."""

    kind: Literal["appointment", "constraint", "shopping", "task"]
    title: str
    person: str | None = None  # id or display name
    start: datetime | None = None
    end: datetime | None = None
    due_at: datetime | None = None
    needs_adult: bool = False
    travel_minutes: int | None = None
    priority: Literal["high", "normal", "low"] = "normal"


class Action(BaseModel):
    type: Literal["create_event", "create_task", "add_shopping", "assign_task", "notify"]
    args: dict[str, Any]
    rationale: str = ""
    requires_confirmation: bool = True


class Conflict(BaseModel):
    kind: str
    severity: Literal["high", "medium", "low"]
    subjects: list[str] = Field(default_factory=list)
    message: str
    options: list[str] = Field(default_factory=list)


class Proposal(BaseModel):
    id: str
    message: str = ""
    actions: list[Action] = Field(default_factory=list)
    conflicts: list[Conflict] = Field(default_factory=list)
    rationale: list[str] = Field(default_factory=list)
    constraints_considered: list[str] = Field(default_factory=list)
    confidence: Literal["high", "medium", "low"] = "high"
    confirmation_required: bool = True
    status: Literal["pending", "confirmed", "rejected", "undone"] = "pending"
    created_at: datetime
    created_entities: list[dict[str, str]] = Field(default_factory=list)


class AuditEvent(BaseModel):
    id: str
    timestamp: datetime
    actor: str
    tool: str
    summary: str
    approval_state: Literal["proposed", "confirmed", "rejected", "undone", "n/a"] = "n/a"
    before: Any = None
    after: Any = None


class Notification(BaseModel):
    id: str
    to: str
    text: str
    created_at: datetime
