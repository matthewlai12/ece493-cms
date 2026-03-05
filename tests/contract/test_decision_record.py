from src.api.decision_record import handle_decision_record
from src.services.decision_notify_service import reset_decision_notify_state


def test_decision_record_endpoint() -> None:
    reset_decision_notify_state()
    body = handle_decision_record(
        submission_id="1",
        payload={"outcome": "accept", "decided_by": "chair", "author_email": "author@example.com"},
    )
    assert body["service"] == "decision_record_service"
    assert body["decision"]["outcome"] == "accept"
    assert body["notified"] is True
