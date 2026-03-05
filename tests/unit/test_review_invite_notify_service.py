from src.services.review_invite_notify_service import (
    create_review_invitation,
    execute,
    reset_review_invite_notify_state,
)


def setup_function() -> None:
    reset_review_invite_notify_state()


def test_create_review_invitation_success() -> None:
    result = create_review_invitation(
        submission_id="101",
        referee_id="ref-1",
        paper_title="Paper 101",
        paper_abstract="Abstract",
        referee_email="ref1@example.com",
    )
    assert result["blocked"] is False
    assert result["notified"] is True
    assert result["invitation"]["respond_to"].endswith("/response")


def test_create_review_invitation_when_workload_limit_reached() -> None:
    for index in range(5):
        create_review_invitation(
            submission_id=str(index + 1),
            referee_id="ref-2",
            paper_title=f"Paper {index + 1}",
            paper_abstract="Abstract",
            referee_email="ref2@example.com",
        )

    blocked = create_review_invitation(
        submission_id="999",
        referee_id="ref-2",
        paper_title="Overflow",
        paper_abstract="Abstract",
        referee_email="ref2@example.com",
    )
    assert blocked["blocked"] is True
    assert blocked["invitation"] is None


def test_execute_lists_invitations_for_referee() -> None:
    create_review_invitation(
        submission_id="1",
        referee_id="ref-a",
        paper_title="A",
        paper_abstract="A",
        referee_email="a@example.com",
    )
    create_review_invitation(
        submission_id="2",
        referee_id="ref-b",
        paper_title="B",
        paper_abstract="B",
        referee_email="b@example.com",
    )

    body = execute({"referee_id": "ref-a"})
    assert len(body["invitations"]) == 1
    assert body["invitations"][0]["referee_id"] == "ref-a"
