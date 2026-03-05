from datetime import datetime, timezone
from uuid import uuid4

_STATE: dict[str, list[dict]] = {
    "submissions": [],
    "invitations": [],
    "reviews": [],
    "decisions": [],
    "registrations": [],
    "payments": [],
    "schedules": [],
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _next_id(bucket: str) -> int:
    return len(_STATE[bucket]) + 1


def _find(bucket: str, key: str, value: str) -> dict | None:
    for item in _STATE[bucket]:
        if str(item.get(key)) == str(value):
            return item
    return None


def perform_use_case(service: str, payload: dict) -> dict:
    data = payload or {}

    if service == "auth_login_service":
        email = str(data.get("email", "")).strip().lower()
        password = str(data.get("password", ""))
        ok = bool(email and password)
        return {"service": service, "authenticated": ok, "token": f"token-{email}" if ok else None}

    if service == "auth_password_service":
        updated = len(str(data.get("new_password", ""))) >= 8
        return {"service": service, "updated": updated}

    if service == "submission_create_service":
        item = {
            "id": _next_id("submissions"),
            "author_id": data.get("author_id", "author-1"),
            "title": data.get("title", "Untitled"),
            "status": "submitted",
            "created_at": _now(),
        }
        _STATE["submissions"].append(item)
        return {"service": service, "submission": item}

    if service == "submission_save_service":
        submission_id = str(data.get("submission_id", ""))
        existing = _find("submissions", "id", submission_id)
        if existing is None:
            existing = {
                "id": int(submission_id) if submission_id.isdigit() else _next_id("submissions"),
                "author_id": data.get("author_id", "author-1"),
                "title": data.get("title", "Draft"),
                "status": "draft",
                "created_at": _now(),
            }
            _STATE["submissions"].append(existing)
        else:
            existing.update({"title": data.get("title", existing["title"]), "status": "draft"})
        return {"service": service, "submission": existing}

    if service == "manuscript_upload_service":
        submission_id = str(data.get("submission_id", ""))
        file_info = {
            "submission_id": submission_id,
            "filename": data.get("filename", "paper.pdf"),
            "uploaded_at": _now(),
        }
        return {"service": service, "uploaded": bool(submission_id), "file": file_info}

    if service == "review_submit_service":
        review = {
            "id": _next_id("reviews"),
            "submission_id": data.get("submission_id", "1"),
            "score": data.get("score", 0),
            "comments": data.get("comments", ""),
            "status": "submitted",
        }
        _STATE["reviews"].append(review)
        return {"service": service, "review": review}

    if service == "referee_assign_service":
        invitation = {
            "id": _next_id("invitations"),
            "submission_id": data.get("submission_id", "1"),
            "referee_id": data.get("referee_id", "ref-1"),
            "status": "pending",
            "sent_at": _now(),
        }
        _STATE["invitations"].append(invitation)
        return {"service": service, "invitation": invitation}

    if service == "review_invite_notify_service":
        return {"service": service, "invitations": _STATE["invitations"]}

    if service == "review_invite_response_service":
        invitation_id = str(data.get("invitation_id", ""))
        invitation = _find("invitations", "id", invitation_id)
        if invitation:
            invitation["status"] = data.get("response", "accepted")
        return {"service": service, "invitation": invitation}

    if service == "assigned_papers_service":
        referee_id = data.get("referee_id")
        invitations = _STATE["invitations"]
        if referee_id:
            invitations = [x for x in invitations if x.get("referee_id") == referee_id]
        return {"service": service, "assignments": invitations}

    if service == "referee_workload_service":
        referee_id = data.get("referee_id", "ref-1")
        count = len([x for x in _STATE["invitations"] if x.get("referee_id") == referee_id])
        return {"service": service, "referee_id": referee_id, "assigned": count, "within_limit": count <= 5}

    if service == "three_referees_service":
        submission_id = data.get("submission_id", "1")
        count = len([x for x in _STATE["invitations"] if str(x.get("submission_id")) == str(submission_id)])
        return {"service": service, "submission_id": submission_id, "assigned": count, "exactly_three": count == 3}

    if service == "decision_record_service":
        decision = {
            "id": _next_id("decisions"),
            "submission_id": data.get("submission_id", "1"),
            "outcome": data.get("outcome", "accept"),
            "decided_at": _now(),
        }
        _STATE["decisions"].append(decision)
        return {"service": service, "decision": decision}

    if service == "decision_notify_service":
        submission_id = str(data.get("submission_id", ""))
        decision = _find("decisions", "submission_id", submission_id)
        return {"service": service, "decision": decision, "notified": decision is not None}

    if service == "schedule_generate_service":
        schedule = {
            "id": _next_id("schedules"),
            "status": "draft",
            "published": False,
            "sessions": data.get("sessions", []),
        }
        _STATE["schedules"].append(schedule)
        return {"service": service, "schedule": schedule}

    if service == "schedule_edit_service" or service == "schedule_modify_service":
        schedule_id = str(data.get("schedule_id", ""))
        schedule = _find("schedules", "id", schedule_id)
        if schedule is None:
            schedule = {"id": int(schedule_id) if schedule_id.isdigit() else _next_id("schedules"), "status": "draft", "published": False, "sessions": []}
            _STATE["schedules"].append(schedule)
        schedule["sessions"] = data.get("sessions", schedule.get("sessions", []))
        return {"service": service, "schedule": schedule}

    if service == "schedule_publish_service":
        schedule_id = str(data.get("schedule_id", ""))
        schedule = _find("schedules", "id", schedule_id)
        if schedule is None:
            schedule = {"id": int(schedule_id) if schedule_id.isdigit() else _next_id("schedules"), "status": "published", "published": True, "sessions": []}
            _STATE["schedules"].append(schedule)
        schedule["status"] = "published"
        schedule["published"] = True
        return {"service": service, "schedule": schedule}

    if service == "schedule_notify_service":
        return {"service": service, "notified": True}

    if service == "schedule_view_attendee_service":
        published = [s for s in _STATE["schedules"] if s.get("published")]
        return {"service": service, "schedules": published}

    if service == "conference_register_service":
        registration = {
            "id": _next_id("registrations"),
            "attendee_id": data.get("attendee_id", "att-1"),
            "status": "initiated",
            "created_at": _now(),
        }
        _STATE["registrations"].append(registration)
        return {"service": service, "registration": registration}

    if service == "registration_payment_service":
        registration_id = str(data.get("registration_id", ""))
        payment = {
            "id": _next_id("payments"),
            "registration_id": registration_id,
            "amount": float(data.get("amount", 0)),
            "status": "paid" if float(data.get("amount", 0)) > 0 else "declined",
            "processed_at": _now(),
        }
        _STATE["payments"].append(payment)
        return {"service": service, "payment": payment}

    if service == "payment_confirmation_service":
        registration_id = str(data.get("registration_id", ""))
        return {
            "service": service,
            "registration_id": registration_id,
            "reference_code": f"TKT-{registration_id}-{uuid4().hex[:8].upper()}",
        }

    if service == "review_access_service":
        submission_id = data.get("submission_id")
        reviews = _STATE["reviews"]
        if submission_id:
            reviews = [r for r in reviews if str(r.get("submission_id")) == str(submission_id)]
        return {"service": service, "reviews": reviews}

    return {"service": service, "ok": True, "payload": data}
