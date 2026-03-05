from typing import Any

from src.services.review_invite_notify_service import (
    get_review_invitation,
    list_review_invitations,
    update_review_invitation_status,
)

_MAX_ASSIGNMENTS = 5


def respond_to_review_invitation(invitation_id: str, response: str) -> dict[str, Any]:
    invitation = get_review_invitation(invitation_id)
    if invitation is None:
        raise ValueError("Review invitation was not found.")

    normalized_response = response.strip().lower()
    if normalized_response not in {"accept", "reject"}:
        raise ValueError("Response must be accept or reject.")

    if normalized_response == "accept":
        accepted_count = len(
            [
                i
                for i in list_review_invitations(invitation["referee_id"])
                if i["status"] == "accepted"
            ]
        )
        if invitation["status"] != "accepted" and accepted_count >= _MAX_ASSIGNMENTS:
            return {
                "invitation": invitation,
                "updated": False,
                "blocked": True,
                "message": "Referee has reached the maximum review limit and cannot accept more invitations.",
            }

    mapped_status = "accepted" if normalized_response == "accept" else "rejected"
    updated = update_review_invitation_status(invitation_id, mapped_status)
    if updated is None:
        raise ValueError("Review invitation was not found.")
    return {
        "invitation": updated,
        "updated": True,
        "blocked": False,
        "message": "Invitation response recorded.",
    }


def execute(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    result = respond_to_review_invitation(
        invitation_id=str(data.get("invitation_id", "")),
        response=str(data.get("response", "")),
    )
    return {"service": "review_invite_response_service", **result}
