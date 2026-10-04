"""Treat user/task text as data: strip control characters and cap length."""
import re

_CTRL = re.compile(r"[\x00-\x08\x0b-\x1f\x7f]")


def clean_text(value: str, limit: int = 200) -> str:
    value = _CTRL.sub("", value or "").strip()
    return value[:limit]
