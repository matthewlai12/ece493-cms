from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timedelta, timezone
from typing import Any, TypedDict

from src.services.audit_log import record_event

_generated_schedules: dict[int, "GeneratedSchedule"] = {}


class GeneratedSession(TypedDict):
    submission_id: int
    title: str
    room: str
    start_time: str
    end_time: str


class GeneratedSchedule(TypedDict):
    id: int
    status: str
    generated_at: str
    sessions: list[GeneratedSession]


def _iso_to_datetime(raw: str, field_name: str) -> datetime:
    try:
        return datetime.fromisoformat(raw)
    except ValueError as exc:
        raise ValueError(f"{field_name} must be a valid ISO-8601 datetime.") from exc


def generate_schedule(
    schedule_id: str,
    accepted_submissions: list[dict[str, Any]],
    rooms: list[str],
    slot_start: str,
    slot_minutes: int,
    *,
    generator_id: str = "scheduler",
) -> GeneratedSchedule:
    if not schedule_id.isdigit() or int(schedule_id) <= 0:
        raise ValueError("Schedule ID is invalid.")
    if not accepted_submissions:
        raise ValueError("At least one accepted submission is required.")
    clean_rooms = [room.strip() for room in rooms if room.strip()]
    if not clean_rooms:
        raise ValueError("At least one room is required.")
    if slot_minutes <= 0:
        raise ValueError("slot_minutes must be greater than zero.")

    start = _iso_to_datetime(slot_start, "slot_start")
    sessions: list[GeneratedSession] = []
    for index, submission in enumerate(accepted_submissions):
        submission_id = str(submission.get("submission_id", "")).strip()
        title = str(submission.get("title", "")).strip()
        if not submission_id.isdigit() or int(submission_id) <= 0:
            raise ValueError(f"Submission {index + 1} has an invalid submission_id.")
        if not title:
            raise ValueError(f"Submission {index + 1} title is required.")

        room_idx = index % len(clean_rooms)
        round_idx = index // len(clean_rooms)
        start_dt = start + timedelta(minutes=round_idx * slot_minutes)
        end_dt = start_dt + timedelta(minutes=slot_minutes)
        sessions.append(
            {
                "submission_id": int(submission_id),
                "title": title,
                "room": clean_rooms[room_idx],
                "start_time": start_dt.isoformat(),
                "end_time": end_dt.isoformat(),
            }
        )

    generated: GeneratedSchedule = {
        "id": int(schedule_id),
        "status": "draft",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sessions": sessions,
    }
    _generated_schedules[generated["id"]] = generated
    record_event(
        "schedule_generate",
        actor=generator_id.strip() or "scheduler",
        details={"schedule_id": generated["id"], "session_count": len(sessions)},
    )
    return dict(generated)


def get_generated_schedule(schedule_id: str) -> GeneratedSchedule | None:
    if not schedule_id.isdigit():
        return None
    schedule = _generated_schedules.get(int(schedule_id))
    if schedule is None:
        return None
    return deepcopy(schedule)


def set_generated_schedule(schedule: GeneratedSchedule) -> None:
    _generated_schedules[int(schedule["id"])] = deepcopy(schedule)


def execute(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    schedule = generate_schedule(
        schedule_id=str(data.get("schedule_id", "")),
        accepted_submissions=list(data.get("accepted_submissions", [])),
        rooms=list(data.get("rooms", [])),
        slot_start=str(data.get("slot_start", "")),
        slot_minutes=int(data.get("slot_minutes", 30)),
        generator_id=str(data.get("generator_id", "scheduler")),
    )
    return {"service": "schedule_generate_service", "schedule": schedule}


def reset_schedule_generate_state() -> None:
    _generated_schedules.clear()
