from datetime import datetime, timezone

_events: list[dict] = []


def record_event(action: str, actor: str = "system", details: dict | None = None) -> dict:
    event = {
        "action": action,
        "actor": actor,
        "details": details or {},
        "at": datetime.now(timezone.utc).isoformat(),
    }
    _events.append(event)
    return event


def list_events(action: str | None = None) -> list[dict]:
    if action is None:
        return list(_events)
    return [event for event in _events if event["action"] == action]


def reset_events() -> None:
    _events.clear()
