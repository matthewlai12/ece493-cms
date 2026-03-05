from src.api.referee_workload import handle_referee_workload
from src.services.review_invite_notify_service import create_review_invitation, reset_review_invite_notify_state


def test_referee_workload_endpoint() -> None:
    reset_review_invite_notify_state()
    for index in range(4):
        create_review_invitation(
            submission_id=str(index + 1),
            referee_id="ref-contract",
            paper_title=f"Paper {index + 1}",
            paper_abstract="Abstract",
            referee_email="contract@example.com",
        )

    body = handle_referee_workload(payload={"referee_id": "ref-contract", "requested_new_assignments": 1})
    assert body["service"] == "referee_workload_service"
    assert body["within_limit"] is True
