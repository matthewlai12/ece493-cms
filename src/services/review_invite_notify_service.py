from datetime import datetime, timezone
from typing import Any, TypedDict

from src.services.notification_service import send_email

_MAX_ASSIGNMENTS = 5
_invitations: list[dict[str, Any]] = []


class ReviewInvitationResult(TypedDict):
    id: int
    submission_id: int
    referee_id: str
    status: str
    paper_title: str
    paper_abstract: str
    sent_at: str
    responded_at: str | None
    respond_to: str


def create_review_invitation(
    submission_id: str,
    referee_id: str,
    paper_title: str,
    paper_abstract: str,
    referee_email: str,
) -> dict[str, Any]:
    if not str(submission_id).isdigit() or int(submission_id) <= 0:
        raise ValueError("Submission ID is invalid.")
    if not referee_id.strip():
        raise ValueError("Referee ID is required.")
    if not paper_title.strip():
        raise ValueError("Paper title is required.")

    normalized_referee_id = referee_id.strip()
    active_assignments = len(
        [i for i in _invitations if i["referee_id"] == normalized_referee_id and i["status"] in {"pending", "accepted"}]
    )
    if active_assignments >= _MAX_ASSIGNMENTS:
        return {
            "invitation": None,
            "notified": False,
            "blocked": True,
            "message": "Referee has reached the maximum allowed number of review assignments.",
        }

    invitation_id = len(_invitations) + 1
    invitation: ReviewInvitationResult = {
        "id": invitation_id,
        "submission_id": int(submission_id),
        "referee_id": normalized_referee_id,
        "status": "pending",
        "paper_title": paper_title.strip(),
        "paper_abstract": paper_abstract.strip(),
        "sent_at": datetime.now(timezone.utc).isoformat(),
        "responded_at": None,
        "respond_to": f"/api/referee/invitations/{invitation_id}/response",
    }
    _invitations.append(invitation)

    delivery = send_email(
        referee_email.strip().lower(),
        f"Review invitation for submission #{invitation['submission_id']}",
        f"You have been invited to review '{invitation['paper_title']}'.",
    )
    return {
        "invitation": invitation,
        "notified": bool(delivery.get("sent")),
        "blocked": False,
        "message": "Invitation sent.",
    }


def list_review_invitations(referee_id: str = "") -> list[ReviewInvitationResult]:
    if referee_id.strip():
        return [dict(i) for i in _invitations if i["referee_id"] == referee_id.strip()]
    return [dict(i) for i in _invitations]


def get_review_invitation(invitation_id: str) -> ReviewInvitationResult | None:
    if not str(invitation_id).isdigit():
        return None
    iid = int(invitation_id)
    for invitation in _invitations:
        if int(invitation["id"]) == iid:
            return dict(invitation)
    return None


def count_active_assignments(referee_id: str) -> int:
    rid = referee_id.strip()
    return len([i for i in _invitations if i["referee_id"] == rid and i["status"] in {"pending", "accepted"}])


def update_review_invitation_status(invitation_id: str, status: str) -> ReviewInvitationResult | None:
    if not str(invitation_id).isdigit():
        return None
    iid = int(invitation_id)
    for invitation in _invitations:
        if int(invitation["id"]) == iid:
            invitation["status"] = status
            invitation["responded_at"] = datetime.now(timezone.utc).isoformat()
            return dict(invitation)
    return None


def execute(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    has_creation_payload = any(
        key in data for key in ("submission_id", "paper_title", "paper_abstract", "referee_email")
    )
    if has_creation_payload:
        result = create_review_invitation(
            submission_id=str(data.get("submission_id", "")),
            referee_id=str(data.get("referee_id", "")),
            paper_title=str(data.get("paper_title", "")),
            paper_abstract=str(data.get("paper_abstract", "")),
            referee_email=str(data.get("referee_email", "")),
        )
        return {"service": "review_invite_notify_service", **result}

    invitations = list_review_invitations(referee_id=str(data.get("referee_id", "")))
    return {"service": "review_invite_notify_service", "invitations": invitations}


def reset_review_invite_notify_state() -> None:
    _invitations.clear()
