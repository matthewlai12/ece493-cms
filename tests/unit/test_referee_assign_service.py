from src.services.audit_log import list_events, reset_events
from src.services.referee_assign_service import assign_referee
from src.services.review_invite_notify_service import reset_review_invite_notify_state


def setup_function() -> None:
    reset_review_invite_notify_state()
    reset_events()


def test_assign_referee_success() -> None:
    result = assign_referee(
        submission_id="801",
        referee_id="ref-801",
        paper_title="Paper 801",
        paper_abstract="Abstract",
        referee_email="ref801@example.com",
        assigned_by="chair-1",
    )
    assert result["blocked"] is False
    assert result["invitation"]["submission_id"] == 801
    assert list_events("referee_assign")[-1]["details"]["referee_id"] == "ref-801"


def test_assign_referee_safe_when_workload_exceeded() -> None:
    for index in range(5):
        assign_referee(
            submission_id=str(index + 1),
            referee_id="ref-limit",
            paper_title=f"Paper {index + 1}",
            paper_abstract="Abstract",
            referee_email="limit@example.com",
            assigned_by="chair-1",
        )

    blocked = assign_referee(
        submission_id="999",
        referee_id="ref-limit",
        paper_title="Overflow",
        paper_abstract="Abstract",
        referee_email="limit@example.com",
        assigned_by="chair-1",
    )
    assert blocked["blocked"] is True
    assert blocked["invitation"] is None
