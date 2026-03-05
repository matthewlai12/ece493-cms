from src.services.referee_workload_service import check_referee_workload
from src.services.review_invite_notify_service import create_review_invitation, reset_review_invite_notify_state


def setup_function() -> None:
    reset_review_invite_notify_state()


def test_check_referee_workload_within_limit() -> None:
    for index in range(3):
        create_review_invitation(
            submission_id=str(index + 1),
            referee_id="ref-workload",
            paper_title=f"Paper {index + 1}",
            paper_abstract="Abstract",
            referee_email="ref@example.com",
        )

    result = check_referee_workload("ref-workload", requested_new_assignments=2)
    assert result["within_limit"] is True
    assert result["projected_total"] == 5


def test_check_referee_workload_exceeds_limit() -> None:
    for index in range(5):
        create_review_invitation(
            submission_id=str(index + 1),
            referee_id="ref-over",
            paper_title=f"Paper {index + 1}",
            paper_abstract="Abstract",
            referee_email="over@example.com",
        )

    result = check_referee_workload("ref-over", requested_new_assignments=1)
    assert result["within_limit"] is False
    assert result["message"] == "Workload limit exceeded."
