from datetime import datetime

import pytest

from homepilot_agent import offline_parser
from homepilot_domain import Commitment, seed_demo

NOW = datetime(2026, 10, 16, 18, 30)
HH = seed_demo().household.model_dump(mode="json")


def kinds(msg):
    out = offline_parser.parse(msg, HH, "sam", NOW)
    [Commitment.model_validate(c) for c in out]  # schema-valid
    return sorted(c["kind"] for c in out)


def test_one_commitment():
    assert kinds("We are out of milk.") == ["shopping"]


def test_three_commitments():
    assert kinds("Maya has the dentist tomorrow at 2, we need eggs, and the history essay is due Monday.") == \
        ["appointment", "shopping", "task"]


def test_golden_scenario_commitments():
    got = kinds("Tomorrow our child has the doctor at 9. I start work at 8:30, Ali has class at 10, "
                "we are out of milk, and the science project is due Monday.")
    assert got == ["appointment", "constraint", "constraint", "shopping", "task"]


def test_nothing_to_plan():
    assert kinds("hello there") == []
