from src.api.referee_workload import handle_referee_workload
from src.services.review_invite_notify_service import create_review_invitation, reset_review_invite_notify_state


def test_referee_workload_endpoint_blocks_when_limit_exceeded() -> None:
    reset_review_invite_notify_state()
    for index in range(5):
        create_review_invitation(
            submission_id=str(index + 1),
            referee_id="ref-int",
            paper_title=f"Paper {index + 1}",
            paper_abstract="Abstract",
            referee_email="int@example.com",
        )

    body = handle_referee_workload(payload={"referee_id": "ref-int", "requested_new_assignments": 1})
    assert body["within_limit"] is False
    assert body["projected_total"] == 6
