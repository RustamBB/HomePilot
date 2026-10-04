"""Deterministic synthetic household for the public demo (no real data)."""
from __future__ import annotations

from datetime import datetime

from .models import Event, Household, Person, ShoppingItem, Task
from .store import HouseholdState

DEMO_HOUSEHOLD_ID = "demo"
# Friday evening before the golden scenario.
DEMO_NOW = datetime(2026, 10, 16, 18, 30)


def seed_demo() -> HouseholdState:
    hh = Household(
        id=DEMO_HOUSEHOLD_ID, name="The Rivera-Khan family", timezone="America/Los_Angeles",
        preferences={"quiet_hours": "21:00-07:00", "brief_time": "07:30"},
        people=[
            Person(id="sam", display_name="Sam", role="parent", responsibilities=["school", "homework"]),
            Person(id="ali", display_name="Ali", role="parent", responsibilities=["groceries"]),
            Person(id="maya", display_name="Maya", role="child", notification_style="none"),
            Person(id="leo", display_name="Leo", role="teen", responsibilities=["dishes"]),
        ])
    st = HouseholdState(household=hh, demo_now=DEMO_NOW)
    ev = [
        Event(id="ev_soccer", title="Leo: soccer practice", start=datetime(2026, 10, 17, 15), end=datetime(2026, 10, 17, 16, 30),
              kind="activity", attendees=["leo"], source="seed"),
        Event(id="ev_dinner", title="Family dinner", start=datetime(2026, 10, 16, 19), end=datetime(2026, 10, 16, 20),
              kind="other", attendees=["sam", "ali", "maya", "leo"], source="seed"),
    ]
    st.events = {e.id: e for e in ev}
    st.tasks = {"t_recycle": Task(id="t_recycle", title="Take out recycling", owner="leo", due_at=datetime(2026, 10, 17, 10),
                                  priority="low", source="seed")}
    st.shopping = {"s_eggs": ShoppingItem(id="s_eggs", name="Eggs", quantity="12")}
    return st
