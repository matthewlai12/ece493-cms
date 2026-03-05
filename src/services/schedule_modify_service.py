from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, TypedDict

from src.services.audit_log import record_event
from src.services.schedule_generate_service import (
    GeneratedSession,
    get_generated_schedule,
    set_generated_schedule,
)

_modified_schedules: dict[int, "ModifiedSchedule"] = {}


class ModifiedSchedule(TypedDict):
    id: int
    status: str
    generated_at: str
    modified_at: str
    notes: str
    sessions: list[GeneratedSession]


def _normalize_sessions(sessions: list[dict[str, Any]]) -> list[GeneratedSession]:
    normalized: list[GeneratedSession] = []
    for index, session in enumerate(sessions):
        submission_id = str(session.get("submission_id", "")).strip()
        title = str(session.get("title", "")).strip()
        room = str(session.get("room", "")).strip()
        start_time = str(session.get("start_time", "")).strip()
        end_time = str(session.get("end_time", "")).strip()

        if not submission_id.isdigit() or int(submission_id) <= 0:
            raise ValueError(f"Session {index + 1} has an invalid submission_id.")
        if not title:
            raise ValueError(f"Session {index + 1} title is required.")
        if not room:
            raise ValueError(f"Session {index + 1} room is required.")
        if not start_time or not end_time:
            raise ValueError(f"Session {index + 1} start_time and end_time are required.")

        try:
            start_dt = datetime.fromisoformat(start_time)
            end_dt = datetime.fromisoformat(end_time)
        except ValueError as exc:
            raise ValueError("Session times must be valid ISO-8601 datetimes.") from exc

        if start_dt >= end_dt:
            raise ValueError(f"Session {index + 1} start_time must be earlier than end_time.")

        normalized.append(
            {
                "submission_id": int(submission_id),
                "title": title,
                "room": room,
                "start_time": start_dt.isoformat(),
                "end_time": end_dt.isoformat(),
            }
        )
    return normalized


def _validate_constraints(sessions: list[GeneratedSession]) -> None:
    seen_submission_ids: set[int] = set()
    for session in sessions:
        submission_id = int(session["submission_id"])
        if submission_id in seen_submission_ids:
            raise ValueError("Each submission can only appear once in a modified schedule.")
        seen_submission_ids.add(submission_id)

    for index, left in enumerate(sessions):
        left_start = datetime.fromisoformat(left["start_time"])
        left_end = datetime.fromisoformat(left["end_time"])
        for right in sessions[index + 1 :]:
            right_start = datetime.fromisoformat(right["start_time"])
            right_end = datetime.fromisoformat(right["end_time"])
            overlaps = left_start < right_end and right_start < left_end
            if overlaps and left["room"] == right["room"]:
                raise ValueError("Schedule conflict detected: overlapping sessions in the same room.")


def modify_schedule(
    schedule_id: str,
    sessions: list[dict[str, Any]],
    *,
    notes: str = "",
    admin_id: str = "admin",
) -> ModifiedSchedule:
    if not schedule_id.isdigit() or int(schedule_id) <= 0:
        raise ValueError("Schedule ID is invalid.")
    if not sessions:
        raise ValueError("At least one session is required for modification.")

    original = get_generated_schedule(schedule_id)
    if original is None:
        raise ValueError("Selected generated schedule does not exist.")

    normalized_sessions = _normalize_sessions(sessions)
    _validate_constraints(normalized_sessions)

    modified: ModifiedSchedule = {
        "id": int(schedule_id),
        "status": "draft",
        "generated_at": str(original.get("generated_at")),
        "modified_at": datetime.now(timezone.utc).isoformat(),
        "notes": notes.strip(),
        "sessions": normalized_sessions,
    }
    _modified_schedules[modified["id"]] = modified
    set_generated_schedule(
        {
            "id": modified["id"],
            "status": modified["status"],
            "generated_at": modified["generated_at"],
            "sessions": modified["sessions"],
        }
    )
    record_event(
        "schedule_modify",
        actor=admin_id.strip() or "admin",
        details={"schedule_id": modified["id"], "session_count": len(normalized_sessions)},
    )
    return dict(modified)


def get_modified_schedule(schedule_id: str) -> ModifiedSchedule | None:
    if not schedule_id.isdigit():
        return None
    schedule = _modified_schedules.get(int(schedule_id))
    if schedule is None:
        return None
    return dict(schedule)


def execute(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    schedule = modify_schedule(
        schedule_id=str(data.get("schedule_id", "")),
        sessions=list(data.get("sessions", [])),
        notes=str(data.get("notes", "")),
        admin_id=str(data.get("admin_id", "admin")),
    )
    return {"service": "schedule_modify_service", "schedule": schedule}


def reset_schedule_modify_state() -> None:
    _modified_schedules.clear()
