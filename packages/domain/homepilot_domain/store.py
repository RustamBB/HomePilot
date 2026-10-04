"""Household state store. In-memory with optional JSON persistence; one state object per household."""
from __future__ import annotations

import threading
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from .backends import Backend, JsonFileBackend
from .errors import HomePilotError
from .models import AuditEvent, Event, Household, Notification, Proposal, ShoppingItem, Task


class HouseholdState(BaseModel):
    household: Household
    events: dict[str, Event] = Field(default_factory=dict)
    tasks: dict[str, Task] = Field(default_factory=dict)
    shopping: dict[str, ShoppingItem] = Field(default_factory=dict)
    proposals: dict[str, Proposal] = Field(default_factory=dict)
    audit: list[AuditEvent] = Field(default_factory=list)
    notifications: list[Notification] = Field(default_factory=list)
    demo_now: datetime | None = None


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


class Store:
    """Households are isolated by id; unknown ids are denied (no cross-household access)."""

    def __init__(self, path: str | Path | None = None, backend: Backend | None = None):
        self._lock = threading.RLock()
        self._backend: Backend | None = backend or (JsonFileBackend(path) if path else None)
        self._states: dict[str, HouseholdState] = {}
        if self._backend:
            self._states = {k: HouseholdState.model_validate_json(v) for k, v in self._backend.load_all().items()}

    def has(self, household_id: str) -> bool:
        return household_id in self._states

    @property
    def lock(self) -> threading.RLock:
        return self._lock

    def put(self, state: HouseholdState) -> None:
        with self._lock:
            self._states[state.household.id] = state
            self.flush()

    def get(self, household_id: str) -> HouseholdState:
        try:
            return self._states[household_id]
        except KeyError:
            raise HomePilotError("household_not_found", f"Unknown household '{household_id}'.") from None

    def now(self, st: HouseholdState) -> datetime:
        return st.demo_now or datetime.now().replace(microsecond=0)

    def require_member(self, st: HouseholdState, person_id: str) -> str:
        p = st.household.person(person_id)
        if not p:
            raise HomePilotError("person_not_in_household", f"'{person_id}' is not a member of this household.")
        return p.id

    def log(self, st: HouseholdState, actor: str, tool: str, summary: str, approval: str = "n/a",
            before: Any = None, after: Any = None) -> AuditEvent:
        ev = AuditEvent(id=new_id("aud"), timestamp=self.now(st), actor=actor, tool=tool, summary=summary,
                        approval_state=approval, before=before, after=after)
        st.audit.append(ev)
        return ev

    def flush(self) -> None:
        if self._backend:
            for hid, st in self._states.items():
                self._backend.save(hid, st.model_dump_json())
