import src.services.review_invite_response_service as response_service
from src.services.review_invite_notify_service import create_review_invitation, reset_review_invite_notify_state
from src.services.review_invite_response_service import respond_to_review_invitation


def setup_function() -> None:
    reset_review_invite_notify_state()


def test_respond_to_review_invitation_accept_success() -> None:
    created = create_review_invitation(
        submission_id="301",
        referee_id="ref-301",
        paper_title="Paper 301",
        paper_abstract="Abstract",
        referee_email="ref301@example.com",
    )
    invitation_id = str(created["invitation"]["id"])
    result = respond_to_review_invitation(invitation_id, "accept")

    assert result["updated"] is True
    assert result["invitation"]["status"] == "accepted"


def test_respond_to_review_invitation_reject_success() -> None:
    created = create_review_invitation(
        submission_id="302",
        referee_id="ref-302",
        paper_title="Paper 302",
        paper_abstract="Abstract",
        referee_email="ref302@example.com",
    )
    invitation_id = str(created["invitation"]["id"])
    result = respond_to_review_invitation(invitation_id, "reject")

    assert result["updated"] is True
    assert result["invitation"]["status"] == "rejected"


def test_respond_to_review_invitation_accept_blocked_when_limit_reached(monkeypatch) -> None:
    created = create_review_invitation(
        submission_id="303",
        referee_id="ref-303",
        paper_title="Paper 303",
        paper_abstract="Abstract",
        referee_email="ref303@example.com",
    )
    invitation = created["invitation"]

    monkeypatch.setattr(
        response_service,
        "list_review_invitations",
        lambda referee_id: [{"status": "accepted", "referee_id": referee_id} for _ in range(5)],
    )

    result = respond_to_review_invitation(str(invitation["id"]), "accept")
    assert result["updated"] is False
    assert result["blocked"] is True
