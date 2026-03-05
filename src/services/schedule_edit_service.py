from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, TypedDict

from src.services.audit_log import record_event

_schedules: dict[int, "ScheduleRecord"] = {}


class SessionRecord(TypedDict):
    title: str
    room: str
    start_time: str
    end_time: str


class ScheduleRecord(TypedDict):
    id: int
    status: str
    sessions: list[SessionRecord]
    notes: str
    updated_at: str


def _to_datetime(raw: str, field: str) -> datetime:
    try:
        return datetime.fromisoformat(raw)
    except ValueError as exc:
        raise ValueError(f"{field} must be a valid ISO-8601 datetime.") from exc


def _normalize_sessions(sessions: list[dict[str, Any]]) -> list[SessionRecord]:
    if not sessions:
        raise ValueError("At least one session is required.")

    normalized: list[SessionRecord] = []
    for index, session in enumerate(sessions):
        title = str(session.get("title", "")).strip()
        room = str(session.get("room", "")).strip()
        start_time = str(session.get("start_time", "")).strip()
        end_time = str(session.get("end_time", "")).strip()

        if not title:
            raise ValueError(f"Session {index + 1} title is required.")
        if not room:
            raise ValueError(f"Session {index + 1} room is required.")
        if not start_time or not end_time:
            raise ValueError(f"Session {index + 1} start_time and end_time are required.")

        start_dt = _to_datetime(start_time, "start_time")
        end_dt = _to_datetime(end_time, "end_time")
        if start_dt >= end_dt:
            raise ValueError(f"Session {index + 1} start_time must be earlier than end_time.")

        normalized.append(
            {
                "title": title,
                "room": room,
                "start_time": start_dt.isoformat(),
                "end_time": end_dt.isoformat(),
            }
        )
    return normalized


def _validate_room_conflicts(sessions: list[SessionRecord]) -> None:
    for index, session in enumerate(sessions):
        left_start = datetime.fromisoformat(session["start_time"])
        left_end = datetime.fromisoformat(session["end_time"])
        for other in sessions[index + 1 :]:
            if session["room"] != other["room"]:
                continue
            right_start = datetime.fromisoformat(other["start_time"])
            right_end = datetime.fromisoformat(other["end_time"])
            overlaps = left_start < right_end and right_start < left_end
            if overlaps:
                raise ValueError("Schedule conflict detected: overlapping sessions in the same room.")


def edit_schedule(
    schedule_id: str,
    sessions: list[dict[str, Any]],
    *,
    notes: str = "",
    editor_id: str = "editor",
) -> ScheduleRecord:
    if not schedule_id.isdigit() or int(schedule_id) <= 0:
        raise ValueError("Schedule ID is invalid.")

    normalized_sessions = _normalize_sessions(sessions)
    _validate_room_conflicts(normalized_sessions)

    schedule: ScheduleRecord = {
        "id": int(schedule_id),
        "status": "draft",
        "sessions": normalized_sessions,
        "notes": notes.strip(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    _schedules[schedule["id"]] = schedule

    record_event(
        "schedule_edit",
        actor=editor_id.strip() or "editor",
        details={"schedule_id": schedule["id"], "session_count": len(normalized_sessions)},
    )
    return dict(schedule)


def get_schedule(schedule_id: str) -> ScheduleRecord | None:
    if not schedule_id.isdigit():
        return None
    schedule = _schedules.get(int(schedule_id))
    if schedule is None:
        return None
    return dict(schedule)


def execute(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    schedule = edit_schedule(
        schedule_id=str(data.get("schedule_id", "")),
        sessions=list(data.get("sessions", [])),
        notes=str(data.get("notes", "")),
        editor_id=str(data.get("editor_id", "editor")),
    )
    return {"service": "schedule_edit_service", "schedule": schedule}


def reset_schedule_edit_state() -> None:
    _schedules.clear()
